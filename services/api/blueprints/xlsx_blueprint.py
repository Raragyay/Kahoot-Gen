from flask import Blueprint, current_app, request, send_from_directory

from constants import DEFAULT_KAHOOT
from exporters import ExcelExporter
from kahoot_creator import KahootCreator

xlsx_blueprint = Blueprint('xlsx_blueprint', __name__)


@xlsx_blueprint.route('', methods=['POST'])
def xlsx_export():
    """
    Takes parameters to generate a kahoot and sends back an excel file
    :return:
    """
    json = request.get_json()
    if 'kahootData' not in json:
        return 'kahootData not in request', 400
    params = json['kahootData']
    kahoot = KahootCreator(DEFAULT_KAHOOT)
    try:
        kahoot.generate_questions(params)
    except Exception as e:
        current_app.log(e)
        return 'malformed request', 400
    exporter = ExcelExporter()
    path = exporter.export(kahoot.kahoot)
    return send_from_directory(directory=path.parent, filename=path.name)

    # print(request.get_json())
