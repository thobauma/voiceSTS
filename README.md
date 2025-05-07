# VoiceSTS
A package that allows playing slay the spire with voice commands.

It uses whisper to transcripe the input and a codeagent to execute and send the input to slay the spire through the CommunicationMod.

This project is still WIP.

## Mod Requirements

- ModTheSpire
- BaseMod
- CommunicationMod

## Setup
- install the mods
- create the conda environment: `conda env create -f conda-recipe.yaml`
- serve an LLM model of your choice with Ollama
- add the model_id and api_base from the served model to `voiceagent/helper/constants.py`
- add the location of your ffmpeg binary to `voiceagent/helper/constants.py`
- install the voiceSTS: `pip install -e .`
- enable steam, slay the spire and ModTheSpire to use a Microphone
### CommunicationMod
- adapt `config.properties`:
    - path to python from the conda environment
    - path to `pipe.sh`
    - path to `sts_input` and `sts_output`
- add `config.properties` to the config of the CommunicationMod:
    - On Mac: `~/Library/Preferences/ModTheSpire/CommunicationMod/config.properties`

## Run
- `python main.py`
- start Slay the Spire with the mods (debug mode recommended)
- manually start a run and use voice commands as soon as you see the map
### Caveats
Sometimes the CommunicationMod fails to read the pipe. In that case let `main.py` run and manually run the CommunicationMod command again through the Mods field in the Slay the Spire main menu.

## Requirements:
- Python 3.11
- ffmpeg
- ollama
- LLM of your choice
