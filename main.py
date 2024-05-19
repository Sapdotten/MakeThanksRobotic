import pandas as pd
import json
from document import Documents


def get_table_data(xlsx_file: str) -> pd.DataFrame:
    """
    Извлекает данные из указанной таблицы в файла Excel.

    Args:
    - xlsx_file (str): Путь к файлу Excel, из которого нужно извлечь данные.
    - name_sheet (str): Название листа в файле Excel, на котором находится
    таблица.

    Returns:
    - pd.DataFrame: DataFrame с данными из указанной таблицы(библиотека pandas).

    Example:
    - extract_table_data("example.xlsx", "Sheet1")
    """

    return pd.ExcelFile(xlsx_file).parse()


def get_json(path: str):
    with open(path, 'r', encoding='UTF-8') as file:
        return json.load(file)


def process_people(data: pd.DataFrame, groups, instituts):
    people = {}
    for key in instituts.keys():
        people[key] = []
    for row in data.iloc[1:].itertuples():
        group_number = row[2][5:]
        for key in groups.keys():
            if group_number in groups[key]:
                for inst in instituts.keys():
                    if key in instituts[inst]['numbers']:
                        people[inst].append([row[1], row[2]])
                        break
                break
    for key in people.keys():
        people[key] = sorted(people[key], key=lambda k: k[0])
    return people


if __name__ == '__main__':
    settings = get_json('configs.json')
    groups = get_json('groups.json')
    instituts = get_json('instituts.json')

    volunteers = get_table_data(settings['tables']['volunteers'])
    volunteers = process_people(volunteers, groups, instituts)

    orgs = get_table_data(settings['tables']['orgs'])
    orgs = process_people(orgs, groups, instituts)

    for key in volunteers.keys():
        new_doc = Documents()
        new_doc.set_event_name(settings['event'])
        new_doc.set_data(settings['date'])
        new_doc.set_institute(key, instituts[key]['director']['post'], instituts[key]['director']['name'])
        new_doc.set_signature(settings['signature']['post'], settings['signature']['person'])
        for human in volunteers[key]:
            new_doc.add_fio(human)
        new_doc.make_thanks(settings['output_files']['volunteers'], settings['templates']['volunteers_thanks'],
                            'Финист')

    for key in orgs.keys():
        new_doc = Documents()
        new_doc.set_event_name(settings['event'])
        new_doc.set_data(settings['date'])
        new_doc.set_signature(settings['signature']['post'], settings['signature']['person'])
        new_doc.set_institute(key, instituts[key]['director']['post'], instituts[key]['director']['name'])
        for human in orgs[key]:
            new_doc.add_fio(human)
        new_doc.make_thanks(settings['output_files']['orgs'], settings['templates']['orgs_thanks'], 'Финист')

    for key in volunteers.keys():
        volunteers[key] += orgs[key]
        volunteers[key] = sorted(volunteers[key], key=lambda k: k[0])
    for key in volunteers.keys():
        new_doc = Documents()
        new_doc.set_event_name(settings['event'])
        new_doc.set_data(settings['date'])
        new_doc.set_institute(key, instituts[key]['director']['post'], instituts[key]['director']['name'])
        new_doc.set_signature(settings['signature']['post'], settings['signature']['person'])
        for human in volunteers[key]:
            new_doc.add_fio(human)
        new_doc.make_exemption(settings['output_files']['exemptions'], settings['templates']['exemptions'], 'Финист')
