import subprocess
import tempfile
from pydub import AudioSegment
from pydub.playback import PLAYER

audio_processes = {}


def cleanup():
    cleaned = 0

    for file in list(audio_processes.keys()):
        audio_process = audio_processes.get(file)
        if audio_process.poll() is not None:
            file.close()
            audio_processes.remove(file)
            cleaned += 1

    return cleaned


def stop():
    stopped = 0
    for file in list(audio_processes.keys()):
        audio_process = audio_processes.pop(file)
        file.close()
        if audio_process.poll() is None:
            audio_process.terminate()
            stopped += 1
    return stopped


def async_play(clip: AudioSegment):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav")
    clip.export(temp_file, "wav")
    audio_processes[temp_file] = subprocess.Popen(
            [PLAYER, "-nodisp", "-autoexit", "-hide_banner", temp_file.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def wait_for_play_to_complete():
    count = 0
    for file in list(audio_processes.keys()):
        audio_process = audio_processes.pop(file)
        if audio_process.poll() is None:
            audio_process.wait()
            count += 1
    return count
