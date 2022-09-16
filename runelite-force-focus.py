#!/usr/bin/env python3

import re
import sys
from subprocess import PIPE, STDOUT, Popen, check_output, run, CalledProcessError
import shlex


def main():
    journalctl = Popen(
        'dbus-monitor "interface=\'org.freedesktop.Notifications\'" | grep --line-buffered  "member=Notify\|string"',
        stdout=PIPE,
        stderr=STDOUT,
        shell=True,
    )

    for line in journalctl.stdout:
        line = line.decode().rstrip()
        runelite_notif = re.search(r"\"(RuneLite - \w+)\"", line)

        if runelite_notif:
            window_title = runelite_notif.group(1)

            try:
                active_window_title = (
                    check_output(("xdotool", "getwindowfocus", "getwindowname"))
                    .decode()
                    .rstrip()
                )
            except CalledProcessError: # no active window
                active_window_title = None

            if window_title != active_window_title:
                run(
                    shlex.split(
                        f"xdotool search --any --name '{window_title}' windowactivate"
                    )
                )

    return 0


if __name__ == "__main__":
    sys.exit(main())
