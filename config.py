from configparser import ConfigParser

HH_URL = "https://api.hh.ru/vacancies"
db_name = 'hh_data'
params = {
    'employer_id': ['856498',
                    '238161',
                    '42600',
                    '1993194',
                    '1009',
                    '61166',
                    '8884',
                    '231166',
                    '3778',
                    '4801531'
                    ],
    'page': 0,
    'per_page': 100
}


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
