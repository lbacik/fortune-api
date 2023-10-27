import logging

from os import path, listdir
from typing import Optional

from lfortune.fortune.config_values import ConfigValues
from lfortune.fortune.indexer import Indexer
from lfortune.fortune.fortune import Fortune
from lfortune.abstract.fortune_source import FortuneSource
from lfortune.fortune.config import Config
from lfortune.fortune.factory import Factory
from lfortune.cli.arguments import Arguments


ENVIRONMENT_VAR_CORS = 'CORS'
SOURCE_LIST_KEY = 'sources'
SOURCE_PATH_KEY = 'path'
SOURCE_PROBABILITY_KEY = 'probability'


config = Config(Arguments.config)
config_values = ConfigValues(config.fortunes_path())
fortune = Factory.create(config_values)


logger = logging.getLogger(__name__)


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


def show_fortunes(config: ConfigValues, db: list) -> list:
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

    else:
        raise ValueError('the path is not a dir or a file')

    return result


def get_fortune(sources: Optional[list[FortuneSource]], index: Optional[int] = None) -> dict:

    fortune_data = fortune.get(sources, index)
    return {
        'fortune': fortune_data.fortune,
        'file': fortune_data.file,
        'index': fortune_data.index,
    }


def get_result(path: str = '', index: int | None = None, explore: bool = False) -> list | dict:

    logger.info('path: %s, index: %s, explore: %s', path, index, explore)

    try:
        if not explore:
            return get_fortune([FortuneSource(path)], index if index is not None else None)
        else:
            return show_fortunes(config_values,[path])
    except Exception as exception:
        return {'error': ' '.join(exception.args)}


def source_list_parser(value: dict) -> Optional[list[FortuneSource]]:
    sources = []
    for sourceDict in value[SOURCE_LIST_KEY]:
        sources.append(
            FortuneSource(
                sourceDict[SOURCE_PATH_KEY],
                sourceDict[SOURCE_PROBABILITY_KEY]
            )
        )
    return sources
