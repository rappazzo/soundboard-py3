# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from rest_service.models.base_model_ import Model
from rest_service import util


class Phrase(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, phrase=None):  # noqa: E501
        """Phrase - a model defined in Swagger

        :param phrase: The phrase of this Phrase.  # noqa: E501
        :type phrase: str
        """
        self.swagger_types = {
            'phrase': str
        }

        self.attribute_map = {
            'phrase': 'phrase'
        }
        self._phrase = phrase

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Phrase of this Phrase.  # noqa: E501
        :rtype: Phrase
        """
        return util.deserialize_model(dikt, cls)

    @property
    def phrase(self):
        """Gets the phrase of this Phrase.


        :return: The phrase of this Phrase.
        :rtype: str
        """
        return self._phrase

    @phrase.setter
    def phrase(self, phrase):
        """Sets the phrase of this Phrase.


        :param phrase: The phrase of this Phrase.
        :type phrase: str
        """
        if phrase is None:
            raise ValueError("Invalid value for `phrase`, must not be `None`")  # noqa: E501

        self._phrase = phrase
