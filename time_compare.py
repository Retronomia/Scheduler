import re

# For TimeComparison class
TIME_RE = re.compile(
    r'^((?P<mon>M)|(?P<tue>Tu)|(?P<wed>W)|(?P<thu>Th)|(?P<fri>F))+ +(?P<hstart>\d?\d):(?P<mstart>\d\d)- *(?P<hend>\d?\d):(?P<mend>\d\d)(?P<pm>p)?$')
FINAL_RE = re.compile(r'^(?P<day>.+)(?P<hstart>\d?\d):(?P<mstart>\d\d)- *(?P<hend>\d?\d):(?P<mend>\d\d)(?P<pm>pm)$')

# also someone needs needs to create fake api function in schedule api

# Class is helpful for is_valid_time
class TimeComparison:
    def __init__(self, time_str):
        match = re.match(TIME_RE, time_str)
        if match:
            self.days = set()
            if match.group('mon'):
                self.days.add('M')
            if match.group('tue'):
                self.days.add('Tu')
            if match.group('wed'):
                self.days.add('W')
            if match.group('thu'):
                self.days.add('Th')
            if match.group('fri'):
                self.days.add('F')
        if not match:
            match = re.match(FINAL_RE, time_str)
            if not match:
                raise AttributeError(f'Invalid time input: {time_str}')
            self.days = {match.group('day')}

        self.start_time = (int(match.group('hstart')), int(match.group('mstart')))
        self.end_time = (int(match.group('hend')), int(match.group('mend')))

        if match.group('pm') and self.end_time[0] != 12:
            self.end_time = self.end_time[0] + 12, self.end_time[1]
        if abs(self.end_time[0] - self.start_time[0]) > 4:
            self.start_time = self.start_time[0] + 12, self.start_time[1]

    def conflicts_with(self, other: 'TimeComparison') -> bool:
        same_days = False
        for day in self.days:
            if day in other.days:
                same_days = True

        if not same_days:
            return False

        starts_after_other_ends = False
        ends_before_other_starts = False

        if self.start_time[0] > other.end_time[0]:
            starts_after_other_ends = True
        elif self.start_time[0] == other.end_time[0] and self.start_time[1] >= other.end_time[1]:
            starts_after_other_ends = True

        if self.end_time[0] < other.start_time[0]:
            ends_before_other_starts = True
        elif self.end_time[0] == other.start_time[0] and self.end_time[1] <= other.start_time[1]:
            ends_before_other_starts = True

        return not (starts_after_other_ends or ends_before_other_starts)