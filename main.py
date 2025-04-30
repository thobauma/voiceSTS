import os
from pathlib import Path
import logging

from voiceagent.voiceAgent import VoiceAgent
from voiceagent.helper.constants import ffmpeg_path, model_id, api_base

import tkinter as tk
import sounddevice as sd
from smolagents import LiteLLMModel

def main():
    # intit logging
    basePath = Path(__file__).parent
    logPath = basePath/"logs"
    logfile = "log"+str(len(list(logPath.glob('*'))))+".log"
    logging.basicConfig(filename=logPath/logfile, level=logging.INFO)
    logging.info(os.environ['PATH'])
    logging.info(sd.query_devices())
    
    # hacky way to add ffmpeg to the path of the subprocess
    os.environ['PATH'] += os.pathsep + os.pathsep.join([ffmpeg_path])
    logging.info(os.environ['PATH'])

    # host model locally with ollama
    model = LiteLLMModel(
        model_id=model_id,
        api_base=api_base,
    )
    prompt_path = Path(__file__).parent / "voiceagent" / "prompts.yaml"
    
    # init and run agent
    root = tk.Tk()
    voiceAgent = VoiceAgent(model=model, prompts_path=prompt_path, root=root)
    root.mainloop()


if __name__ == "__main__":
    main()
