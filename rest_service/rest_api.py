#!/usr/bin/env python3

import connexion

from rest_service import encoder
from in_service import InService


class RestService(InService):

    def __init__(self, config=None):
        self.config = config or {}

    def get_name(self):
        return "rest"

    def run_service(self):
        app = connexion.App(__name__, specification_dir='spec/')
        app.app.json_encoder = encoder.JSONEncoder
        app.add_api('api.yaml', arguments={'title': 'Sounboard API'}, pythonic_params=True)
        print(f"Soundboard rest service is listening (port: {self.config.get('port', 8080)})")
        app.run(self.config.get('port', 8080))

    def stop_service(self):
        pass


if __name__ == '__main__':
    service = RestService()
    service.run_service()
