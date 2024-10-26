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
    QPlainTextEdit
)
from PyQt5.QtCore import QCoreApplication, Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QMovie


class AppTheme:
    main_color = "white"
    text_color = "black"
    button_color = "black"
    button_text_color = "white"
    accent_color = "red"
    alert_color = "red"
    interface_color = "gray"

    plain_text_font = "Consolas"
    button_text_font = "Consolas"

    button_border_radius = 5

    button_text_size = 20
    plain_text_size = 20
    hint_text_size = 15


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Генератор документов")
        self.create_buttons()
        self.init_main_menu()
        

    def create_buttons(self):
        # buttons of main menu
        self.check_data_button = self.create_button(
            "Проверить актуальность данных", self.check_data_action
        )
        self.create_docs_button = self.create_button(
            "Создать документы по мероприятию", self.create_docs_action
        )
        self.get_contacts_button = self.create_button(
            "Связаться с разработчиком", self.get_contacts_action
        )

        # buttons of creating event menu
        self.next_create_event_button = self.create_button(
            "Далее", self.next_create_event_action
        )
        self.back_create_event_button = self.create_button(
            "Назад", self.back_create_event_action
        )


    def init_main_menu(self):
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {AppTheme.main_color};")

        main_vbox = QVBoxLayout(widget)
        main_vbox.addWidget(self.check_data_button)
        main_vbox.addWidget(self.create_docs_button)
        main_vbox.addWidget(self.get_contacts_button)

        self.setCentralWidget(widget)
        self.show()

    def init_get_event_window(self):
        widget = QWidget()
        main_vbox = QVBoxLayout(widget)
        
        upper_vbox = QVBoxLayout()

        event_name_vbox = QVBoxLayout()
        event_name_label = self.create_label("Введите название мероприятия")
        event_name_plain_text = self.create_plain_text_edit("Название мероприятия")
        event_name_vbox.addWidget(event_name_label)
        event_name_vbox.addWidget(event_name_plain_text)

        date_hbox = QHBoxLayout()
        date_label = self.create_label("Дата мероприятия")
        date_plain_text = self.create_plain_text_edit('с 3 по 5 октября')
        date_hbox.addWidget(date_label)
        date_hbox.addWidget(date_plain_text)

        signature_vbox = QVBoxLayout()
        signature_label = self.create_label("Кто будет подписывать документ?")
        signature_post_plain_text = self.create_plain_text_edit("Должность")
        signature_name_plain_text = self.create_plain_text_edit("Фамилия И.О.")
        signature_vbox.addWidget(signature_label)
        signature_vbox.addWidget(signature_post_plain_text)
        signature_vbox.addWidget(signature_name_plain_text)

        upper_vbox.addLayout(event_name_vbox)
        upper_vbox.addLayout(date_hbox)
        upper_vbox.addLayout(signature_vbox)

        bottom_hbox_with_buttons = QHBoxLayout()
        bottom_hbox_with_buttons.addWidget(self.back_create_event_button)
        bottom_hbox_with_buttons.stretch(1)
        bottom_hbox_with_buttons.addWidget(self.next_create_event_button)

        main_vbox.addLayout(upper_vbox)
        main_vbox.addLayout(bottom_hbox_with_buttons)
        self.setCentralWidget(widget)
        self.show()


    def check_data_action(self):
        pass

    def create_docs_action(self):
        self.init_get_event_window()

    def get_contacts_action(self):
        pass

    def next_create_event_action(self):
        pass

    def back_create_event_action(self):
        pass

    def create_new_signature_action(self):
        pass

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
                             margin: 10px 10px 10px 10px;
                             border-radius: {AppTheme.button_border_radius}px;
                             """
        )
        button.setFont(QFont(AppTheme.button_text_font, AppTheme.button_text_size))
        return button

    def create_label(self, text: str) -> QLabel:
        label = QLabel()
        label.setText(text)
        label.setFont(QFont(AppTheme.plain_text_font, AppTheme.plain_text_size))
        label.setStyleSheet(f"color: {AppTheme.text_color};")
        return label
    
    def create_plain_text_edit(self, text: str) -> QPlainTextEdit:
        plain_text = QPlainTextEdit()
        plain_text.setPlainText(text)
        plain_text.setFont(QFont(AppTheme.plain_text_font, AppTheme.plain_text_size))
        plain_text.setStyleSheet(f"color: {AppTheme.text_color};")
        return plain_text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
