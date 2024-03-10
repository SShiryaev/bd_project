import requests
import psycopg2


def get_vacancies(url, params):
    """
    Получает вакансии со стороннего ресурса hh.ru
    :return: список вакансий в json файле
    """
    response = requests.get(url, params=params).json()
    return response


def create_database(db_name, param) -> None:
    """Создает новую базу данных для сохранения данных """
    conn = psycopg2.connect(dbname='postgres', **param)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **param)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                company_db_id SERIAL PRIMARY KEY,
                company_id INT NOT NULL,
                title VARCHAR(255) NOT NULL
                    )
                """)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_db_id SERIAL PRIMARY KEY,
                company_db_id INT REFERENCES companies(company_db_id),
                vacancy_id INT NOT NULL,
                title VARCHAR NOT NULL,
                salary_from INT,
                salary_to INT,
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()
    print(f"БД успешно создана")


def save_data_to_database(db_name: str, params: dict, req) -> None:
    """Сохранение данных в БД"""
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        companies_list = []
        for vac in req['items']:
            company_id = vac['employer']['id']
            company_name = vac['employer']['name']
            vacancy_id = vac['id']
            vacancy_name = vac['name']
            salary_from = vac['salary'].get('from') if vac['salary'] else 0
            salary_to = vac['salary'].get('to') if vac['salary'] else 0
            vacancy_url = vac['alternate_url']

            if company_id not in companies_list:
                cur.execute(
                    """
                    INSERT INTO companies (company_id, title)
                    VALUES (%s,%s)
                    RETURNING company_db_id
                    """,
                    (company_id, company_name))
                companies_list.append(company_id)
                company_db_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO vacancies (company_db_id, vacancy_id, title, salary_from, salary_to, vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (company_db_id, vacancy_id, vacancy_name.lower(), salary_from, salary_to,
                 vacancy_url)
            )

        conn.commit()
        conn.close()
        print('Данные внесены')
