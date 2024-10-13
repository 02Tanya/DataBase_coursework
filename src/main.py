import psycopg2
from time import sleep

from config import config
from class_DBManager import DBManager
from utils import (
    get_info_about_employers, get_vacancies, create_database,
    create_employers_table, create_vacancies_table,
    insert_data
)

list_employers_id = [49357, 87021, 3529, 2180, 1942330, 3148, 2748, 3776, 4934, 1122462]


def main():
    employers = get_info_about_employers(list_employers_id)

    vacancies = {}
    key = 1
    for employer_id in list_employers_id:
        vacancies[key] = get_vacancies(employer_id)
        key += 1

    params = config()
    db_name = 'my_db'
    # conn = None

    create_database(params, db_name)
    print("База данных успешно создана")
    params.update({'dbname': db_name})

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_employers_table(cur)
                print('Таблица employers создана успешно')
                create_vacancies_table(cur)
                print('Таблица vacancies создана успешно')
                insert_data(cur, employers, vacancies)
                print('Данные в таблицы добавлены успешно')
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



    while True:
        print("\u001b[36m")
        sleep(1)
        print(
            "Вы можете выбрать следующие действия:\n"
            "1 - Вывести список компаний и количество вакансий у каждой компании;\n"
            "2 - Вывести список всех вакансий;\n"
            "3 - Вывести среднюю величину заработной платы по вакансиям;\n"
            "4 - Вывести список всех вакансий, у которых зарплата выше средней;\n"
            "5 - Поиск вакансий по ключевому слову;\n"
            "6 - Выход"
        )
        print("\u001b[0m")
        user_input = input("Укажите номер выбранного Вами действия:\n")

        if user_input == "1":
            print('\nСписок компаний и количество вакансий каждой компании:')
            request_1 = DBManager(params).get_companies_and_vacancies_count()
            for row in request_1:
                print(f'{row[0]} - {row[1]}')
            continue
        elif user_input == "2":
            print('\nСписок всех вакансий:')
            request_2 = DBManager(params).get_all_vacancies()
            for row in request_2:
                print(row)
        elif user_input == "3":
            print('\nСредняя заработная плата по вакансиям:')
            request_3 = DBManager(params).get_avg_salary()
            print(request_3)
        elif user_input == "4":
            print('\nСписок всех вакансий, у которых заработная плата выше средней:')
            request_4 = DBManager(params).get_vacancies_with_higher_salary()
            for row in request_4:
                print(row[0])
        elif user_input == "5":
            keyword = input("Пожалуйста, введите ключевое слово для поиска вакансий: \n")
            if DBManager(params).get_vacancies_with_keyword(keyword):

                print(f'\nСписок всех вакансий в которых содержится "{keyword}":')
                request_5 = DBManager(params).get_vacancies_with_keyword(keyword)
                for row in request_5:
                    print(row[0])
                continue
            else:
                print("По вашему запросу ничего не найдено. Попробуйте изменить параметры запроса.")
                continue

        else:
            print("\nРабота программы завершена. Будем рады снова помочь Вам с поиском:)")
            break

    DBManager(params).closes_the_connection_to_the_database()

if __name__ == '__main__':
    print("\u001b[36m")
    print(
        "* * * Добрый день! Вас приветствует помощник в подборе вакансий * * *\n "
        "      -------------------------------------------------------\n"
        "\n       Подождите, пожалуйста, данные сейчас загрузятся :)"
    )
    print("\u001b[0m")
    main()
