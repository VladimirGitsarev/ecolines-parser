import datetime

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QCommandLinkButton

from constants import CITIES, BUY_URL, CURRENCIES


class CustomDialog(QDialog):
    def __init__(self, matches: list, search_values: tuple):
        super().__init__()

        self.setWindowTitle("Ticket found!")

        from_city, to_city, date, _, _, currency = search_values

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()

        for match in matches:
            emoji = "\U00002714" if match.get("match") else "\U0000274C"
            info = f'{match.get("departure_city")} -> {match.get("arrival_city")}: ' \
                   f'{match.get("departure_date")} {match.get("departure_time")} - ' \
                   f'{match.get("arrival_date")} {match.get("arrival_time")}' \
                   f' | {match.get("status") if match.get("is_free") else "SOLD OUT"}   ' + emoji
            details = QLabel(info)
            self.layout.addWidget(details)

        self.link_button = QCommandLinkButton('Open ecolines.net to buy ticket')
        self.layout.addWidget(self.link_button)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.link_button.clicked.connect(
            lambda: self.open_link(from_city=from_city, to_city=to_city, date=date, currency=currency)
        )

    def open_link(self, from_city: str, to_city: str, date: datetime.date, currency: str):
        from_city_key, to_city_key, currency_key = CITIES.get(from_city), CITIES.get(to_city), CURRENCIES.get(currency)
        url = BUY_URL.format(
            from_city_key=from_city_key,
            to_city_key=to_city_key,
            date=str(date),
            currency_key=currency_key
        )
        url_link = QUrl(url)
        QDesktopServices.openUrl(url_link)
