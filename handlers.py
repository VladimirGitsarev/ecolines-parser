import datetime
import json
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from typing import Any, Tuple

from PyQt5 import QtMultimedia
from PyQt5.QtCore import QTimer

from components import CustomDialog
from constants import (
    CURRENT_DIR, CITIES, BUY_URL, CURRENCIES, EMAIL_SENDER,
    EMAIL_PASSWORD, CONFIG_FILE, NOTIFICATION_FILE
)
from ecolines import Ui_mainWindow
from parser import Parser


class UIHandlers:
    @staticmethod
    def search_button_handler(app: Any) -> None:
        if app.timer_started:
            app.timer.stop()
            app.timer_started = False
            app.ui.searchButton.setText('Search')
            HandlerService.set_ui_enabled(ui=app.ui, enabled=True)
        else:
            HandlerService.save_values(ui=app.ui)
            app.ui.textEdit.clear()
            from_city, to_city, date, after_time, before_time, currency = HandlerService.get_search_values(ui=app.ui)
            results = Parser.parse(
                from_city=from_city,
                to_city=to_city,
                date=date,
                after_time=after_time,
                before_time=before_time,
                currency=currency
            )
            HandlerService.show_results(app=app, results=results)
            matches = list(filter(lambda result: result.get('match') is True, results))
            if matches:
                HandlerService.notify(
                    sound_notification=app.ui.soundCheckBox.isChecked(),
                    email_notification=app.ui.emailCheckBox.isChecked(),
                    app=app,
                    filename=NOTIFICATION_FILE,
                    email=app.ui.emailLineEdit.text(),
                    matches=matches,
                )
            else:
                HandlerService.set_ui_enabled(ui=app.ui, enabled=False)
                interval = app.ui.spinBox.value() * 1000
                app.ui.searchButton.setText('Stop')
                HandlerService.set_timer(app=app, interval=interval)
                app.timer_started = True

    @staticmethod
    def email_checkbox_handler(app: Any):
        app.ui.emailLineEdit.setEnabled(app.ui.emailCheckBox.isChecked())


class HandlerService:
    @staticmethod
    def set_timer(app: Any, interval: int) -> None:
        app.timer = QTimer()
        app.timer.setInterval(interval)
        app.timer.timeout.connect(lambda: HandlerService.recurring_timer(app=app))
        app.timer.start()

    @staticmethod
    def recurring_timer(app: Any) -> None:
        results = Parser.parse(*HandlerService.get_search_values(ui=app.ui))
        HandlerService.show_results(app=app, results=results)

        matches = list(filter(lambda result: result.get('match') is True, results))
        if matches and app.timer_started:
            app.timer.stop()
            app.timer_started = False
            app.ui.searchButton.setText('Search')
            HandlerService.set_ui_enabled(ui=app.ui, enabled=True)

            HandlerService.notify(
                sound_notification=app.ui.soundCheckBox.isChecked(),
                email_notification=app.ui.emailCheckBox.isChecked(),
                app=app,
                filename=NOTIFICATION_FILE,
                email=app.ui.emailLineEdit.text(),
                matches=matches,
            )

    @staticmethod
    def show_results(app: Any, results: list) -> None:
        app.ui.textEdit.append(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}')

        for result in results:
            emoji = "\U00002714" if result.get("match") else "\U0000274C"
            info = f'{result.get("departure_city")} -> {result.get("arrival_city")}: ' \
                   f'{result.get("departure_date")} {result.get("departure_time")} - ' \
                   f'{result.get("arrival_date")} {result.get("arrival_time")}' \
                   f' | {result.get("status") if result.get("is_free") else "SOLD OUT"}   ' + emoji
            app.ui.textEdit.append(info)

        app.ui.textEdit.append('\n')

    @staticmethod
    def get_search_values(ui: Ui_mainWindow) -> Tuple[str, str, datetime.date, datetime.time, datetime.time, str]:

        from_city, to_city, date, after_time, before_time, currency = (
            ui.fromComboBox.currentText(),
            ui.toComboBox.currentText(),
            ui.dateEdit.date().toPyDate(),
            ui.afterTimeEdit.time().toPyTime(),
            ui.beforeTimeEdit.time().toPyTime(),
            ui.currencyComboBox.currentText()
        )

        return from_city, to_city, date, after_time, before_time, currency

    @staticmethod
    def set_ui_enabled(ui: Ui_mainWindow, enabled: bool = True):
        ui.afterTimeEdit.setEnabled(enabled)
        ui.beforeTimeEdit.setEnabled(enabled)
        ui.dateEdit.setEnabled(enabled)
        ui.fromComboBox.setEnabled(enabled)
        ui.toComboBox.setEnabled(enabled)
        ui.currencyComboBox.setEnabled(enabled)
        ui.spinBox.setEnabled(enabled)
        ui.emailCheckBox.setEnabled(enabled)
        ui.soundCheckBox.setEnabled(enabled)
        ui.emailLineEdit.setEnabled(enabled and ui.emailCheckBox.isChecked())

    @staticmethod
    def notify(
            sound_notification: bool,
            email_notification: bool,
            app: Any,
            filename: str,
            email: str,
            matches: list[dict],
    ):
        if sound_notification:
            HandlerService.play_sound(filename=filename)

        if email_notification:
            from_city, to_city, date, after_time, before_time, currency = HandlerService.get_search_values(ui=app.ui)
            from_city_key, to_city_key, currency_key = (
                CITIES.get(from_city),
                CITIES.get(to_city),
                CURRENCIES.get(currency)
            )
            url = BUY_URL.format(
                from_city_key=from_city_key,
                to_city_key=to_city_key,
                date=str(date),
                currency_key=currency_key
            )
            HandlerService.send_email(
                email=email,
                matches=matches,
                url=url
            )

        dialog = CustomDialog(matches=matches, search_values=HandlerService.get_search_values(ui=app.ui))
        dialog.exec()

    @staticmethod
    def play_sound(filename: str):
        filename = os.path.join(CURRENT_DIR, filename)
        QtMultimedia.QSound.play(filename)

    @staticmethod
    def send_email(email: str, matches: list[dict], url: str):
        receivers = [email]
        mail_content = ''

        for match in matches:
            emoji = "\U00002714" if match.get("match") else "\U0000274C"
            info = f'{match.get("departure_city")} -> {match.get("arrival_city")}: ' \
                   f'{match.get("departure_date")} {match.get("departure_time")} - ' \
                   f'{match.get("arrival_date")} {match.get("arrival_time")}' \
                   f' | {match.get("status") if match.get("is_free") else "SOLD OUT"}   ' + emoji + '\n'
            mail_content += info
        mail_content += f'\nBuy ticket here -> {url}'

        try:
            message = MIMEMultipart()
            message['From'] = EMAIL_SENDER
            message['Subject'] = 'Ecolines ticket found!'
            message.attach(MIMEText(mail_content, 'plain'))

            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(EMAIL_SENDER, EMAIL_PASSWORD)
            session.sendmail(EMAIL_SENDER, receivers, message.as_string())
            session.quit()
        except:
            pass

    @staticmethod
    def save_values(ui: Ui_mainWindow):
        values = {
            'date': ui.dateEdit.text(),
            'after_time': ui.afterTimeEdit.text(),
            'before_time': ui.beforeTimeEdit.text(),
            'from_city': ui.fromComboBox.currentText(),
            'to_city': ui.toComboBox.currentText(),
            'currency': ui.currencyComboBox.currentText(),
            'interval': ui.spinBox.value(),
            'sound': ui.emailCheckBox.isChecked(),
            'email': ui.emailLineEdit.text()
        }

        json_object = json.dumps(values, indent=4)

        with open(CONFIG_FILE, "w") as outfile:
            outfile.write(json_object)
