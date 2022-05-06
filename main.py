import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from eink import Eink
from observer import Observable


def get_state():
    with urlopen('https://sirens.in.ua/api/v1/', timeout=10) as response:
        data = response.read()
        return json.loads(data)
    return None


def main():
    observable = Observable()
    Eink(observable)
    try:
        main_cycle(observable)
    except IOError as e:
        print("IOError: "+str(e))
    except KeyboardInterrupt:
        observable.close()


def main_cycle(observable):
    curr_state = {}
    prev_state = {}
    timeout_count = 0
    while True:
        try:
            curr_state = get_state()
            timeout_count = 0
        except (HTTPError, URLError) as e:
            print("HTTP,URL Error: "+str(e))
            timeout_count += 1
        finally:
            if timeout_count >= 3:
                curr_state = None
            if curr_state != prev_state:
                prev_state = curr_state
                observable.update_observers(curr_state)
            time.sleep(10)


if __name__ == "__main__":
    main()
