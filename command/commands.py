import random
import io
import os
import requests

from command.audio import async_play, stop
from library.libraries import Libraries
from pydub import AudioSegment
from pydub.playback import play


voice_rss_api_key = None
language = 'en-us'
registry = {}


def configure_commands(config):
    config = config or {}
    global voice_rss_api_key
    voice_rss_api_key = config.get("say", {}).get("api_key") or os.environ["VOICE_RSS_API_KEY"]


def register_command(name, cmd):
    registry[name] = cmd


def get_command(name):
    return registry.get(name)


def has_command(name):
    return registry.get(name) is not None


def list_sounds(lib_name=None):
    if lib_name is None:
        library = Libraries().instance.get_default_lib()
    else:
        library = Libraries().instance.get_lib(lib_name)
    if library is not None:
        return sorted(library.list())
    return []


def list_libs():
    lib_names = []
    for lib in Libraries().instance.get_libs():
        if not lib.is_default():
            lib_names.append(lib.get_name())
    return sorted(lib_names)


def play_sound(*sound_names, lib_name=None):
    if lib_name is None:
        library = Libraries().instance.get_default_lib()
    else:
        library = Libraries().instance.get_lib(lib_name)

    valid = False
    clip = AudioSegment.empty()
    played = ''
    if library is not None:
        if len(sound_names) == 0:
            sound_names = [random.choice(library.list())]
        for sound_name in sound_names:
            if library.has_file(sound_name):
                if len(played) > 0:
                    played += " "
                played += sound_name
                clip += AudioSegment.from_file(library.get_file(sound_name))
                valid = True
            else:
                clip += AudioSegment.silent(100)
                played += f" XX_{sound_name}_XX"

    if valid:
        async_play(clip)
        base_name = lib_name or "Play"
        return f"{base_name} '{played}'"


def say_phrase(*words):
    if voice_rss_api_key is None:
        print("Missing API key for 'say' command")
        raise ValueError ("Missing API key for 'say' command")
    # do the say command
    sentence = " ".join(words)
    params = {
        'key': voice_rss_api_key,
        'src': sentence,
        'r': 0,
        'c': 'WAV',
        'f': '16khz_16bit_stereo'
    }
    r = requests.get("http://api.voicerss.org/", params=params)
    clip = AudioSegment.from_file(io.BytesIO(r.content), format='wav')
    play(clip)

    return f"I said '{sentence}'"


def stop_audio():
    stopped = stop()
    return f"stopped {stopped}"
