from bs4 import BeautifulSoup
import requests
import json


if __name__ == "__main__":
    data = {}
    html = requests.get("https://ssau.ru/education/program").text
    page = BeautifulSoup(html, "lxml")
    h_and_tables = page.find("div", class_="body1-text")
    hh = []
    groups = []
    for elem in h_and_tables:
        if elem.name == "h4":
            hh.append(elem.text.strip())
            groups.append([])
        elif elem.name == "table":
            trs = elem.find_all("tr")
            for tr in trs[2:]:
                tds = tr.find_all("td")
                groups[-1].append(tds[1].text.replace(".", "").strip())

    data = {}
    for i in range(0, len(hh)):
        data[hh[i]] = groups[i]

    with open("parsed_groups.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False)
