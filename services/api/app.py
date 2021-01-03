from flask import Flask

from blueprints.xlsx_blueprint import xlsx_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(xlsx_blueprint, url_prefix='/api/create_xlsx')
    return app


app = create_app()
if __name__ == '__main__':
    app.run()
