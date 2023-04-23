#!/usr/bin/env python3
import subprocess
import sys
import re
import os


def main():
    if len(sys.argv) < 2:
        tool = os.path.basename(sys.argv[0])
        print('Usage: {} </path/to/test_koyotecoin> [<subtest>]'.format(tool))
        print('For example: {} src/test/test_koyotecoin wallet_tests'.format(tool))
        exit(1)
    test_koyotecoin = sys.argv[1]
    args = [test_koyotecoin, '--log_level=test_suite']
    if len(sys.argv) > 2:
        args += ['--run_test=' + sys.argv[2]]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    results = []
    for line in p.stdout:
        if not line:
            break
        line = line.decode()
        m = re.match('.*Leaving test case "(.*)".*: ([0-9]+)(us|mks|ms)', line)
        if m:
            if m.group(3) == 'ms':
                elapsed = int(m.group(2)) * 1000
            else:
                elapsed = int(m.group(2))
            results.append((m.group(1), elapsed))
        sys.stderr.write('.')
        sys.stderr.flush()
    sys.stderr.write('\n')
    sys.stderr.flush()
    rv = p.wait()

    if rv == 0:
        print('| {:<55} | {:^9} |'.format('Test', 'Time (μs)'))
        print('| {} | {}:|'.format('-'*55, '-'*9))
        results.sort(key=lambda a: -a[1])
        for a in results:
            print('| {:<55} | {:>9} |'.format('`'+a[0]+'`', a[1]))


if __name__ == '__main__':
    main()
