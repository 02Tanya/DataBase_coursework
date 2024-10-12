import requests
from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    '''Абстрактный класс для обеспечения получения вакансий с сайта с использованием API'''

    def __init__(self, url_get, count_vacancies=5):
        self._url_get = url_get
        self._count_vacancies = count_vacancies

    @abstractmethod
    def get_vacancies(self, vacancy_title):
        pass


class HHVacancyAPI(VacancyAPI):
    '''Класс для получения вакнсий с сайта hh.ru'''

    url_get = "https://api.hh.ru/vacancies"

    def __init__(self, url=url_get):
        super().__init__(url)


    def get_vacancies(self, vacancy_title) -> list:
        # def get_vacancies(self, vacancy_employer) -> list:
        params = {"text": vacancy_title, "per_page": self._count_vacancies}
        try:
            response = requests.get(self.url_get, params=params)
            response.raise_for_status()
            response_json = response.json()
            # print(response.status_code)
            return response_json.get("items", [])
        except requests.exceptions.RequestException as error:
            print(f"Ошибка получения данных: {error}")

if __name__ == '__main__':
    find = HHVacancyAPI()
    vacancies = find.get_vacancies('python')
    print(vacancies)