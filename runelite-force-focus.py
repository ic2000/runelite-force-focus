#!/usr/bin/env python3

import re
import sys
from subprocess import PIPE, STDOUT, Popen, check_output, run
import shlex
from datetime import datetime


def get_window_title():
    window_titles = check_output(["wmctrl", "-l"]).decode().rstrip()
    r = re.compile("^[^ ]+  [^ ]+ [^ ]+ RuneLite - \w+$")
    window_titles = window_titles.split("\n")
    window_title = list(filter(r.match, window_titles))[0]
    return window_title[window_title.find("RuneLite") :]


def main():
    journalctl = Popen("journalctl -f", stdout=PIPE, stderr=STDOUT, shell=True)

    for line in journalctl.stdout:
        line = line.decode().rstrip()

        if "runelite" in line and "notify-send" in line:
            time = line.split(" ")[2]

            if time != datetime.now().strftime("%H:%M:%S"):
                continue

            active_window_title = (
                check_output(["xdotool", "getwindowfocus", "getwindowname"])
                .decode()
                .rstrip()
            )

            window_title = get_window_title()

            if window_title != active_window_title:
                run(
                    shlex.split(
                        f"xdotool search --any --name '{window_title}' windowactivate"
                    )
                )

    return 0


if __name__ == "__main__":
    sys.exit(main())
