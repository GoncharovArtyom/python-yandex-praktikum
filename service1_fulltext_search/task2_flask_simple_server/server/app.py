import json

from flask import Flask, Response
from flask import request

app = Flask(__name__)


@app.route('/client/info', methods=['GET'])
def get_client_info():
    response = {
        'user_agent': request.headers['User-Agent']
    }
    return Response(
        status=200,
        response=json.dumps(response),
        headers={
            'Content-Type': 'application/json'
        }
    )
