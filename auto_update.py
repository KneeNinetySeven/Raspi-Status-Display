import logging
import os
from threading import Thread
import time

class AutoUpdater:

    _thread: Thread
    _running: bool = False

    def __init__(self, wait_millis) -> None:
        self._logger = logging.getLogger()
        self.wait_millis = wait_millis

    def __del__(self) -> None: 
        if not self._thread == None and self._thread.is_alive(): 
            self._running = False
            
    def run(self) -> None:
        self._thread = Thread(
            daemon=True,
            name="Auto Update Watchdog",
            target=self._check,
        ).start()
        self._running = True

    def _check(self) -> None:
        self._logger.info("Auto update watchdog initiated!")
        while(self._running): 
            self._logger.info("Checking for avilable updates")
            if self._is_update_available():
                self._start_update_script()
            else:
                self._logger.debug("No available update detected.")
            time.sleep(self.wait_millis / 1000)
            

    def _is_update_available(self) -> bool:
        return not os.system("git diff-index --quiet HEAD") == 0

    def _start_update_script(self) -> None:
        self._logger.info("Available update detected. Initiating...")
        os.system("./script/update.sh")
