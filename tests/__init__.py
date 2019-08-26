import pytest
import json
import logging
from flask import Flask, request
from blueprints import app
from ecommerce import cache


def call_user(request):
    user = app.test_client()
    return user


@pytest.fixture
def user(request):
    return call_user(request)


def create_token_admin():
    token = cache.get('test-token')
    if token is None:
        # prepare request input
        data = {
            'username': 'ammar',
            'password': 'satudua'
        }
        # do request
        req = call_user(request)
        res = req.post('/auth',
                        data=json.dumps(data),
                        content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token


def create_token_user():
    token = cache.get('test-token')
    if token is None:
        # prepare request input
        data = {
            'username': 'Dwita',
            'password': 'dwita123'
        }
        # do request
        req = call_user(request)
        res = req.post('/auth',
                        data=json.dumps(data),
                        content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token
