import time

import requests
import json


def upload_sec_tickers_data(collection_url):
    while True:
        sec_response = requests.get('https://www.sec.gov/files/company_tickers.json')
        if sec_response.status_code == 200:
            loc_json = json.loads(sec_response.text)
            break
        else:
            time.sleep(60)
    for record in loc_json:
        data = loc_json[record]
        data['cik_str'] = str(data.get('cik_str'))
        ticker = data.get('ticker')
        response = requests.get(f'{collection_url}?ticker={ticker}')
        if response.status_code == 200:
            response_json = json.loads(response.text)
            is_in_database = False if response_json.get('total') == 0 else True
            if not is_in_database:
                requests.post(f'{collection_url}', json=data)


if __name__ == '__main__':
    url = 'http://62.216.33.167:21005/api/sec_data_tickers'
    while True:
        start_time = time.time()
        upload_sec_tickers_data(url)
        work_time = int(time.time() - start_time)
        time.sleep(abs(work_time % 14400 - 14400))
