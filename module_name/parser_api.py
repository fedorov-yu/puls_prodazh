import itertools
import threading
import time
from datetime import datetime
import requests
import logging
from fake_useragent import UserAgent

logging.getLogger('name').setLevel(logging.WARNING)
logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO,
)


def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return execute


@thread
def get_datas(api_addr: str, posts: int = 10):
    """get data from api_addr"""
    data = []
    ua = UserAgent()
    headers = {
        'Accept': 'application/json',
        'User-Agent': ua.random,
    }
    count_of_req = 0
    logging.info(f'STARTED {datetime.now().time()}')
    for j, url in enumerate(itertools.cycle(api_addr), start=1):
        if j == posts + 1:
            logging.info(f'RECEIVED {datetime.now().time()}')
            print(data)
            return

        if count_of_req == 60:
            logging.info("I'm sleeping")
            count_of_req = 0
            time.sleep(60)

        try:
            response = requests.get(url + str(j), headers=headers)
            count_of_req += 1
            print(f'COUNT OF REQUESTS ====> {count_of_req}')
            response.raise_for_status()
            print('STATUS='+str(response.status_code), url + str(j))
            data.append(response.json())

        except requests.exceptions.RequestException as e:
            logging.error(f'STOPPED {e}')
            print(data)
            return


if __name__ == "__main__":
    get_datas()
