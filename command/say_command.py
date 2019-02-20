from command import Command
import io
import os
import requests
import tempfile
from pydub import AudioSegment
from pydub.playback import play


class Say(Command):

    def __init__(self, config):
        self.api_key = config.get("api_key", os.environ["VOICE_RSS_API_KEY"])
        if self.api_key is None:
            print("Missing API key for 'say' command")
            raise ValueError ("Missing API key for 'say' command")
        self.language = 'en-us'

    def invoke(self, *args):
        # do the say command
        sentence = " ".join(args)
        params = {
            'key': self.api_key,
            'src': sentence,
            'hl': self.language,
            'r': 0,
            'c': 'WAV',
            'f': '16khz_16bit_stereo'
        }
        r = requests.get("http://api.voicerss.org/", params=params)
        clip = AudioSegment.from_file(io.BytesIO(r.content), format='wav')
        play(clip)

        return f"I said '{sentence}'"

