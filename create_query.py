with open('query.sql', 'w') as f:
    f.write('SELECT DISTINCT "token_address", "token_symbol", SUM("amount") OVER (PARTITION BY "token_address")\n\n')
    f.write('FROM erc20."view_token_balances_daily"\n\n')
    with open('result.csv') as g:
        g.readline()
        wallet_address = "\\" + g.readline().split(',')[0][1:]
        f.write(f"WHERE (\"wallet_address\" = '{wallet_address}'")
        for line in g:
            wallet_address = "\\" + line.split(',')[0][1:]
            f.write(f" OR\n\"wallet_address\" = '{wallet_address}'")
        f.write(") AND \"amount\" > 0 AND \"day\" = '2023-03-06 00:00'\n")
