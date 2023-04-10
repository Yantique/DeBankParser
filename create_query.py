from datetime import date, timedelta

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
    with open('query.sql', 'w') as f:
        f.write('SELECT *, "quantity" * "price" as "total"\n')
        f.write('FROM (\n')
        f.write('    WITH token_prices AS (\n')
        f.write('        SELECT "median_price", "contract_address"\n')
        f.write('        FROM (\n')
        f.write('            SELECT "median_price", "contract_address", row_number() OVER (PARTITION BY "contract_address")\n')
        f.write('            FROM dex."view_token_prices"\n')
        f.write(f"            WHERE \"hour\" between '{start_date}' AND '{end_date}') AS raw_data\n")
        f.write('        WHERE row_number = 1)\n')
        f.write('    SELECT DISTINCT "token_address", "token_symbol", SUM("amount") OVER (PARTITION BY "token_address") AS quantity, "median_price" AS price\n')
        f.write('    FROM erc20."view_token_balances_daily"\n')
        f.write('    JOIN token_prices ON token_prices."contract_address" = erc20."view_token_balances_daily"."token_address"\n')
        with open('result.csv') as g:
            g.readline()
            wallet_address = "\\" + g.readline().split(',')[0][1:]
            f.write(f"    WHERE (\"wallet_address\" = '{wallet_address}'")
            for line in g:
                wallet_address = "\\" + line.split(',')[0][1:]
                f.write(f" OR\n           \"wallet_address\" = '{wallet_address}'")
            f.write(f") AND \"amount\" > 0 AND \"day\" = '{start_date} 00:00') AS data\n")
        f.write('ORDER BY "total" DESC')
    print('Query Created')


if __name__ == '__main__':
    create_query(input("Enter date: "))
