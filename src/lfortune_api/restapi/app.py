import os

from typing import List, Optional, Dict
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from lfortune.abstract.fortune_source import FortuneSource
from lfortune.fortune.config import Config
from lfortune.fortune.config_values import ConfigValues
from lfortune.fortune.factory import Factory
from lfortune.cli.arguments import Arguments
from .functions import show_fortunes

VERSION = '0.4'

ENVIRONMENT_VAR_CORS = 'CORS'
SOURCE_LIST_KEY = 'sources'
SOURCE_PATH_KEY = 'path'
SOURCE_PROBABILITY_KEY = 'probability'

app = Flask(__name__)

if ENVIRONMENT_VAR_CORS in os.environ and os.environ.get(ENVIRONMENT_VAR_CORS) == 'yes':
    CORS(app)
    app.logger.info('*** CORS has been set up!')

api = Api(app=app, version=VERSION)
name_space = api.namespace('fortune', description='Fortune API')

source_model = api.model('Source', {
    SOURCE_PATH_KEY: fields.String,
    SOURCE_PROBABILITY_KEY: fields.Integer(default=0)
})

source_list_model = api.model('SourceList', {
    SOURCE_LIST_KEY: fields.List(fields.Nested(source_model)),
})

config = Config(Arguments.config)
config_values = ConfigValues(config.fortunes_path())
fortune = Factory.create(config_values)
app.logger.info('ROOT PATH: %s', config_values.root_path)


def source_list_parser(value: Dict) -> Optional[List[FortuneSource]]:
    sources = []
    for sourceDict in value[SOURCE_LIST_KEY]:
        sources.append(
            FortuneSource(
                sourceDict[SOURCE_PATH_KEY],
                sourceDict[SOURCE_PROBABILITY_KEY]
            )
        )
    return sources


def get_fortune(sources: Optional[List[FortuneSource]], index: Optional[int] = None) -> str:
    fortune_data = fortune.get(sources, index)
    return jsonify({
        'fortune': fortune_data.fortune,
        'file': fortune_data.file,
        'index': fortune_data.index,
    })


@name_space.route("/<path:path>")
@name_space.param('explore', 'list the directory content or all fortunes from the file (if path indicates file)')
class FortuneApi(Resource):
    @staticmethod
    def get(path: str = '', index: Optional[int] = None) -> str:
        explore: bool = request.args.get('explore', False)
        app.logger.debug('explore: %s, path: %s', explore, path)
        if explore is False:
            sources = None
            if path:
                sources = [FortuneSource(path)]
            return get_fortune(sources, index)
        else:
            try:
                result = show_fortunes(config_values, [path])
                return jsonify(result)
            except ValueError as e:
                api.abort(404, e)


@name_space.route("/")
@name_space.param('explore', 'list the directory content or all fortunes from the file (if path indicates file)')
class FortuneApiPost(Resource):
    @staticmethod
    def get() -> str:
        return FortuneApi.get()

    @staticmethod
    @name_space.expect(source_list_model)
    def post():
        explore: bool = request.args.get('explore', False)
        if explore:
            api.abort(400, 'use GET for explore')
        app.logger.debug(api.payload)
        sources = source_list_parser(api.payload)
        return get_fortune(sources)


@name_space.route("/<path:path>/<int:index>")
class FortuneApiGetByIndex(Resource):
    @staticmethod
    def get(path: str, index: int) -> str:
        return FortuneApi.get(path, index)
