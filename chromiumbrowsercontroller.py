import fileinput
import logging
import os
import subprocess
from pathlib import Path


class ChromiumBrowserController:
    """Handles Chromium browser instances to show the
    blaulichtSMS Einsatzmonitor dashboard.
    """

    def __init__(self, session_id):
        self.logger = logging.getLogger(__name__)
        self._session_id = session_id
        self._process = None

    def start(self):
        self._delete_crash_exit()
        self._process = subprocess.Popen(
            [
                "/usr/bin/chromium-browser",
                "--display=:0",
                "--noerrdialogs",
                "--disable-session-restore",
                "--disable-session-crashed-bubble",
                "--disable-infobars",
                "--start-fullscreen",
                "https://dashboard.blaulichtsms.net/#/login?token="
                + self._session_id
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        self.logger.info("Started browser")

    def is_alive(self):
        return self._process.poll() is None

    def _delete_crash_exit(self):
        """If Chromium starts after an unexpected exit (e.g. the host crashed),
        Chromium displays a notification asking if the user wants to restore the crashed session.

        This method removes this notification, as it is not wanted for the alarm monitor.
        """
        self.logger.debug("Delete crashed session flag")
        file_path = os.path.join(
            str(Path.home()), ".config", "chromium", "Default", "Preferences")
        try:
            with fileinput.input(files=file_path, inplace=True) as file:
                for line in file:
                    replaced_line = line.replace(
                        "\"exit_type\":\"Crashed\"",
                        "\"exit_type\":\"Normal\""
                    )
                    print(replaced_line, end="")
        except FileNotFoundError:
            self.logger.debug(
                "Preferences file does not exist."
                + " No crashed session flag to delete."
            )

    def terminate(self):
        self._process.terminate()
        self.logger.info("Closed browser")
