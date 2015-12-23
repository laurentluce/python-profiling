"""Profiling stats.
"""


class Stat(object):
    def __init__(self):
        self.filename = None
        self.line_number = None
        self.name = None
        self.calls = None
        self.non_recursive_calls = None
        self.total_time = None
        self.total_time_percentage = None
        self.cumulative_time = None
        self.sub_calls = []

    def get_data(self):
        return {
            'filename': self.filename,
            'line_number': self.line_number,
            'name': self.name,
            'calls': self.calls,
            'non_recursive_calls': self.non_recursive_calls,
            'total_time': self.total_time,
            'total_time_percentage': self.total_time_percentage,
            'cumulative_time': self.cumulative_time,
            'sub_calls': self.sub_calls}

    def __str__(self):
        return 'Stat: filename: %s, line_number: %d, name: %s, calls: %d, ' \
               'non_recursive_calls: %d, total_time: %f, ' \
               'total_time_percentage: %f, cumulative_time: %f' % (
                   self.filename,
                   self.line_number,
                   self.name,
                   self.calls,
                   self.non_recursive_calls,
                   self.total_time,
                   self.total_time_percentage,
                   self.cumulative_time)


def parse_stats(stats):
    res = []
    total_time = 0
    for k, v in stats.iteritems():
        stat = Stat()
        stat.filename = k[0]
        stat.line_number = k[1]
        stat.name = k[2]
        stat.calls = v[0]
        stat.non_recursive_calls = v[1]
        stat.total_time = v[2]
        if stat.total_time > total_time:
            total_time = stat.total_time
        stat.cumulative_time = v[3]
        if len(v) == 5 and v[4]:
            stat.sub_calls = parse_stats(v[4])
        res.append(stat)

    for stat in res:
        stat.total_time_percentage = 100 * (stat.total_time / total_time)

    return res


def sort_stats_by_total_time(stats):
    return sorted(stats, key=lambda stat: stat.total_time, reverse=True)
