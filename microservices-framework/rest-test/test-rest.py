import os
import sys
import json
import random
import requests

lib_path = '/workspaces/private_vyperlogix_lib3'
if (not any([f == lib_path for f in sys.path])):
    sys.path.insert(0, lib_path)

domain = '35.202.79.147'
uuid = '4a1bf01e-0693-48c5-a52b-fc275205c1d8'

def test_get1():
    items = ['status', 'has_plugins', 'modules', 'endpoints', 'imports', 'aliases']
    url = 'http://{}/rest/services/{}/__directory__/?DEBUG=1'.format(domain, uuid)

    resp = requests.get(url=url)
    data = resp.json()
    for item in items:
        assert data.get(item) is not None, 'Problem with {} in response.'.format(item)
    assert data.get('status') == 'OK', 'Problem with "status" in response. Expected "OK" but got {}.'.format(data.get('status'))
    print(json.dumps(data, indent=3))
    
def test_get2():
    items = ['status', 'has_plugins', 'modules', 'endpoints', 'imports', 'aliases']
    url = 'https://{}/rest/services/{}/__directory__/?DEBUG=1'.format(domain, uuid)

    resp = requests.get(url=url, verify=False)
    data = resp.json()
    for item in items:
        assert data.get(item) is not None, 'Problem with {} in response.'.format(item)
    assert data.get('status') == 'OK', 'Problem with "status" in response. Expected "OK" but got {}.'.format(data.get('status'))
    print(json.dumps(data, indent=3))
    

def test_get3():
    items = ['status', 'response']
    url = 'https://{}/rest/services/{}/module1/__dir__/'.format(domain, uuid)

    resp = requests.get(url=url, verify=False)
    data = resp.json()
    for item in items:
        assert data.get(item) is not None, 'Problem with {} in response.'.format(item)
    assert data.get('status') == 'OK', 'Problem with "status" in response. Expected "OK" but got {}.'.format(data.get('status'))
    print(json.dumps(data, indent=3))
    print(data.keys())
    

def test_get4():
    items = ['status', 'response']
    url = 'https://{}/rest/services/{}/hello-world/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4'.format(domain, uuid)

    __kwargs__ = {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "p1": "1",
        "p2": "2",
        "p3": "3",
        "p4": "4",
        "p5": "5",
        "p6": "6",
        "p7": "7",
        "p8": "8",
        "p9": "9",
        "p10": "10"
        }

    resp = requests.get(url=url, verify=False)
    data = resp.json()
    for item in items:
        assert data.get(item) is not None, 'Problem with {} in response.'.format(item)
    assert data.get('status') == 'OK', 'Problem with "status" in response. Expected "OK" but got {}.'.format(data.get('status'))
    print('='*30)
    print(data.get('response', {}).keys())
    print(json.dumps(data.get('response', {}), indent=3))
    print('='*30)
    d = data.get('response', {})
    k = list(d.keys())[0]
    assert d.get(k, {}).get('response') == 'hello-world', 'Problem with "status" in response. Expected "hello-world" but got {}.'.format(data.get('response', {}).get('response'))
    for k,v in __kwargs__.items():
        fetch = lambda bucket, k:bucket.get('response', {}).get(list(bucket.get('response', {}).keys())[0]).get('kwargs', {}).get(k)
        print('{} -> {} : {}? '.format(list(data.get('response', {}).keys())[0], k, v),)
        assert fetch(data, k) == v, 'Problem with {} in response.  Expected {} but got  {}.'.format(k,v,fetch(data, k))
    print(json.dumps(data, indent=3))
    print(data.keys())
    

def test_modules():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    

    items = ['status', 'has_plugins', 'modules', 'endpoints', 'imports', 'aliases']
    url = 'https://{}/rest/services/{}/__directory__/?DEBUG=1'.format(domain, uuid)

    resp = requests.get(url=url, verify=False)
    data = resp.json()
    verified_urls = []
    if (data.get('has_plugins', False)):
        the_modules = data.get('modules', {})
        module_names = list(the_modules.keys())
        for name in module_names:
            the_module_endpoints = data.get('endpoints', {}).get(name, {}).get('GET', {})
            for k,v in the_module_endpoints.items():
                __url__ = 'https://{}/rest/services/{}/{}/{}/'.format(domain, uuid, name, k)
                print(__url__)
                __resp__ = requests.get(url=__url__, verify=False)
                __data__ = __resp__.json()
                print(json.dumps(__data__, indent=3))
                assert __data__.get('status') == 'OK', 'Problem with "{}", expected status of "OK" but got {}.'.format(__url__, __data__.get('status'))
                verified_urls.append(__url__)
                print('-'*30)
            print('='*30)
            
        import time
        
        class MyTimer(object):
            
            def __enter__(self):
                self.start = time.time()
                return self

            def __exit__(self, typ, value, traceback):
                self.duration = time.time() - self.start
        
        from vyperlogix.threads import pooled
        from vyperlogix.decorators import executor

        __executor = pooled.BoundedExecutor(200, 2000)

        @executor.threaded(__executor)
        def do_rest_work(url, vector):
            print(url)
            response = requests.get(url=url, verify=False)
            d = response.json()
            try:
                assert d.get('status') == 'OK', 'Problem with "{}", expected status of "OK" but got {}.'.format(u, d.get('status'))
                vector['num_worked'] = vector.get('num_worked', 0) + 1
            except:
                vector['num_failures'] = vector.get('num_failures', 0) + 1
            finally:
                vector['num_attempts'] = vector.get('num_attempts', 0) + 1

        with MyTimer() as timer:
            d = {}
            d['num_worked'] = 0
            d['num_attempts'] = 0
            d['num_failures'] = 0
            __stats__ = 'stats'
            d[__stats__] = {}
            for i in range(1000):
                k = random.randint(0, len(verified_urls)-1)
                u = verified_urls[k]
                d.get(__stats__, {})[u] = d.get(__stats__, {}).get(u, 0) + 1
                do_rest_work(u, d)
            __executor.shutdown()

        print('num_attempts = {}'.format(d.get('num_attempts', 0)))
        print('num_worked   = {}'.format(d.get('num_worked', 0)))
        print('num_failures = {}'.format(d.get('num_failures', 0)))
        print('stats = {}'.format(d.get(__stats__, {})))
        print('Elapsed Time: {}'.format(timer.duration))
        print('Velocity: {}'.format((d.get('num_attempts', 0) - d.get('num_failures', 0)) / timer.duration))
        assert d.get('num_failures', -1) == 0, 'Problem with num_failures, expected 0 but got {}.'.format(d.get('num_failures', -1))



if (__name__ == '__main__'):
    if (0):
        for k,v in os.environ.items():
            print('{} : {}'.format(k, v))
        
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print('ip -> {}'.format(ip))
    
    if (0):
        test_get1()
        test_get2()
        test_get3()
        test_get4()
    test_modules()
