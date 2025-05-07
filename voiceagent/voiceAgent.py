import time
import yaml
from pathlib import Path
import logging
import numpy as np
import tkinter as tk
from tkinter import scrolledtext

import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile
import traceback
import time


from smolagents import CodeAgent, Model

from voiceagent.actions import action_tools
from voiceagent.communication.communicator import Communicator

import whisper

class VoiceAgent:
    def __init__(self, model: Model, prompts_path: str | Path, root, logger: logging.Logger, communicator: Communicator):
        self.root = root
        self.root.title("Voice to STS")
        self.logger = logger
        self.logger.info("Loading Whisper model turbo")
        self.stt_model: whisper.Whisper = whisper.load_model(
            "turbo"
        )  # You can use "small", "medium", etc.
        with open(prompts_path, "r") as stream:
            self.prompt_template = yaml.safe_load(stream)
        self.agent = CodeAgent(
            model=model, tools=action_tools, max_steps=1, verbosity_level=2 # 0
        )
        self.comms = communicator
        self.listen_button = tk.Button(
            root,
            text="Listen (Auto Stop)",
            command=self.main_loop,
            font=("Arial", 14),
        )
        self.listen_button.pack(pady=10)

        self.output_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=100, height=50, font=("Consolas", 12)
        )
        self.output_area.pack(padx=10, pady=10)

        self.quit_button = tk.Button(
            root, text="Exit", command=self.root.quit, font=("Arial", 12)
        )
        self.quit_button.pack(pady=5)

    def main_loop(self):
        try:
            audio_file = self.record_audio()
            # Hacky way to counteract whisper hallicunations for silent inputs.
            if audio_file == -1:
                self.output_area.insert(tk.END, "No Sound detected\n")
                self.output_area.see(tk.END)
                self.root.update()
                return

            self.output_area.insert(tk.END, "Transcribing with Whisper...\n")
            self.output_area.see(tk.END)
            self.root.update()

            self.logger.info(f"""audiofile: {audio_file}""")
            spoken_text = self.transcribe(audio_file)

            task = f"""{self.prompt_template["system_prompt"]}\n\n{spoken_text}"""
            message = []
            for step_log in self.agent.run(task, max_steps=0):
                message.append(step_log.action_output)
            response = self.comms.send_and_receive(message[-1])
            # print(response)
            self.output_area.insert(tk.END, f"Output:\n{response}\n")
            self.output_area.see(tk.END)


        except Exception as e:
            self.output_area.insert(tk.END, f"Error: {str(e)}\n")
            self.output_area.insert(tk.END, traceback.format_exc())
            self.output_area.see(tk.END)

    def record_audio(
        self,
        samplerate: int = 16000,
        silence_threshold: int = 100,
        silence_duration: float = 5.0,
        max_duration: int = 10,
    ):
        self.output_area.insert(tk.END, "Recording... Speak now!\n")
        self.output_area.see(tk.END)
        self.root.update()

        # print("Speak your Python command: ")
        self.logger.info("Speak your Python command: ")
        audio_buffer = []
        start_time = time.time()
        last_sound_time = time.time()

        def callback(indata, frames, time_info, status):
            nonlocal last_sound_time
            volume_norm = np.linalg.norm(indata) * 10
            if volume_norm > silence_threshold:
                last_sound_time = time.time()
            audio_buffer.append(indata.copy())

        stream = sd.InputStream(samplerate=samplerate, channels=1, callback=callback)
        with stream:
            while True:
                self.root.update()
                time.sleep(0.1)
                if time.time() - last_sound_time > silence_duration:
                    self.logger.info("Silence detected. Stopping recording!")
                    self.output_area.insert(
                        tk.END, "Silence detected. Stopping recording!\n"
                    )
                    self.output_area.see(tk.END)
                    break
                if time.time() - start_time > max_duration:
                    self.logger.info("Max recording time reached.")
                    break

        audio_data = np.concatenate(audio_buffer, axis=0)
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        scipy.io.wavfile.write(
            temp_wav.name, samplerate, (audio_data * 32767).astype(np.int16)
        )
        # self.output_area.insert(tk.END, "Playing !\n")
        # self.output_area.see(tk.END)
        # sd.play(audio_data)
        # self.output_area.insert(tk.END, "Playing end!\n")
        # self.output_area.see(tk.END)
        if len(np.unique(audio_data)) == 1:
            return -1
        return temp_wav.name

    def transcribe(self, audio_path: str):
        # print("Transctibing with Whisper.")
        self.logger.info("Transcribing with Whisper.")
        result = self.stt_model.transcribe(audio_path, language="en", fp16=False)
        self.output_area.insert(tk.END, f"""You said: {result["text"]}\n""")
        self.output_area.see(tk.END)
        # print(f"You said: {result['text']}")
        self.logger.info(f"You said: {result['text']}")
        return result["text"]

    def generate_action(self, task):
        task = f"""{self.prompt_template["system_prompt"]}\n\n{task}"""
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": f"{self.prompt_template}"}],
            },
            {"role": "user", "content": [{"type": "text", "text": f"{task}"}]},
        ]
        self.agent()
