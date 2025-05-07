import logging
import os
import stat
import fcntl
from pathlib import Path

def init_fifos(filenames):
    # Create fifos for communication
    for f in filenames:
        if os.path.exists(f):
            os.remove(f)
        os.mkfifo(f)
        os.chmod(
            f,
            stat.S_IRUSR
            | stat.S_IWUSR
            | stat.S_IRGRP
            | stat.S_IWGRP
            | stat.S_IROTH
            | stat.S_IWOTH,
        )


class Communicator:
    def __init__(self, logger: logging.Logger, input_path: Path, output_path: Path):
        self.logger = logger
        self.input_path = input_path
        self.output_path = output_path
        init_fifos([self.input_path, self.output_path])

        self.logger.debug("Opening fifo")
        self.input_fifo = open(self.input_path, "w")
        self._send_message("Ready")
        self.output_fifo = open(self.output_path, "r")
        flag = fcntl.fcntl(self.output_fifo, fcntl.F_GETFD)
        fcntl.fcntl(self.output_fifo, fcntl.F_SETFL, flag | os.O_NONBLOCK)
        self.logger.debug("Opening fifo done")
        self.logger.debug("Sending Ready")

    def send_and_receive(self, message: str) -> str:
        self.logger.info(f"send message: {message}")
        self.output_fifo.readlines()
        self._send_message(message)
        response = self.output_fifo.readline()
        self.logger.info(f"response: {response}")
        return response

    def _send_message(self, message: str) -> None:
        self.input_fifo.write(f"{message}\n")
        self.input_fifo.flush()

