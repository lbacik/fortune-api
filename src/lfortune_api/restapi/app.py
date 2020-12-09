import lfortune_api.restapi.logging_config
from typing import List, Optional, Dict
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from lfortune.abstract.fortune_source import FortuneSource
from lfortune.fortune.config import Config
from lfortune.fortune.config_values import ConfigValues
from lfortune.fortune.factory import Factory
from lfortune.cli.arguments import Arguments
from .functions import show_fortunes

SOURCE_LIST_KEY = 'sources'
SOURCE_PATH_KEY = 'path'
SOURCE_PROBABILITY_KEY = 'probability'

app = Flask(__name__)
api = Api(app=app, version="0.2.1")
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
                f'{config_values.root_path}/{sourceDict[SOURCE_PATH_KEY]}',
                sourceDict[SOURCE_PROBABILITY_KEY]
            )
        )
    return sources


def get_fortune(sources: Optional[List[FortuneSource]]) -> str:
    fortune_str = fortune.get(sources)
    return jsonify({'fortune': fortune_str})


@name_space.route("/<path:path>")
@name_space.param('explore', 'list the directory content or all fortunes from the file (if path indicates file)')
class FortuneApi(Resource):
    @staticmethod
    def get(path: str = '') -> str:
        explore: bool = request.args.get('explore', False)
        app.logger.debug('explore: %s, path: %s', explore, path)
        if explore is False:
            sources = None
            if path:
                sources = [FortuneSource(f'{config_values.root_path}/{path}')]
            return get_fortune(sources)
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
