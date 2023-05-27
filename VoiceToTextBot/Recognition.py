import subprocess as sp
import wave
import json
import os

from vosk import Model, KaldiRecognizer
from pathlib import Path


async def recognition_def(model: Model, file_path: Path) -> str:

    cmd_parameters = [f"ffmpeg -i {file_path} -ac 1 -ar 16000 -y "
                      f"-f wav output.wav "]
    sp.run(cmd_parameters, shell=True, stdout=sp.DEVNULL, stdin=sp.DEVNULL)
    file_path = "output.wav"
    wf = wave.open(f'{file_path}', "rb")
    rec = KaldiRecognizer(model, 16000)
    data = wf.readframes(wf.getnframes())
    rec.AcceptWaveform(data)
    recognized_data = json.loads(rec.Result())["text"]
    os.remove(file_path)
    return recognized_data
