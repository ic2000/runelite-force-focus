#!/usr/bin/env python3

import re
import sys
from subprocess import PIPE, STDOUT, Popen, run
import shlex


def main():
    notifs = Popen(
        'dbus-monitor "interface=\'org.freedesktop.Notifications\'" | grep --line-buffered  "member=Notify\|string"',
        stdout=PIPE,
        stderr=STDOUT,
        shell=True,
    )

    for line in notifs.stdout:
        line = line.decode().rstrip()
        runelite_notif = re.search(r"\"(RuneLite - \w+)\"", line)

        if runelite_notif:
            window_title = runelite_notif.group(1)

            run(
                shlex.split(
                    f"xdotool search --any --name '{window_title}' windowactivate"
                )
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
