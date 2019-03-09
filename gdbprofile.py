#!/usr/local/bin/python2.7
from __future__ import print_function, unicode_literals

import gdb
import re


def backtrace():
    """ Generates stack frames until none is available """
    frame = gdb.newest_frame()

    while frame is not None:
        yield frame
        frame = frame.older()


traces = {}


def write_profile(fname):
    presort = []

    # Sort trace
    for key, count in traces.items():
        presort.append((count, key))

    with open(fname, 'w') as fh:
        for callcount, trace in reversed(sorted(presort, key=lambda x: x[0])):
            res = []
            for frame in trace:
                res.append(str(frame))
            res = reversed(res)
            print(";".join(res), callcount, file=fh)


def collect_trace(event):
    if event.stop_signal != "SIGEMT":
        print("Ignoring", event.stop_signal)
        return

    print("Collecting frames")

    trace = []
    for f in backtrace():
        name = str(f.name())
        trace.append(re.sub(r'::h[0-9a-f]+$', r'', name))
    trace = tuple(trace)

    if trace not in traces:
        traces[trace] = 0
    traces[trace] += 1

    write_profile('trace.txt')
    gdb.execute('continue')
    gdb.execute('continue')


gdb.events.stop.connect(collect_trace)

gdb.execute("handle SIGEMT nopass")  # Hijack SIGEMT for profiling
gdb.execute("set pagination 0")

print("Profiler set up, sending SIGEMT to the process collects a stack frame")
