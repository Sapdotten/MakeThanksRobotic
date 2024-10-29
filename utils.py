import json
from document import Documents
import pandas as pd


class FileManager:
    @classmethod
    def read_json(cls, file: str) -> dict:
        """Reads a JSON file and returns it as a dictionary .

        Args:
            file (str): [description]

        Returns:
            dict: [description]
        """
        with open(file, "r", encoding="UTF-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def write_json(cls, file: str, data: dict) -> None:
        with open(file, "w") as f:
            json.dump(data, f)

    @classmethod
    def get_table_data(cls, xlsx_file: str) -> pd.DataFrame:
        """Parse the table data and return a pandas DataFrame .

        Args:
            xlsx_file (str): [description]

        Returns:
            pd.DataFrame: [description]
        """
        return pd.ExcelFile(xlsx_file).parse()


class MakeDocs:
    CONFIGS_FILE = ".\\src\\configs.json"
    INSTITUTS_FILE = ".\\src\\instituts.json"
    GROUPS_FILE = ".\\src\\groups.json"

    @classmethod
    def _process_students(cls, table: str) -> dict:
        """"""
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
    def _make_doc(
        cls, doc: Documents, dir: str, table: str, template_path: str
    ) -> None:
        """Make a doc and then add it to the table .

        Args:
            doc (Documents): [description]
            dir (str): [description]
            table (str): [description]
            template_path (str): [description]
        """
        instituts = FileManager.read_json(cls.INSTITUTS_FILE)
        students = cls._process_students(table)

        new_doc = Documents()
        new_doc.event_name = doc.event_name
        new_doc.date = doc.date
        new_doc.signature_post = doc.signature_post
        new_doc.signature_name = doc.signature_name

        for key in instituts.keys():
            new_doc.fios = sorted(students[key], key=lambda x: x[0])
            new_doc.institut_name = instituts[key]["declension"]
            new_doc.director_name = instituts[key]["director"]["name"]
            new_doc.director_post = instituts[key]["director"]["post"]
            new_doc.make_thanks(dir, template_path, doc.event_name)
            print("made ", key)

    @classmethod
    def make_thank_org(cls, doc: Documents, dir: str, table: str):
        files_paths = FileManager.read_json(cls.CONFIGS_FILE)
        instituts = FileManager.read_json(cls.INSTITUTS_FILE)
        students = cls._process_students(table)

        new_doc = Documents()
        new_doc.event_name = doc.event_name
        new_doc.date = doc.date
        new_doc.signature_post = doc.signature_post
        new_doc.signature_name = doc.signature_name

        for key in instituts.keys():
            new_doc.fios = sorted(students[key], key=lambda x: x[0])
            new_doc.institut_name = instituts[key]["declension"]
            new_doc.director_name = instituts[key]["director"]["name"]
            new_doc.director_post = instituts[key]["director"]["post"]
            new_doc.make_thanks(dir, files_paths["gratitude_org_file_path"], "Благодарность организаторам "+doc.event_name)
            print("made ", key)
        

    @classmethod
    def make_thank_help(cls, doc: Documents, dir: str, table: str):
        files_paths = FileManager.read_json(cls.CONFIGS_FILE)
        instituts = FileManager.read_json(cls.INSTITUTS_FILE)
        students = cls._process_students(table)

        new_doc = Documents()
        new_doc.event_name = doc.event_name
        new_doc.date = doc.date
        new_doc.signature_post = doc.signature_post
        new_doc.signature_name = doc.signature_name

        for key in instituts.keys():
            new_doc.fios = sorted(students[key], key=lambda x: x[0])
            new_doc.institut_name = instituts[key]["declension"]
            new_doc.director_name = instituts[key]["director"]["name"]
            new_doc.director_post = instituts[key]["director"]["post"]
            new_doc.make_thanks(dir, files_paths["gratitude_help_file_path"], "Благодарность за помощь "+doc.event_name)
            print("made ", key)

    @classmethod
    def make_exemption(cls, doc: Documents, dir: str, table: str):
        files_paths = FileManager.read_json(cls.CONFIGS_FILE)
        instituts = FileManager.read_json(cls.INSTITUTS_FILE)
        students = cls._process_students(table)

        new_doc = Documents()
        new_doc.event_name = doc.event_name
        new_doc.date = doc.date
        new_doc.signature_post = doc.signature_post
        new_doc.signature_name = doc.signature_name

        for key in instituts.keys():
            new_doc.fios = sorted(students[key], key=lambda x: x[0])
            new_doc.institut_name = instituts[key]["declension"]
            new_doc.director_name = instituts[key]["director"]["name"]
            new_doc.director_post = instituts[key]["director"]["post"]
            new_doc.make_exemption(dir, files_paths["exemption_file_path"], "Освобождения "+doc.event_name)
            print("made ", key)
