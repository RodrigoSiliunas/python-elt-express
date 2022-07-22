from app import *
from datetime import datetime as date, timedelta
import pprint


if __name__ == "__main__":
    # today = datetime.today().strftime("%A")

    # if ((today == 'Saturday') or (today == 'Sunday')):
    #     from_date = date.today() - timedelta(days=30)
    #     from_date = f'{from_date.day:02d}/{from_date.month:02d}/{from_date.year}'
    #     to_date = f'{date.today().day:02d}/{datetime.now().month:02d}/{datetime.now().year}'
    # else:
    #     from_date = date.today() - timedelta(days=5)
    #     from_date = f'{from_date.day:02d}/{from_date.month:02d}/{from_date.year}'
    #     to_date = f'{date.today().day:02d}/{datetime.now().month:02d}/{datetime.now().year}'

    # init_db()
    # insert_all_data_without_email()
    insert_from_date('20/04/2022')
    # insert_from_date('03/01/2022')

    # request = RequestExpress('qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw')
    # data = request.get_template_from_date('30/06/2022')

    # print(data)

    # print(f'Há um total de: {len(data)}')