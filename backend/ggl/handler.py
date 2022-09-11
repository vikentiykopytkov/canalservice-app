from .data import get_data

import httpx
import xml.etree.ElementTree as ET


def get_handled_data():
    data = get_data()
    fiat = httpx.get('https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=04/09/2022&date_req2=11/09/2022&VAL_NM_RQ=R01235').text # Получение курса с сайта ЦБ РФ

    fiat = ET.fromstring(fiat) # Парсинг из XML данных
    current_fiat = float(fiat[-1][1].text.replace(',', '.'))

    return [(row [0], row [1], row [2], int(row [2] * current_fiat), row [3]) for row in data] # Добавлена сконвертированная в рубли стоимость