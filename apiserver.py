import flask
from flask import jsonify, request

blueprint = flask.Blueprint(
    'bot_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/bot/<question>', methods=['GET'])
def get_answer(question):
    print(question)
    answer = ''
    return answer