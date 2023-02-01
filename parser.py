import datetime
import requests

from bs4 import BeautifulSoup

from constants import CITIES, SEARCH_URL, CURRENCIES


class Parser:
    @classmethod
    def parse(
            cls,
            from_city: str,
            to_city: str,
            date: datetime.date,
            after_time: datetime.time,
            before_time: datetime.time,
            currency: str
    ):
        from_city_key, to_city_key, currency_key = CITIES.get(from_city), CITIES.get(to_city), CURRENCIES.get(currency)

        url = SEARCH_URL.format(
            from_city_key=from_city_key,
            to_city_key=to_city_key,
            date=str(date),
            currency_key=currency_key
        )

        response = requests.get(url=url)

        if response.ok:
            results = cls.process_html(text=response.text)
            validated_results = cls.validate_results(results=results, after_time=after_time, before_time=before_time)

            return validated_results

    @staticmethod
    def process_html(text: str) -> list[dict]:
        results = []

        soup = BeautifulSoup(text, "html.parser")
        lis = soup.find_all('li')

        for li in lis:
            h2_list = li.find_all('h2')
            p_list = li.find_all('p', {'class': 'hidden-xs hidden-sm'})
            if h2_list and p_list:
                departure_time, arrival_time = h2_list[0].text.strip(), h2_list[1].text.strip()
                departure_date, arrival_date = p_list[0].span.text, p_list[1].span.text
                departure_city, arrival_city = (
                    p_list[0].find_all(text=True, recursive=False)[2].strip(),
                    p_list[1].find_all(text=True, recursive=False)[2].strip()
                )
                status = li.button.text.strip()
                is_free = not bool(li.button.get("disabled"))

                results.append({
                    'departure_time': departure_time, 'arrival_time': arrival_time,
                    'departure_date': departure_date, 'arrival_date': arrival_date,
                    'departure_city': departure_city, 'arrival_city': arrival_city,
                    'status': status, 'is_free': is_free
                })

                # info = f'{departure_city} -> {arrival_city}: ' \
                #        f'{departure_date} {departure_time} - {arrival_date} {arrival_time}' \
                #        f' | {status if is_free else "SOLD OUT"}'
                #
                # print(info)

        return results

    @classmethod
    def validate_results(cls, results: list[dict], after_time: datetime.time, before_time: datetime.time) -> list[dict]:
        for result in results:
            hour, minute = result.get('departure_time').split(':')
            result['match'] = all([
                datetime.time(hour=int(hour), minute=int(minute)) < before_time,
                datetime.time(hour=int(hour), minute=int(minute)) > after_time,
                result.get('is_free')
            ])

        return results
