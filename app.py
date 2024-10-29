import sys

from PyQt5.QtWidgets import (
    QPushButton,
    QApplication,
    QFileDialog,
    QMainWindow,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QGraphicsDropShadowEffect,
    QDesktopWidget,
    QCheckBox,
    QPlainTextEdit,
)
from PyQt5.QtCore import QCoreApplication, Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QMovie

from document import Documents
import utils


class AppTheme:
    main_color = "#f5f5f5"
    label_text_color = "#333333"
    plain_text_color = "#828282"
    button_color = "#27ae61"
    button_text_color = "#f5f5f5"
    accent_color = "#2f80ec"
    alert_color = "#eb5757"
    interface_color = "#828282"

    label_text_font = "Consolas"
    plain_text_font = "Times New Roman"
    button_text_font = "Consolas"

    button_border_radius = 5

    button_text_size = 17
    label_text_size = 15
    plain_text_size = 14
    hint_text_size = 15


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генератор документов")
        self.init_get_event_window()

    def init_main_menu(self):
        """
        Отображает главное меню с выбором действий:
        - Проверить актуальность данных
        - Создать доки по мероприятию
        - Связаться с разработчиком
        """
        widget = QWidget()

        create_docs_button = self.create_button(
            "Создать документы по мероприятию", self.create_docs_action
        )
        get_contacts_button = self.create_button(
            "Поблагодарить разработчиков", self.get_contacts_action
        )

        widget.setStyleSheet(f"background-color: {AppTheme.main_color};")

        main_vbox = QVBoxLayout(widget)
        main_vbox.addStretch(1)
        main_vbox.addWidget(create_docs_button)
        main_vbox.addWidget(get_contacts_button)
        main_vbox.addStretch(1)

        self.setCentralWidget(widget)
        self.adjustSize()
        self.show()

    def init_get_event_window(self, doc: Documents = None):
        """
        Отобржает меню со сбором данных по мероприятиюЖ
        - навание мерпориятия
        - дата мероприятия
        - пост подписывающего документ
        - фИО подписывающего документ
        """
        widget = QWidget()

        if doc is None:
            doc = Documents()

        next_create_event_button = self.create_button(
            "Далее", lambda x: self.next_create_event_action(doc)
        )
        back_create_event_button = self.create_button(
            "Назад", self.back_create_event_action
        )

        main_vbox = QVBoxLayout(widget)
        upper_vbox = QVBoxLayout()

        event_name_vbox = QVBoxLayout()
        event_name_label = self.create_label("Введите название мероприятия")
        self.event_name_plain_text = self.create_plain_text_edit(doc.event_name)
        event_name_vbox.addWidget(event_name_label)
        event_name_vbox.addWidget(self.event_name_plain_text)

        date_hbox = QHBoxLayout()
        date_label = self.create_label("Дата мероприятия")
        self.date_plain_text = self.create_plain_text_edit(doc.date)
        date_hbox.addWidget(date_label)
        date_hbox.addWidget(self.date_plain_text)

        signature_vbox = QVBoxLayout()
        signature_label = self.create_label("Кто будет подписывать документ?")
        self.signature_post_plain_text = self.create_plain_text_edit(doc.signature_post)
        self.signature_name_plain_text = self.create_plain_text_edit(doc.signature_name)
        signature_vbox.addWidget(signature_label)
        signature_vbox.addWidget(self.signature_post_plain_text)
        signature_vbox.addWidget(self.signature_name_plain_text)

        upper_vbox.addLayout(event_name_vbox)
        upper_vbox.addLayout(date_hbox)
        upper_vbox.addLayout(signature_vbox)

        bottom_hbox_with_buttons = QHBoxLayout()
        bottom_hbox_with_buttons.addWidget(back_create_event_button)
        bottom_hbox_with_buttons.addWidget(next_create_event_button)

        main_vbox.addLayout(upper_vbox)
        main_vbox.addLayout(bottom_hbox_with_buttons)
        self.adjustSize()
        self.setCentralWidget(widget)
        self.show()

    def init_create_docs_window(self, doc: Documents):
        """
        Меню с выбором типа документов:
        - благодарность за организацию
        - благодарность за помощь в организации
        - освобождения
        """
        widget = QWidget()
        main_vbox = QVBoxLayout()

        path_to_src_label = self.create_label("Укажите путь к таблице с людьми")
        set_path_to_src_button = self.create_button(
            "Указать путь", self.set_path_to_src_action, AppTheme.accent_color
        )
        self.chosen_path_to_src_label = self.create_label(
            "Путь к файлу...", AppTheme.interface_color
        )
        path_note_label = self.create_label(
            """Обратите внимание, что в таблице должен быть один лист, на котором:
1) В первом столбце записаны ФИО студентов
2) Во втором столбце указаны номера группы в формате 0000-000000D""",
            AppTheme.alert_color,
        )
        set_path_to_result_label = self.create_label(
            "Укажите папку, куда сохранить сгенерированные документы"
        )
        set_path_to_result_button = self.create_button(
            "Указать путь", self.set_path_to_result_action, AppTheme.accent_color
        )
        self.chosen_path_to_result_label = self.create_label(
            "Путь к папке...", AppTheme.interface_color
        )

        create_gratitude_org_button = self.create_button(
            "Создать благодарность за организацию",
            lambda x: self.make_gratitude_org(doc),
        )
        create_gratitude_help_button = self.create_button(
            "Создать благодарность за помощь в организации",
            lambda x: self.make_gratitude_help(doc),
        )
        create_release_button = self.create_button(
            "Создать освобождения", lambda x: self.make_exemption(doc)
        )
        create_docs_back_button = self.create_button(
            "Назад", lambda x: self.create_docs_back_action(doc), AppTheme.alert_color
        )
        main_vbox.addStretch(1)
        main_vbox.addWidget(path_to_src_label)
        main_vbox.addWidget(set_path_to_src_button)
        main_vbox.addWidget(self.chosen_path_to_src_label)
        main_vbox.addWidget(path_note_label)
        main_vbox.addStretch(1)
        main_vbox.addWidget(set_path_to_result_label)
        main_vbox.addWidget(set_path_to_result_button)
        main_vbox.addWidget(self.chosen_path_to_result_label)
        main_vbox.addStretch(1)
        main_vbox.addWidget(create_gratitude_org_button),
        main_vbox.addWidget(create_gratitude_help_button)
        main_vbox.addWidget(create_release_button)
        main_vbox.addWidget(create_docs_back_button)
        main_vbox.addStretch(1)

        widget.setLayout(main_vbox)
        self.setCentralWidget(widget)
        self.adjustSize()
        self.show()


    def create_docs_action(self):
        self.init_get_event_window()

    def get_contacts_action(self):
        pass

    def next_create_event_action(self, doc: Documents):
        """This method is called when the create_event_action is called .

        Args:
            doc (Documents): [description]
        """
        doc.event_name = self.event_name_plain_text.toPlainText()
        doc.date = self.date_plain_text.toPlainText()
        doc.signature_name = self.signature_name_plain_text.toPlainText()
        doc.signature_post = self.signature_post_plain_text.toPlainText()
        self.init_create_docs_window(doc)

    def back_create_event_action(self):
        self.init_main_menu()

    def create_gratitude_org_action(self, doc: Documents):
        self.init_get_paths_window(doc, lambda x: self.make_gratitude_org(doc))

    def create_gratitude_help_action(self, doc: Documents):
        self.init_get_paths_window(doc, lambda x: self.make_gratitude_help(doc))

    def create_release_action(self, doc: Documents):
        self.init_get_paths_window(doc, lambda x: self.make_exemption(doc))

    def create_docs_back_action(self, doc: Documents):
        self.init_get_event_window(doc)

    def set_path_to_src_action(self):
        self.src_table = QFileDialog.getOpenFileName()[0]
        self.chosen_path_to_src_label.setText(self.src_table)

    def set_path_to_result_action(self):
        self.result_path = QFileDialog.getExistingDirectory()
        self.chosen_path_to_result_label.setText(self.result_path)

    def get_paths_back_action(self, doc: Documents):
        self.init_create_docs_window(doc)

    def make_gratitude_org(self, doc: Documents):
        utils.MakeDocs.make_thank_org(doc, self.result_path, self.src_table)
        self.show_success_message()

    def make_gratitude_help(self, doc: Documents):
        utils.MakeDocs.make_thank_help(doc, self.result_path, self.src_table)
        self.show_success_message()

    def make_exemption(self, doc: Documents):
        utils.MakeDocs.make_exemption(doc, self.result_path, self.src_table)
        self.show_success_message()

    def create_button(
        self, text: str, func: callable, button_color=None
    ) -> QPushButton: 
        if button_color is None:
            button_color = AppTheme.button_color
        button = QPushButton(text)
        button.clicked.connect(func)
        button.resize(button.minimumSizeHint())
        button.setStyleSheet(
            f"""
                             background-color: {button_color};
                             color: {AppTheme.button_text_color};
                             font-size: {AppTheme.button_text_size}px;
                             padding: 10px 10px 10px 10px;
                             margin: 7px 7px 7px 7px;
                             border-radius: {AppTheme.button_border_radius}px;
                             """
        )
        button.setFont(QFont(AppTheme.button_text_font, AppTheme.button_text_size))
        return button

    def create_label(self, text: str, text_color: str = None) -> QLabel:
        if text_color is None:
            text_color = AppTheme.label_text_color
        label = QLabel()
        label.setText(text)
        label.setFont(QFont(AppTheme.label_text_font, AppTheme.label_text_size))
        label.setStyleSheet(f"color: {text_color};")
        return label

    def create_plain_text_edit(self, text: str) -> QPlainTextEdit:
        plain_text = QPlainTextEdit()
        plain_text.setPlainText(text)
        plain_text.setFont(QFont(AppTheme.plain_text_font, AppTheme.plain_text_size))
        plain_text.setStyleSheet(f"color: {AppTheme.plain_text_color};")
        return plain_text
    
    def show_success_message(self):
        # Создание сообщения об успехе
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Операция выполнена успешно!")
        msg.setWindowTitle("Успех")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
