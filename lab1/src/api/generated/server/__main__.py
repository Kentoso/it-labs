#!/usr/bin/env python3

import connexion

from server import encoder
from flask import g
from service.database_service import AbstractDatabaseService, DatabaseService


def main():
    app = connexion.App(__name__, specification_dir="./openapi/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        "openapi.yaml", arguments={"title": "Simple DBMS API"}, pythonic_params=True
    )

    @app.app.before_request
    def before_request():
        g.database_service = DatabaseService()

    app.run(port=8080)


if __name__ == "__main__":
    main()
