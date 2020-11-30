from flask import Flask, jsonify
from lfortune.fortune.config import Config
from lfortune.fortune.config_values import ConfigValues
from lfortune.fortune.factory import Factory
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

config = Config(None)
config_values = ConfigValues(config.fortunes_path())

fortune = Factory.create(config_values)

app.logger.info('ROOT PATH: %s', config_values.root_path)


@app.route("/", methods=['GET'])
def home() -> str:
    fortune_str = fortune.get()
    return jsonify({'fortune': fortune_str})


# commented out because of uwsgi
# app.run(port=5000)
