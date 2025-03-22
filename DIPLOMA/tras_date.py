from datetime import datetime
import re

# метод для обробки дат
def process_date(date_str: str):
    """
    обробка дати, приведення до потрібного формату

    :param date_str: Str, дата для обробки
    :return: str формату "dd.mm.yyyy" або None
    """

    if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_str):
        return date_str
    # "yyyy-mm-dd"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        pass
    # "dd mm yyyy"
    if re.match(r'^\d{1,2} \d{1,2} \d{4}$', date_str):
        try:
            return datetime.strptime(date_str, "%d %m %Y").strftime("%d.%m.%Y")
        except ValueError:
            return None
    # "dd/mm/yyyy"
    if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%d.%m.%Y")
        except ValueError:
            return None
    # "d-m-yyyy"
    if re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', date_str):
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%d.%m.%Y")
        except ValueError:
            return None

    return None