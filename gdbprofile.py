#!/usr/local/bin/python2.7
from __future__ import print_function, unicode_literals

import gdb


def backtrace():
    """ Generates stack frames until none is available """
    frame = gdb.newest_frame()

    while frame is not None:
        yield frame
        frame = frame.older()


def print_backtrace(event):
    if event.stop_signal != "SIGTRAP":
        print("Ignoring signal", event.stop_signal)
        return

    print("Dumping frames", event)

    for f in backtrace():
        print(f)
        print("\t", f.name())
        print("\t", f.find_sal())

    print("Done, last frame is", f)
    print("Event was:", event, dir(event), event.stop_signal, type(event.stop_signal))


gdb.execute("set pagination 0")

gdb.events.stop.connect(print_backtrace)

print("Profiler set up")
