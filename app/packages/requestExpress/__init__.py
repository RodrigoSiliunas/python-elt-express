import requests


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

    def get_template_from_date(self, start_date: str, end_date: str) -> requests.Response:
        data = {
            "search": {
                "freights": {
                    "service_at": f"{start_date} - {end_date}"
                }
            }
        }

        response = requests.get(
            f'{self.base_url}/api/analytics/reports/929/data', json=data, headers=self.headers)

        return response
