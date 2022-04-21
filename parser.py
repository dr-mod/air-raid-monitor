import re


class Parser:
    def __init__(self, state_holder):
        self.state_holder = state_holder

    def process_message(self, message):
        def check(message, regexp, funct):
            if re.search(regexp, message):
                for place in self.parse(message):
                    funct(place)
        check(message, r'.*Повітряна тривога.*', self.state_holder.alarm_on)
        check(message, r'.*Відбій тривоги.*', self.state_holder.alarm_off)

    def parse(self, message):
        output = re.findall(r'#[\w|_]+$', message)
        output = set([m[1:] for m in output])
        return output

