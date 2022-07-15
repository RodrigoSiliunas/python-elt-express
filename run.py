from app import *
from datetime import datetime as date, timedelta


if __name__ == "__main__":
    today = datetime.today().strftime("%A")

    if ((today == 'Saturday') or (today == 'Sunday')):
        from_date = date.today() - timedelta(days=30)
        from_date = f'{from_date.day:02d}/{from_date.month:02d}/{from_date.year}'
        to_date = f'{date.today().day:02d}/{datetime.now().month:02d}/{datetime.now().year}'
    else:
        from_date = date.today() - timedelta(days=5)
        from_date = f'{from_date.day:02d}/{from_date.month:02d}/{from_date.year}'
        to_date = f'{date.today().day:02d}/{datetime.now().month:02d}/{datetime.now().year}'

    insert_from_data_to_data(from_date, to_date)
