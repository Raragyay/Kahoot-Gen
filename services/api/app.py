from flask import Flask

import config
from blueprints.default_table import default_table_blueprint
from blueprints.xlsx_blueprint import xlsx_blueprint
from db.db import db


def create_app():
    app = Flask(__name__)
    app.register_blueprint(xlsx_blueprint, url_prefix='/api/excel')
    app.register_blueprint(default_table_blueprint, url_prefix='/api/default-table')
    app.config.from_object(config.Config)
    db.init_app(app)
    return app


app = create_app()
if __name__ == '__main__':
    app.run()
