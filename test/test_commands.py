import time
from command import say_command, play_command, stop_command, list_command
from command.play_command import wait_for_play_to_complete
from library.files_library import FilesLibrary
from library.libraries import Libraries


class TestCommand:

    def test_say(self, capsys):
        say = say_command.Say()
        out = say.invoke("some words")
        assert out == "I said 'some words'"

    def test_play_one_file(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard'), is_default=True)
        play_cmd = play_command.Play()
        out = play_cmd.invoke("rimshot")
        wait_for_play_to_complete()
        assert out == "play 'rimshot'"

    def test_play_multi_files(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard/kurt'))
        play_cmd = play_command.Play(lib_name="kurt")
        out = play_cmd.invoke("nestor", "is", "technology")
        wait_for_play_to_complete()
        assert out == "kurt 'nestor is technology'"

    def test_play_multi_files_with_missing(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard/kurt'))
        play_cmd = play_command.Play(lib_name="kurt")
        out = play_cmd.invoke("nestor", "is", "weenie", "technology")
        wait_for_play_to_complete()
        assert out == "kurt 'nestor is XX_weenie_XX technology'"

    def test_stop(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard'), is_default=True)
        play_cmd = play_command.Play()
        stop_cmd = stop_command.Stop()
        play_cmd.invoke("greatestamericanhero")
        time.sleep(3)
        out = stop_cmd.invoke()
        assert out == "stopped 1"

    def test_try_to_stop_a_finished_play(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard'), is_default=True)
        play_cmd = play_command.Play()
        stop_cmd = stop_command.Stop()
        play_cmd.invoke("doh")
        time.sleep(3)
        out = stop_cmd.invoke()
        assert out == "stopped 0"

    def test_list_command(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard'), is_default=True)
        list_cmd = list_command.List()
        sounds = list_cmd.invoke()
        assert len(sounds) > 0

    def test_non_default_list_command(self, capsys):
        Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard/kurt'))
        list_cmd = list_command.List()
        sounds = list_cmd.invoke('kurt')
        assert len(sounds) > 0
