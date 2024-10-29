import json
from document import Documents
import pandas as pd

class FileManager:
    @classmethod
    def read_json(cls,file: str) -> dict:
        with  open(file, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        return data
    
    @classmethod
    def write_json(cls, file:str, data: dict) -> None:
        with open(file, 'w') as f:
            json.dump(data, f)

    @classmethod
    def get_table_data(cls, xlsx_file: str) -> pd.DataFrame:
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

class MakeDocs:
    CONFIGS_FILE = ".\\src\\configs.json"
    INSTITUTS_FILE = ".\\src\\instituts.json"
    GROUPS_FILE = ".\\src\\groups.json"

    @classmethod
    def process_students(cls, table: str) -> dict:
        readed_students = FileManager.get_table_data(table)
        groups = FileManager.read_json(cls.GROUPS_FILE)
        students = {}

        for key in groups.keys():
            students[key] = []
        for student in readed_students.itertuples():
            group_number = student[2].strip()[5:11]
            for key in students.keys():
                if group_number in groups[key]:
                    students[key].append([student[1], student[2]])
        
        return students
    
    @classmethod
    def make_thanks_org(cls, doc: Documents, dir: str, table: str) -> None:
        instituts = FileManager.read_json(cls.INSTITUTS_FILE)
        students = cls.process_students(table)

        new_doc = Documents()
        new_doc.event_name = doc.event_name
        new_doc.date = doc.date
        new_doc.signature_post = doc.signature_post
        new_doc.signature_name = doc.signature_name

        files_paths = FileManager.read_json(cls.CONFIGS_FILE)

        for key in instituts.keys():
            new_doc.fios = sorted(students[key], key = lambda x: x[0])
            new_doc.institut_name = instituts[key]["declension"]
            new_doc.make_thanks(dir, files_paths["gratitude_org_file_path"], doc.event_name)
            print("made ", key)





