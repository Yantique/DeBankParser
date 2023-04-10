from datetime import date, timedelta
from jinja2 import Template

import re


def valid_date_format(given_date):
    while True:
        if re.match(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', given_date):
            given_date = date(*list(map(int, given_date.split('-'))))
            return given_date
        else:
            given_date = input("Wrong format! Date format is 'yyyy-mm-dd'.\nEnter date: ")


def create_query(start_date):
    start_date = valid_date_format(start_date)
    end_date = start_date + timedelta(days=7)
    with open('query_template.sql', 'r') as f:
        data = ''.join(f.readlines())
    template = Template(data)
    with open('result.csv', 'r') as f:
        f.readline()
        wallets = []
        for line in f:
            wallets.append("\\" + line.split(',')[0][1:])
    query = template.render(start_date=start_date, end_date=end_date, wallets=wallets)
    with open('query.sql', 'w') as f:
        f.write(query)
    print('Query Created')


if __name__ == '__main__':
    create_query(input("Enter date (yyyy-mm-dd): "))
