from utils import get_vacancies, create_database, save_data_to_database
from config import HH_URL, params, config, db_name
from dbmanager import DBManager


def main():
    req = get_vacancies(HH_URL, params)
    par = config()
    create_database(db_name, par)
    save_data_to_database(db_name, par, req)

    info = DBManager('hh_info2', par)
    print("1 - получить список всех компаний и количество вакансий у каждой компании")
    print("2 - получить список всех вакансий с указанием названия компании, "
          "названия вакансии и зарплаты и ссылки на вакансию")
    print("3 - получить среднюю зарплату по вакансиям")
    print("4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
    print("5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова")
    print("6 - получить все списки")
    print("0 - выйти")
    answer = int(input("Какая информация вам интересна, введите цифру -> "))
    if answer == 1:
        info.get_companies_and_vacancies_count()
    elif answer == 2:
        info.get_all_vacancies()
    elif answer == 3:
        info.get_avg_salary()
    elif answer == 4:
        info.get_vacancies_with_higher_salary()
    elif answer == 5:
        keyword = input("Введите ключевое слово для поиска: ").lower()
        info.get_vacancies_with_keyword(keyword)
    elif answer == 6:
        keyword = input("Введите ключевое слово для поиска: ").lower()
        info.get_companies_and_vacancies_count()
        info.get_all_vacancies()
        info.get_avg_salary()
        info.get_vacancies_with_higher_salary()
        info.get_vacancies_with_keyword(keyword)
    elif answer == 0:
        print("Всего доброго!")
    info.conn.close()


if __name__ == '__main__':
    main()
