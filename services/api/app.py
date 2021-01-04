from flask import Flask

import config
from db.db import db
from blueprints.xlsx_blueprint import xlsx_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(xlsx_blueprint, url_prefix='/api/create_xlsx')
    app.config.from_object(config.Config)
    db.init_app(app)
    return app


app = create_app()
if __name__ == '__main__':
    app.run()
