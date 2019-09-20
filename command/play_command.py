from command import Command
import subprocess
import tempfile
from pydub import AudioSegment
from pydub.playback import PLAYER

from library.libraries import Libraries

procs = {}

def cleanup():
    cleaned = 0

    for file in list(procs.keys()):
        proc = procs.get(file)
        if proc.poll() is not None:
            file.close()
            procs.remove(file)
            cleaned += 1

    return cleaned

def stop():
    stopped = 0
    for file in list(procs.keys()):
        proc = procs.pop(file)
        file.close()
        if proc.poll() is None:
            proc.terminate()
            stopped += 1
    return stopped

def async_play(clip: AudioSegment):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav")
    clip.export(temp_file, "wav")
    procs[temp_file] = subprocess.Popen(
            [PLAYER, "-nodisp", "-autoexit", "-hide_banner", temp_file.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def wait_for_play_to_complete():
    count = 0
    for file in list(procs.keys()):
        proc = procs.pop(file)
        if proc.poll() is None:
            proc.wait()
            count += 1
    return count


class Play(Command):

    def __init__(self, config=None):
        config = config or {}
        lib_name = config.get("lib_name", None)
        if lib_name is None:
            self.library = Libraries().instance.get_default_lib()
            lib_name = "Default Library"
        else:
            self.library = Libraries().instance.get_lib(lib_name)
        if self.library is None:
            raise NameError(f"{lib_name} not found")

    def invoke(self, *args):
        valid = False
        clip = AudioSegment.empty()
        played = ''
        if self.library is not None:
            for arg in args:
                if self.library.has_file(arg):
                    if len(played) > 0:
                        played += " "
                    played += arg
                    clip += AudioSegment.from_file(self.library.get_file(arg))
                    valid = True
                else:
                    clip += AudioSegment.silent(100)
                    played += f" XX_{arg}_XX"

        if valid:
            async_play(clip)
            return f"{self.get_name()} '{played}'"

        return None
