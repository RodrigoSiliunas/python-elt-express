from concurrent.futures import ProcessPoolExecutor
import requests

import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor as Executor


class RequestExpress:
    def __init__(self, bearer_token: str) -> None:
        self.base_url = 'https://viaexpressa.eslcloud.com.br'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        }

    def get_templates(self) -> requests.Response:
        response = requests.get(
            f'{self.base_url}/api/analytics/reports', headers=self.headers)

        return response

    def get_template_info(self, id: str | int) -> requests.Response:
        response = requests.get(
            f'{self.base_url}/api/analytics/reports/{id}/info', headers=self.headers)

        return response

    def get_template_from_date(self, date: str):
        data = {
            "search": {
                "freights": {
                    "service_at": f"{date} - {date}"
                }
            },
            "page": 1,
            "per": 100
        }

        response_arr = []

        response = requests.get(
            f'{self.base_url}/api/analytics/reports/929/data', json=data, headers=self.headers).json()

        while (len(response) != 0):
            for object in response:
                response_arr.append(object)

            response = requests.get(
                f'{self.base_url}/api/analytics/reports/929/data', json=data, headers=self.headers).json()
            data['page'] += 1

        return response_arr


    def get_template_from_date_to_date(self, from_date: str, to_date: str) -> requests.Response:
        response_arr = []

        data = {
            "search": {
                "freights": {
                    "service_at": f"{from_date} - {to_date}"
                }
            },
            "page": 1,
            "per": 100
        }

        response = requests.get(
            f'{self.base_url}/api/analytics/reports/929/data', json=data, headers=self.headers).json()

        while (len(response) != 0):
            for object in response:
                response_arr.append(object)

            response = requests.get(
                f'{self.base_url}/api/analytics/reports/929/data', json=data, headers=self.headers).json()
            data['page'] += 1

        return response_arr
