import asyncio
import json
import time

import aiohttp
import pandas as pd

# from random_proxies import Random_Proxy

# random_proxies = Random_Proxy()
start_time = time.perf_counter()


async def main(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        page_number = 1
        for page_number in range(1, 31):
            task = asyncio.create_task(
                get_data_json(session, url, page_number))   
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open('raw_data.json', 'r', encoding='utf-8') as f:
        data = f.read()
        toJson = json.loads(data)

    case_list = []

    for i in range(len(toJson)):
        for value in (toJson[i]):
            case = {'title': value['title'], 'thumbnail': value['cover'], 'status': value['index_show'], 'url': 'https://www.bilibili.tv/th/play/' +
                    str(value['season_id'])}
            case_list.append(case)

    with open('clean_data.json', 'w', encoding='utf-8') as f:
        json.dump(case_list, f, ensure_ascii=False, indent=4)

    df_json = pd.read_json('clean_data.json')
    df_json.to_excel('Aasdfnime_list.xlsx')


async def get_data_json(session, url, page_number):
    params = {'buvid': '7918C9CB-1802-8960-BAFC-7F4D0ED6A7AD52259infoc', 'csrf': '28bc8f806e9033fbcc205b7f5b2a07a4', 'order': '0',
              'page': page_number, 'pagesize': '32', 'platform': 'web', 's_locale': 'th_TH', 'season_type': '1,4', 'timezone': 'GMT%2B07'}
    headers = {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    # print('here')
    # proxy = random_proxies.random_proxy()
    case_list = []
    async with session.get(url, params=params, headers=headers) as response:
        # print('yes')
        print(response.status)
        # assert response.status == 200  # check if the page is ok
        response = await response.json()
        await asyncio.sleep(0.5)
        return response['data']['cards']


def real_main(url):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(url))
    print("--- %s seconds ---" % (time.perf_counter() - start_time))


if __name__ == "__main__":
    real_main('https://api.bilibili.tv/intl/gateway/web/v2/ogv/index/items')
