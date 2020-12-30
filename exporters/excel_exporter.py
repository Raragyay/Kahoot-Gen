import asyncio
import copy
from pathlib import Path
from uuid import uuid4
import pandas as pd
import aiofiles.os as aios

import constants
from constants import DEFAULT_KAHOOT
from exporters.base_exporter import BaseExporter
from kahoot_creator import KahootCreator


class ExcelExporter(BaseExporter):
    def __init__(self):
        super().__init__()

    async def export(self, kahoot) -> Path:
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

        async def set_df_idx(entry):
            idx, question = entry
            prompt = question['question']
            choices = [answer['answer'] for answer in question['choices']]
            time = question['time']
            correct_answers = ",".join(map(str, [idx + 1 for idx, answer in enumerate(question['choices']) if answer[
                'correct']]))
            output_df.loc[idx] = [prompt, *choices, time, correct_answers]

        await asyncio.gather(*map(set_df_idx, enumerate(question_list)))
        await aios.mkdir(export_path.parent)
        output_df.to_excel(export_path, encoding='utf-8-sig')
        return export_path


async def main():
    kahoot_copy = copy.deepcopy(DEFAULT_KAHOOT)
    kahoot_copy['kahoot']['questions'] = await KahootCreator().question_generator.generate_questions(**{
        'question_type'   : 'fr_ant',
        'categories'      : ["personalities"],
        'num_of_questions': 3})
    await ExcelExporter().export(kahoot_copy)


if __name__ == '__main__':
    asyncio.run(main())
