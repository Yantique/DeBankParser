SELECT DISTINCT "token_address", "token_symbol", "quantity", "price", SUM(dr) OVER (PARTITION BY "token_address") as "wallets", "total"
FROM (
SELECT *, "quantity" * "price" as "total",
    CASE
    WHEN
        "amount" / "quantity" > 0.0001 THEN 1
    ELSE 0
    END AS dr
FROM (
    WITH token_prices AS (
        SELECT "median_price", "contract_address"
        FROM (
            SELECT "median_price", "contract_address", row_number() OVER (PARTITION BY "contract_address")
            FROM dex."view_token_prices"
            WHERE "hour" between '{{ start_date }}' AND '{{ end_date }}') AS raw_data
        WHERE row_number = 1)
    SELECT "token_address", "token_symbol", "amount", SUM("amount") OVER (PARTITION BY "token_address") AS quantity, "median_price" AS price
    FROM erc20."view_token_balances_daily"
    JOIN token_prices ON token_prices."contract_address" = erc20."view_token_balances_daily"."token_address"
    WHERE ({% for wallet in wallets %}"wallet_address" = '{{ wallet }}' OR
           {% endfor %}"wallet_address" = '{{ wallets[-1] }}') AND "amount" > 0 AND "day" = '{{ start_date }} 00:00') AS data
) as prep
ORDER BY "total" DESC