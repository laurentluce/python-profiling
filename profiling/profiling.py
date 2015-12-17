import cProfile
import marshal
import pprint
import pstats
import StringIO
import tempfile
import time

import config
import stats

class Result(object):
    def __init__(self):
        self.name = None
        self.time = None
        self.exception = None
        self.calls_total_time = None


def main():
    entries = config.parse_config('cfg.txt')
    print '--- Config ---'
    for entry in entries:
        print entry.name
        print entry.call
        print entry.args
        print entry.exception

    results = []
    for entry in entries:
        result = Result()
        result.name = entry.name
        st = time.time()
        try:
            entry.call(*entry.args)
            result.time = time.time() - st

            pr = cProfile.Profile()
            pr.enable()
            entry.call(*entry.args)
            pr.disable()
            ps = pstats.Stats(pr)
            stats_file = tempfile.NamedTemporaryFile()
            ps.dump_stats(stats_file.name)
            s = marshal.load(stats_file.file)
            print s
            ps = stats.parse_stats(s)
            ps = stats.sort_stats_by_total_time(ps)
            ps_filtered = []
            for e in ps:
                if 'Profiler' not in e.name:
                    ps_filtered.append(e)
            result.calls_total_time = ps_filtered[1:4]

        except Exception as e:
            print str(e)
            result.exception = e
        results.append(result)

    print '--- Results ---'
    for result in results:
        print result.name
        print result.time
        print result.exception
        for e in result.calls_total_time:
            print e.name

main()
