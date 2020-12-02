import subprocess
import logging
import os
import sys
import signal
import requests

import traceback

root = logger = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def exception_hook(exc_type, exc_value, exc_traceback):
    logging.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )
sys.excepthook = exception_hook


class TestClass:
    @classmethod
    def setup_class(cls):
        logger.info("(setup_class) for {}".format(cls.__name__))

    @classmethod
    def teardown_class(cls):
        logger.info("(teardown_class) for {}".format(cls.__name__))

    def setup_method(self, method):
        logger.info("setup_method for {}".format(method.__name__))

    def teardown_method(self, method):
        logger.info("teardown_method for {}".format(method.__name__))

    def test_get_directory(self):
        logger.info("BEGIN: test_get_directory")
        response = requests.get('http://127.0.0.1:8088/rest/services/__dir__/')
        logger.info("test_get_directory :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        #logger.info("test_get_directory :: response.json() -> {}".format(data))
        assert response.status_code == 200, 'Problem with test_get_directory #1.'
        assert data.get('status') == 'OK', 'Problem with test_get_directory #2.'
        assert data.get('has_plugins') == True, 'Problem with test_get_directory #3.'
        assert len(data.get('modules', {}).keys()) > 0, 'Problem with test_get_directory #4.'
        assert len(data.get('endpoints', {}).keys()) > 0, 'Problem with test_get_directory #5.'
        assert len(data.get('imports', {}).keys()) > 0, 'Problem with test_get_directory #6.'
        logger.info("END!!! test_get_directory")


    def test_complex_get(self):
        logger.info("BEGIN: test_complex_get")
        response = requests.get('http://127.0.0.1:8088/rest/services/hello-world/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4')
        logger.info("test_complex_get :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_complex_get #1.'
        assert data.get('status') == 'OK', 'Problem with test_complex_get #2.'
        assert len(data.get('response', {}).keys()) > 0, 'Problem with test_complex_get #3.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_complex_get :: items -> {} {}".format(len(items), items))
        assert len(items) == 15, 'Problem with test_complex_get #4.'
        logger.info("END!!! test_complex_get")


    def test_post_404(self):
        logger.info("BEGIN: test_post_404")
        response = requests.post('http://127.0.0.1:8088/rest/services/hello-world/?a=1&b=2&c=3&d=4', json={})
        logger.info("test_post_404 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 404, 'Problem with test_post_404 #1.'
        assert data.get('status', '').find(' is undefined for POST.') > -1, 'Problem with test_post_404 #2.'
        logger.info("END!!! test_post_404")


    def test_post_200(self):
        logger.info("BEGIN: test_post_200")
        payload = {
            "args": [1,2,3,4,5,6],
            "name1": "one",
            "name2": "two",
            "name3": "three",
            "name4": "four"
        }

        response = requests.post('http://127.0.0.1:8088/rest/services/sample-one/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4', json=payload)
        logger.info("test_post_200 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_post_200 #1.'
        assert data.get('status') == 'OK', 'Problem with test_post_200 #2.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_post_200 :: items -> {} {}".format(len(items), items))
        assert len(items) == 20, 'Problem with test_post_200 #3.'
        logger.info("END!!! test_post_200")


    def test_put_200(self):
        logger.info("BEGIN: test_put_200")
        payload = {
            "args": [1,2,3,4,5,6],
            "name1": "one",
            "name2": "two",
            "name3": "three",
            "name4": "four"
        }

        response = requests.put('http://127.0.0.1:8088/rest/services/sample-one2/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4', json=payload)
        logger.info("test_put_200 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_put_200 #1.'
        assert data.get('status') == 'OK', 'Problem with test_put_200 #2.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_put_200 :: items -> {} {}".format(len(items), items))
        assert len(items) == 20, 'Problem with test_put_200 #3.'
        logger.info("END!!! test_put_200")


    def test_delete_200(self):
        logger.info("BEGIN: test_delete_200")
        payload = {
            "args": [1,2,3,4,5,6],
            "name1": "one",
            "name2": "two",
            "name3": "three",
            "name4": "four"
        }

        response = requests.delete('http://127.0.0.1:8088/rest/services/sample-one2a/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4', json=payload)
        logger.info("test_delete_200 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_delete_200 #1.'
        assert data.get('status') == 'OK', 'Problem with test_delete_200 #2.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_delete_200 :: items -> {} {}".format(len(items), items))
        assert len(items) == 20, 'Problem with test_delete_200 #3.'
        logger.info("END!!! test_delete_200")

    ###################################################################################################
    
    def test_module1_complex_get(self):
        logger.info("BEGIN: test_module1_complex_get")
        response = requests.get('http://127.0.0.1:8088/rest/services/module1/hello-world/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4')
        logger.info("test_module1_complex_get :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_module1_complex_get #1.'
        assert data.get('status') == 'OK', 'Problem with test_module1_complex_get #2.'
        assert len(data.get('response', {}).keys()) > 0, 'Problem with test_module1_complex_get #3.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_module1_complex_get :: items -> {} {}".format(len(items), items))
        assert len(items) == 16, 'Problem with test_module1_complex_get #4.'
        logger.info("END!!! test_module1_complex_get")


    def test_module1_post_404(self):
        logger.info("BEGIN: test_module1_post_404")
        response = requests.post('http://127.0.0.1:8088/rest/services/module1/hello-world/?a=1&b=2&c=3&d=4', json={})
        logger.info("test_module1_post_404 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 404, 'Problem with test_module1_post_404 #1.'
        assert data.get('status', '').find(' is undefined for POST.') > -1, 'Problem with test_module1_post_404 #2.'
        logger.info("END!!! test_module1_post_404")


    def test_module1_post_200(self):
        logger.info("BEGIN: test_module1_post_200")
        payload = {
            "args": [1,2,3,4,5,6],
            "name1": "one",
            "name2": "two",
            "name3": "three",
            "name4": "four"
        }

        response = requests.post('http://127.0.0.1:8088/rest/services/module1/sample-one/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4', json=payload)
        logger.info("test_module1_post_200 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_module1_post_200 #1.'
        assert data.get('status') == 'OK', 'Problem with test_module1_post_200 #2.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_module1_post_200 :: items -> {} {}".format(len(items), items))
        assert len(items) == 21, 'Problem with test_module1_post_200 #3.'
        logger.info("END!!! test_module1_post_200")


    def test_module1_put_200(self):
        logger.info("BEGIN: test_module1_put_200")
        payload = {
            "args": [1,2,3,4,5,6],
            "name1": "one",
            "name2": "two",
            "name3": "three",
            "name4": "four"
        }

        response = requests.put('http://127.0.0.1:8088/rest/services/module1/sample-one2/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4', json=payload)
        logger.info("test_module1_put_200 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_module1_put_200 #1.'
        assert data.get('status') == 'OK', 'Problem with test_module1_put_200 #2.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_module1_put_200 :: items -> {} {}".format(len(items), items))
        assert len(items) == 21, 'Problem with test_module1_put_200 #3.'
        logger.info("END!!! test_module1_put_200")


    def test_module1_delete_200(self):
        logger.info("BEGIN: test_module1_delete_200")
        payload = {
            "args": [1,2,3,4,5,6],
            "name1": "one",
            "name2": "two",
            "name3": "three",
            "name4": "four"
        }

        response = requests.delete('http://127.0.0.1:8088/rest/services/module1/sample-one2a/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4', json=payload)
        logger.info("test_module1_delete_200 :: response.status_code -> {}".format(response.status_code))
        data = response.json()
        assert response.status_code == 200, 'Problem with test_module1_delete_200 #1.'
        assert data.get('status') == 'OK', 'Problem with test_module1_delete_200 #2.'
        items = data.get('response', {}).get([k for k in data.get('response', {}).keys() if (k != 'response')][0], {}).get('kwargs', {}).keys()
        logger.info("test_module1_delete_200 :: items -> {} {}".format(len(items), items))
        assert len(items) == 21, 'Problem with test_module1_delete_200 #3.'
        logger.info("END!!! test_module1_delete_200")
    