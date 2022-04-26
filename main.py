import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from eink import Eink
from observer import Observable


def get_state():
    req = Request('https://sirens.in.ua/api/v1/')
    data = urlopen(req).read()
    return json.loads(data)


def main():
    observable = Observable()
    Eink(observable)
    prev_state = {}
    try:
        main_cycle(observable, prev_state)
    except IOError as e:
        print(str(e))
    except KeyboardInterrupt:
        observable.close()


def main_cycle(observable, prev_state):
    while True:
        try:
            curr_state = get_state()
            if curr_state != prev_state:
                prev_state = curr_state
                observable.update_observers(curr_state)
            time.sleep(10)
        except (HTTPError, URLError) as e:
            print(str(e))
            time.sleep(5)


if __name__ == "__main__":
    main()
