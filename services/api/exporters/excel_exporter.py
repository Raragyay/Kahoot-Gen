import os
from pathlib import Path
from uuid import uuid4

import pandas as pd

import constants
from exporters import BaseExporter


class ExcelExporter(BaseExporter):
    def __init__(self):
        super().__init__()

    def export(self, kahoot) -> Path:
        """
        Exports the given kahoot into an excel file ready for importing and returns the path to the file
        :param kahoot:
        :return:
        """
        base_path: Path = constants.base_folder_path
        folder_id = uuid4()
        export_path = base_path.joinpath("xlsx_export", str(folder_id), "kahoot_export.xlsx")
        question_list = kahoot['kahoot']['questions']
        output_df = pd.DataFrame(
            columns=['Questions', 'Answer 1', 'Answer 2', 'Answer 3', 'Answer 4', 'Time', 'Correct Answer'])

        for idx, question in enumerate(question_list):
            prompt = question['question']
            choices = [answer['answer'] for answer in question['choices']]
            time = question['time']
            correct_answers = ",".join(map(str, [idx + 1 for idx, answer in enumerate(question['choices']) if answer[
                'correct']]))
            output_df.loc[idx] = [prompt, *choices, time, correct_answers]

        os.mkdir(export_path.parent)
        output_df.to_excel(export_path, encoding='utf-8-sig')
        return export_path
