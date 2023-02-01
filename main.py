import datetime
import json
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from constants import CITIES, CURRENCIES, CONFIG_FILE, LOGO_FILE
from ecolines import Ui_mainWindow
from handlers import UIHandlers


class EcolinesApp(QMainWindow):
    def __init__(self, parent=None):
        super(EcolinesApp, self).__init__(parent)

        self.ui = Ui_mainWindow()
        self.setFixedSize(700, 480)
        self.ui.setupUi(self)

        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.timer_started = False

        self.ui.searchButton.clicked.connect(lambda: UIHandlers.search_button_handler(self))
        self.ui.emailCheckBox.stateChanged.connect(lambda: UIHandlers.email_checkbox_handler(self))

        self.set_defaults()

    def set_defaults(self):
        self.ui.dateEdit.setDate(datetime.datetime.now())
        self.ui.afterTimeEdit.setTime(datetime.time(hour=0, minute=0))
        self.ui.beforeTimeEdit.setTime(datetime.time(hour=23, minute=59))
        self.ui.spinBox.setValue(60)
        self.ui.emailLineEdit.setEnabled(False)

        for city in CITIES.keys():
            self.ui.fromComboBox.addItem(city)
            self.ui.toComboBox.addItem(city)

        for currency in CURRENCIES.keys():
            self.ui.currencyComboBox.addItem(currency)

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as openfile:
                values = json.load(openfile)
                self.set_saved_values(values=values)
        else:
            self.ui.fromComboBox.setCurrentText('Warsaw 01 (Zachodnia)')
            self.ui.toComboBox.setCurrentText('Minsk (Centralniy)')
            self.ui.currencyComboBox.setCurrentText('BYN')

    def set_saved_values(self, values: dict) -> None:
        self.ui.dateEdit.setDate(datetime.datetime.strptime(values.get('date'), '%d.%m.%Y'))
        self.ui.afterTimeEdit.setTime(datetime.datetime.strptime(values.get('after_time'), '%H:%M').time())
        self.ui.beforeTimeEdit.setTime(datetime.datetime.strptime(values.get('before_time'), '%H:%M').time())
        self.ui.fromComboBox.setCurrentText(values.get('from_city'))
        self.ui.toComboBox.setCurrentText(values.get('to_city'))
        self.ui.currencyComboBox.setCurrentText(values.get('currency'))
        self.ui.spinBox.setValue(values.get('interval'))
        self.ui.soundCheckBox.setChecked(True)
        self.ui.emailCheckBox.setChecked(bool(values.get('email')))
        self.ui.emailLineEdit.setText(values.get('email'))


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon(LOGO_FILE))

    form = EcolinesApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

