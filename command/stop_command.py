from command import Command
from command.play_command import stop

class Stop(Command):

    def __init__(self, config):
        pass

    def invoke(self, *args):
        stopped = stop()
        return f"stopped {stopped}"
