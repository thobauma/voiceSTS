import os
from pathlib import Path
import logging

from voiceagent.voiceAgent import VoiceAgent
from voiceagent.helper.constants import ffmpeg_path, model_id, api_base
from voiceagent.communication.communicator import Communicator

import tkinter as tk
import sounddevice as sd
from smolagents import LiteLLMModel


def main():
    # intit logging
    basePath = Path(__file__).parent
    runsPath = basePath / "logs/runs"
    runNumber = str(len(list(runsPath.glob("*"))))
    runPath = runsPath / runNumber
    runPath.mkdir()

    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)

    logging.captureWarnings(True)

    log_file_handler = logging.FileHandler(runPath / "run.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_file_handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(log_file_handler)

    logger.info(os.environ["PATH"])
    logger.info(sd.query_devices())

    # hacky way to add ffmpeg to the path of the subprocess
    os.environ["PATH"] += os.pathsep + os.pathsep.join([ffmpeg_path])
    logger.info(os.environ["PATH"])

    # host model locally with ollama
    model = LiteLLMModel(
        model_id=model_id,
        api_base=api_base,
    )
    promptPath = Path(__file__).parent / "voiceagent" / "prompts.yaml"
    fifoPath = basePath / "logs" / "fifo"
    communicator = Communicator(
        logger = logger,
        input_path=fifoPath / "sts_input",
        output_path=fifoPath / "sts_output",
    )
    # init and run agent
    root = tk.Tk()
    voiceAgent = VoiceAgent(
        model=model,
        prompts_path=promptPath,
        root=root,
        logger=logger,
        communicator=communicator,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
