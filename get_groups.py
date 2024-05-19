from bs4 import BeautifulSoup
import requests
import json


def get_links():
    data = {}
    html = requests.get("https://ssau.ru/rasp").text
    page = BeautifulSoup(html, 'lxml')
    facultets = page.find_all('div', class_='card-default faculties__item')
    for elem in facultets:
        links = elem.find_all('a', href=True)
        for link in links:
            data[elem.text.strip()] = link['href']
    return data


def get_groups_via_links(data: dict) -> dict[str, set[str]]:
    group_fac = {}
    for key in data.keys():
        html = requests.get("https://ssau.ru" + data[key]).text
        page = BeautifulSoup(html, 'lxml')
        groups = page.find_all('a', class_="btn-text group-catalog__group")
        group_fac[key] = set()
        for group in groups:
            group_fac[key].add(group.text[6:].strip())
        for key in data.keys():
            data[key] = list(data[key])
    return group_fac


if __name__ == '__main__':
    data = get_links()
    data = get_groups_via_links(data)
    with open("groups.json", 'w', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False)
