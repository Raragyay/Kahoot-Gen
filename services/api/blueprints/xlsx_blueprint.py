import os
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, safe_join, send_from_directory

from constants import DEFAULT_KAHOOT, base_folder_path
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
    return {
               'fileId': path.parent.stem}, 200
    # return send_from_directory(directory=path.parent, filename=path.name)


@xlsx_blueprint.route('/<fileId>', methods=['GET'])
def get_file_id(fileId):
    file_path = Path(safe_join(base_folder_path.joinpath('xlsx_export'), fileId, 'kahoot_export.xlsx'))
    if file_path.exists():
        return send_from_directory(directory=file_path.parent,
                                   filename=file_path.name)
    else:
        return 'File does not exist', 404
