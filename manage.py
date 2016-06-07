#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'wbs_timetracker'
        )
    )

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wbs_timetracker.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
