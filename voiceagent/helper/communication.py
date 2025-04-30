import logging

class Communicator:
    def __init__(self):
        self.send("ready")

    def send(self, message: str) -> str:
        logging.info(f"send message: {message}")
        response = input(message + "\n")
        logging.info(f"response: {response}")
        return response