from tqdm import tqdm
from create_query import create_query

import time
import json
import requests


def valid_num_pages(value):
    while True:
        try:
            value = int(value)
            if 1 < value < 1000:
                return value
            else:
                value = input('The value should be between 1 and 1000.\nEnter the number of pages: ')
        except ValueError:
            value = input('The value should be between 1 and 1000.\nEnter the number of pages: ')


def get_data(pages):
    pages = valid_num_pages(pages)
    headers = {
        'authority': 'api.debank.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
        'account': '{"random_at":1674767761,"random_id":"f765417ae995457e9f3369cd0d7461e5","user_addr":null}',
        'origin': 'https://debank.com',
        'referer': 'https://debank.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'source': 'web',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-api-nonce': 'n_dnNAOSWvzwmQiOQu52o7i0ohyaT7vnL89JvKD1tI',
        'x-api-sign': 'c5db3b1c9783a1e9e3e8f1b521ff1538c6817a51d680cd2754634cf89a24e474',
        'x-api-ts': '1677801551',
        'x-api-ver': 'v2',
    }

    with open('result.csv', 'w') as f:
        f.write('wallet,balance\n')

    for i in tqdm(range(1, pages + 1), ascii=True, desc='Progress: ', bar_format='{l_bar}{bar} Time: {elapsed}'):
        params = {
            'page_num': f'{i}',
            'page_count': '50',
        }

        response = requests.get('https://api.debank.com/social_ranking/list', params=params, headers=headers)
        results = json.loads(response.content)
        for result in results['data']['social_ranking_list']:
            with open('result.csv', 'a') as f:
                f.write(result['id'] + ',' + str(result['value_dict']['net_usd_value']) + '\n')
        time.sleep(3)

    print('Data loaded!')


if __name__ == '__main__':
    get_data(input("Enter the number of pages (1 page = 50 wallets): "))
    create_query(input("Enter date (yyyy-mm-dd): "))
