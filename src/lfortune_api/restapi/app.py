from typing import List

from flask import Flask, jsonify, request
from lfortune.abstract.fortune_source import FortuneSource
from lfortune.fortune.config import Config
from lfortune.fortune.config_values import ConfigValues
from lfortune.fortune.factory import Factory
from lfortune.cli.arguments import Arguments
from .functions import show_fortunes
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

config = Config(Arguments.config)
config_values = ConfigValues(config.fortunes_path())

fortune = Factory.create(config_values)
app.logger.info('ROOT PATH: %s', config_values.root_path)


def get_fortune(sources: List[FortuneSource]) -> str:
    fortune_str = fortune.get(sources)
    return jsonify({'fortune': fortune_str})


@app.route("/", methods=['GET'])
@app.route("/<path:path>", methods=['GET'])
def home(path: str = '') -> str:
    explore: bool = request.args.get('explore', False)
    if explore != False:
        result = show_fortunes(config_values, [path])
        return jsonify(result)
    else:
        sources = None
        if path:
            sources = [FortuneSource(path)]
        return get_fortune(sources)
