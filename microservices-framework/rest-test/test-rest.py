import os
import sys
import json
import requests

domain = '35.202.79.147'
uuid = '4a1bf01e-0693-48c5-a52b-fc275205c1d8'

def test_get1():
    items = ['status', 'has_plugins', 'modules', 'endpoints', 'imports', 'aliases']
    url = 'http://{}/rest/services/{}/__directory__/'.format(domain, uuid)

    resp = requests.get(url=url)
    data = resp.json()
    for item in items:
        assert data.get(item) is not None, 'Problem with {} in response.'.format(item)
    assert data.get('status') == 'OK', 'Problem with "status" in response. Expected "OK" but got {}.'.format(data.get('status'))
    print(json.dumps(data, indent=3))
    
def test_get2():
    items = ['status', 'has_plugins', 'modules', 'endpoints', 'imports', 'aliases']
    url = 'https://{}/rest/services/{}/__directory__/'.format(domain, uuid)

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
    items = ['status', 'has_plugins', 'modules', 'endpoints', 'imports', 'aliases']
    url = 'http://{}/rest/services/{}/__directory__/'.format(domain, uuid)

    resp = requests.get(url=url)
    data = resp.json()
    if (data.get('has_plugins', False)):
        the_modules = data.get('modules', {})
        print(json.dumps(the_modules, indent=3))
    


if (__name__ == '__main__'):
    if (0):
        for k,v in os.environ.items():
            print('{} : {}'.format(k, v))
        
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print('ip -> {}'.format(ip))
    
    sys.exit()
        
    test_get1()
    test_get2()
    test_get3()
    test_get4()
    test_modules()
