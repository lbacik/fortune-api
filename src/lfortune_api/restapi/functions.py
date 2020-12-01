from os import makedirs, path, listdir
from typing import List

from lfortune.fortune.config_values import ConfigValues
from lfortune.fortune.indexer import Indexer
from lfortune.fortune.fortune import Fortune


def read_fortune(file: str, i: int) -> str:
    result: str = ''
    file = open(file, 'r')
    file.seek(i)
    fortune_end = False
    while not fortune_end:
        line = file.readline()
        if line and line != Fortune.SEPARATOR:
            result += line
        else:
            fortune_end = True
    return result


def show_fortunes(config: ConfigValues, db: List) -> List:
    fortune_path = config.root_path
    if db and db[0].find('..') == -1:
        fortune_path += f'/{db[0]}'

    result = []

    if path.isdir(fortune_path):
        for filename in listdir(fortune_path):
            if filename[0] == '.':
                continue
            current_file = f'{fortune_path}/{filename}'
            if path.isfile(current_file):
                filename, file_extension = path.splitext(filename)
                if not file_extension:
                    result.append(filename)
            elif path.isdir(current_file):
                result.append(f'{filename}/')

    elif path.isfile(fortune_path):
        indexer = Indexer(Fortune.SEPARATOR)
        data = indexer.index(fortune_path)
        for f in data.indices:
            result.append(read_fortune(fortune_path, f))

    return result
