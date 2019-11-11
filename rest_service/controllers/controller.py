import socket

import connexion

from command import commands
from rest_service.models.phrase import Phrase
from rest_service.models.sound import Sound
from rest_service import util


def list_sounds(tag=None, offset=None, limit=None):
    """list the sounds available in the soundboard

    List the sounds with the specified tag.  If no tag is specified, then the files
    listed will be from the untagged list (default)

        :param tag: the tag for sounds to list
        :type tag: str
        :param offset: number of records to skip for pagination
        :type offset: int
        :param limit: maximum number of records to return
        :type limit: int

        :rtype: List[str]
    """
    sounds = commands.list_sounds(lib_name=tag)
    if offset is not None:
        if limit is not None:
            sounds = sounds[offset:offset+limit]
        else:
            sounds = sounds[offset:]
    elif limit is not None:
        sounds = sounds[:limit]

    return sounds


def list_tags():
    """list the tags which sounds are filed under
    :rtype: None
    """
    return commands.list_libs()


def play_something(sound=None):
    """make the soundboard play a sound

    plays the specified sound OR a sound at random if only the tag is speficied

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        sound = Sound.from_dict(connexion.request.get_json())
    sounds = []
    if sound.name is not None:
        sounds.append(sound.name)
    if sound.names is not None:
        sounds.extend(sound.names)
    who = socket.gethostbyaddr(connexion.request.remote_addr)[0]
    result = commands.play_sound(*sounds, lib_name=sound.tag, who=who)

    return result


def say_something(data=None):  # noqa: E501
    """make the soundboard say a phrase

    says the specified word or phrase

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        data = Phrase.from_dict(connexion.request.get_json())
    who = socket.gethostbyaddr(connexion.request.remote_addr)[0]
    return commands.say_phrase(data.phrase, who=who)


def stop_audio():
    """make the soundboard stop the current audio output

    stop audio output


    :rtype: None
    """
    who = socket.gethostbyaddr(connexion.request.remote_addr)[0]
    return commands.stop_audio(who=who)
