import cProfile
import json
import marshal
import pprint
import pstats
import StringIO
import sys
import tempfile
import time

import config
import stats

class Result(object):
    def __init__(self):
        self.name = None
        self.time = None
        self.time_diff_percentage = None
        self.exception = None
        self.top_calls_total_time = None

    def get_data(self):
        data = {
            'name': self.name,
            'time': self.time,
            'exception': self.exception,
            'time_diff_percentage': self.time_diff_percentage}
        if self.top_calls_total_time:
            data['top_calls_total_time'] = [
                {'name': e.name, 'percentage': e.total_time_percentage}
                    for e in self.top_calls_total_time]
        return data

    def __str__(self):
        return 'Result: name: %s, time: %.2f, exception: %s, ' \
               'top_calls_total_time: %.2f' % (
               self.name,
               self.time,
               self.exception,
               self.top_calls_total_time)


def get_result_from_name(name, results):
    for result in results:
        if result.name == name:
            return result


def read_last_results():
    try:
        with open('last') as f:
            last = json.loads(f.read())
        last_results = []
        for result in last:
            last_result = Result()
            last_result.name = result['name']
            last_result.time = result['time']
            last_result.time_diff_percentage = result['time_diff_percentage']
            last_result.exception = result['exception']
            last_result.top_calls_total_time = result['top_calls_total_time']
            last_results.append(last_result)

    except Exception as e:
        last_results = []

    return last_results


def profile(config_file):
    entries = config.parse_config(config_file)
    last_results = read_last_results()

    results = []
    for entry in entries:
        result = Result()
        result.name = entry.name
        last_result = get_result_from_name(result.name, last_results)
        if last_result:
            last_result_time = last_result.time
        else:
            last_result_time = None

        try:
            st = time.time()
            for _ in range(entry.rounds):
                entry.call(*(entry.args[0]), **(entry.args[1]))
            result.time = (time.time() - st) * 1000. / entry.rounds
            if last_result_time:
                result.time_diff_percentage = 100 * (
                    result.time - last_result_time) / last_result_time
            pr = cProfile.Profile()
            pr.enable()
            for _ in range(entry.rounds):
                entry.call(*(entry.args[0]), **(entry.args[1]))
            pr.disable()
            ps = pstats.Stats(pr)
            stats_file = tempfile.NamedTemporaryFile()
            ps.dump_stats(stats_file.name)
            s = marshal.load(stats_file.file)
            #pprint.pprint(s)
            ps = stats.parse_stats(s)
            ps = stats.sort_stats_by_total_time(ps)
            ps_filtered = []
            for e in ps:
                if 'Profiler' not in e.name:
                    ps_filtered.append(e)
            result.top_calls_total_time = ps_filtered[:5]

        except Exception as e:
            result.exception = e
        results.append(result)

    return results


if __name__ == "__main__":
    results = profile(sys.argv[1])
    for result in results:
        pprint.pprint(result.get_data())

    with open('last', 'w') as f:
        to_write = []
        for result in results:
            if result.exception is None:
                to_write.append(result.get_data())
        f.write(json.dumps(to_write))
