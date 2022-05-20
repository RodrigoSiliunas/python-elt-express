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

        return response.json()

    def get_template_info(self, id: str | int) -> requests.Response:
        response = requests.get(
            f'{self.base_url}/api/analytics/reports/{id}/info', headers=self.headers)

        return response.json()

    def get_template_from_date(self, id: str | int, start_date: str, end_date: str) -> list:
        data = {
            "search": {
                "freights": {
                    "service_at": f"{start_date} - {end_date}"
                }
            }
        }

        response = requests.get(
            f'{self.base_url}/api/analytics/reports/{id}/data', json=data, headers=self.headers)
        data_to_return = []

        # For object in response.json.
        for index in response.json():
            # Here we get the invoices_mapping field from request and get the content and transform it into a string.
            invoices_mapping = ""

            # For data in the field invoices mapping on response.json.
            for data in index['invoices_mapping']:
                invoices_mapping += f'{data}, '

            invoices_mapping = invoices_mapping.strip()
            invoices_mapping = invoices_mapping[:-1]

            del index['invoices_mapping']

            index['invoices_mapping'] = invoices_mapping
            data_to_return.append(index)

        return data_to_return

    # def get_response_data():
    #     request = RequestExpress(
    #         'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw')
    #     response = request.get_template_from_date(413, '16/05/2022', '16/05/2022')
    #     data_to_return = []

    #     # For object in response.json.
    #     for index in response.json():
    #         # Here we get the invoices_mapping field from request and get the content and transform it into a string.
    #         invoices_mapping = ""

    #         # For data in the field invoices mapping on response.json.
    #         for data in index['invoices_mapping']:
    #             invoices_mapping += f'{data}, '

    #         invoices_mapping = invoices_mapping.strip()
    #         invoices_mapping = invoices_mapping[:-1]

    #         del index['invoices_mapping']

    #         index['invoices_mapping'] = invoices_mapping
    #         data_to_return.append(index)

    #     return data_to_return
