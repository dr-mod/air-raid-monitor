from collections import defaultdict


class StateHolder:
    def __init__(self):
        places = ('Чернігівська_область', 'Рівненська_область', 'м_Кривий_Ріг_та_Криворізька_територіальна_громада',
                  'Одеська_область', 'Київська_область', 'Кіровоградська_область', 'Первомайська_територіальна_громада',
                  'Краматорський_район', 'Сумська_область', 'Тернопільська_область', 'Волинська_область',
                  'м_Вознесенськ_та_Вознесенська_територіальна_громада', 'Великоновосілківська_територіальна_громада',
                  'Полтавська_область', 'м_Миколаїв_та_Миколаївська_територіальна_громада',
                  'Арбузинська_територіальна_громада', 'м_Київ', 'Львівська_область',
                  'Святогірська_територіальна_громада', 'Запорізька_область', 'Харківська_область',
                  'Дніпропетровська_область', 'Хмельницька_область', 'Миколаївська_область',
                  'м_Баштанка_та_Баштанська_територіальна_громада', 'Закарпатська_область', 'ІваноФранківська_область',
                  'Житомирська_область', 'Первомайський_район', 'Черкаська_область', 'Вінницька_область',
                  'Донецька_область', 'Чернівецька_область', 'Херсонська_область', 'Херсон', 'Синельниківський_район',
                  'Ізюмський_район', 'Луганська_область')
        self.state = defaultdict(lambda: False)
        for place in places:
            place = place.lower().strip()
            self.state[place] = False
        self.state['Луганська_область'.lower().strip()] = True

    def alarm_on(self, place):
        place = place.lower().strip()
        self.state[place] = True

    def alarm_off(self, place):
        place = place.lower().strip()
        self.state[place] = False

    def generate(self) -> {}:
        result = {}
        result["Mykolayiv"] = self.full_or_part('Миколаївська_область', ['Первомайська_територіальна_громада',
                                                                         'м_Вознесенськ_та_Вознесенська_територіальна_громада',
                                                                         'м_Миколаїв_та_Миколаївська_територіальна_громада',
                                                                         'Арбузинська_територіальна_громада',
                                                                         'м_Баштанка_та_Баштанська_територіальна_громада',
                                                                         'Первомайський_район'])
        result["Chernihiv"] = self.full_or_part('Чернігівська_область')
        result["Rivne"] = self.full_or_part('Рівненська_область')
        result["Chernivtsi"] = self.full_or_part('Чернівецька_область')
        result["Ivano-Frankivs'k"] = self.full_or_part('ІваноФранківська_область')
        result["Khmel'nyts'kyy"] = self.full_or_part('Хмельницька_область')
        result["L'viv"] = self.full_or_part('Львівська_область')
        result["Ternopil'"] = self.full_or_part('Тернопільська_область')
        result["Transcarpathia"] = self.full_or_part('Закарпатська_область')
        result["Volyn"] = self.full_or_part('Волинська_область')
        result["Cherkasy"] = self.full_or_part('Черкаська_область')
        result["Kirovohrad"] = self.full_or_part('Кіровоградська_область')
        result["Kiev"] = self.full_or_part('Київська_область')
        result["Odessa"] = self.full_or_part('Одеська_область')
        result["Vinnytsya"] = self.full_or_part('Вінницька_область')
        result["Zhytomyr"] = self.full_or_part('Житомирська_область')
        result["Sumy"] = self.full_or_part('Сумська_область')
        result["Dnipropetrovs'k"] = self.full_or_part('Дніпропетровська_область',
                                                      ['м_Кривий_Ріг_та_Криворізька_територіальна_громада',
                                                       'Синельниківський_район'])
        result["Donets'k"] = self.full_or_part('Донецька_область',
                                               ['Краматорський_район', 'Великоновосілківська_територіальна_громада',
                                                'Святогірська_територіальна_громада'])
        result["Kharkiv"] = self.full_or_part('Харківська_область', ['Ізюмський_район'])
        result["Poltava"] = self.full_or_part('Полтавська_область')
        result["Zaporizhzhya"] = self.full_or_part('Запорізька_область')
        result["Kiev City"] = self.full_or_part('м_Київ')
        result["Kherson"] = self.full_or_part('Херсонська_область', ['Херсон'])
        result["Luhans'k"] = self.full_or_part('Луганська_область')
        result["Sevastopol"] = "occupied"
        result["Crimea"] = "occupied"
        return result

    def full_or_part(self, district="", cities=[]):
        if self.state[district.lower()]:
            return "full"
        for city in cities:
            if self.state[city.lower()]:
                return "partial"
        return None
