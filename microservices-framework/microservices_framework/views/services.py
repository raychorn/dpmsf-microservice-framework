from importlib import import_module
from os.path import splitext
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

import os
import json

import sys
import traceback

from vyperlogix.django import django_utils

from .mongo import RestAPI

from django.conf import settings

from vyperlogix.json import db
from vyperlogix.decorators import expose
from vyperlogix.django.services import ServiceRunner

from vyperlogix.django.django_utils import get_url_parms

class RestServicesAPI(RestAPI):
    """
    Microservice Architecture that deployes Python Modules via REST End-points.
    """
    def get_runner(self, uuid):
        fp_root = os.path.dirname(__file__)
        fp_plugins = os.sep.join([fp_root, 'plugins'])
        has_plugins = os.path.exists(fp_plugins) and os.path.isdir(fp_plugins)
        if (not has_plugins):
            os.mkdir(fp_plugins)
            has_plugins = os.path.exists(fp_plugins) and os.path.isdir(fp_plugins)
        fp_plugins_initpy = os.sep.join([fp_plugins, '__init__.py'])
        if (not (os.path.exists(fp_plugins_initpy) and (os.path.isfile(fp_plugins_initpy)))):
            with open(fp_plugins_initpy, 'w') as fOut:
                fOut.write('{}\n'.format('#'*40))
                fOut.write('# (c). Copyright, Vyper Logix Corp, All Rights Reserved.\n')
                fOut.write('{}\n'.format('#'*40))
                fOut.write('\n\n')
                fOut.flush()
        return ServiceRunner(fp_plugins, uuid)

    
    def get(self, request, *args, **kwargs):
        from django.conf import settings
        DEBUG = getattr(settings, "DEBUG", False)
        func = kwargs.get('func')
        uuid = kwargs.get('uuid')
        print('*** uuid -> {}'.format(uuid))
        admin_id = db.get_admin_id()
        print('*** admin_id -> {}'.format(admin_id))
        response = {'status' : 'OK'}
        try:
            if (func == '__directory__'):
                if (uuid == admin_id):
                    response['fpath'] = fp_root = os.path.dirname(__file__)
                    fp_plugins = os.sep.join([fp_root, 'plugins'])
                    response['has_plugins'] = has_plugins = os.path.exists(fp_plugins) and os.path.isdir(fp_plugins)
                    if (not has_plugins):
                        os.mkdir(fp_plugins)
                        response['has_plugins'] = has_plugins = os.path.exists(fp_plugins) and os.path.isdir(fp_plugins)
                    fp_plugins_initpy = os.sep.join([fp_plugins, '__init__.py'])
                    if (not (os.path.exists(fp_plugins_initpy) and (os.path.isfile(fp_plugins_initpy)))):
                        with open(fp_plugins_initpy, 'w') as fOut:
                            fOut.write('{}\n'.format('#'*40))
                            fOut.write('# (c). Copyright, Vyper Logix Corp, All Rights Reserved.\n')
                            fOut.write('{}\n'.format('#'*40))
                            fOut.write('\n\n')
                            fOut.flush()
                    runner = ServiceRunner(fp_plugins, admin_id)
                    if (DEBUG):
                        response['modules'] = runner.modules
                        response['endpoints'] = expose.get_endpoints()
                        response['imports'] = runner.imports
                        response['aliases'] = runner.aliases
                        response['status'] = 'OK'
                else:
                    response= {} # no response when the uuid is missing or invalid.
                    return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
            else:
                url_parm_analysis = get_url_parms(db=db)
                url_parm_to_alias = url_parm_analysis.get('->', {})
                url_parm_alias_to_original = url_parm_analysis.get('<-', {})

                runner = self.get_runner(uuid)
                if (func in runner.modules.keys()) or (func in runner.aliases):
                    func = kwargs.get(url_parm_to_alias.get('URL_PARM1', ''))
                endpoints = expose.get_endpoints()
                d = endpoints.get(request.method, {}).get(func, None)
                if ( (d is not None) and (kwargs.get('module', None) is None) ) or ( (d is not None) and (d.get('module') == kwargs.get('module')) ):
                    func_name = d.get('func')
                    module_alias = runner.aliases.get(d.get('module'))
                    module_name = d.get('module') if ((module_alias is None) or (len(module_alias) == 0)) else module_alias
                    if (func_name is None) or (module_name is None):
                        response['status'] = '{} is undefined.'.format(func)
                        return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
                    data = {}
                    data['__request__'] = request
                    for k,v in request.query_params.items():
                        data[k] = v
                    for k,v in kwargs.items():
                        data[k] = v
                    response['response'] = runner.exec(module_name, func_name, **data)
                else:
                    modules = runner.modules
                    func = kwargs.get('func')
                    param1 = kwargs.get(url_parm_to_alias.get('URL_PARM1', ''))
                    __is__ = (modules.get(func, None) != None) and (param1 == '__dir__')
                    if (__is__) and (db.is_uuid_admin(uuid)):
                        endpoints = expose.get_endpoints()
                        module_endpoints = endpoints.get(func, {})
                        response['response'] = module_endpoints
                    else:
                        __in__ = ' in {}'.format(kwargs.get('module'))
                        response['status'] = '{} is undefined for {}{}.'.format(func, request.method, __in__ if (kwargs.get('module')) else '')
                        return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        except Exception as ex:
            extype, ex, tb = sys.exc_info()
            formatted = traceback.format_exception_only(extype, ex)[-1]
            for l in traceback.format_exception(extype, ex, tb):
                print(l.rstrip())
            response = {}
            response['exception'] = formatted
            return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        return Response(response, status=status.HTTP_200_OK, content_type='application/json')


    def post(self, request, **kwargs):
        print('*** kwargs -> {}'.format(kwargs))
        func = kwargs.get('func')
        uuid = kwargs.get('uuid')
        print('*** uuid -> {}'.format(uuid))

        response = {'status' : 'OK'}
        __body__ = self.get_payload(request)
        __map__ = __body__.get('__map__', {})
        if ('__map__' in __body__.keys()):
            del __body__['__map__']
        response["response"] = {}
        runner = self.get_runner(uuid)

        url_parm_analysis = get_url_parms(db=db)
        url_parm_to_alias = url_parm_analysis.get('->', {})
        url_parm_alias_to_original = url_parm_analysis.get('<-', {})
        try:
            endpoints = expose.get_endpoints()
            if (func in runner.modules.keys()) or (func in runner.aliases):
                func = kwargs.get(url_parm_to_alias.get('URL_PARM1', ''))
            d = endpoints.get(request.method, {}).get(func, None)
            if (d is not None):
                func_name = d.get('func')
                module_alias = runner.aliases.get(d.get('module'))
                module_name = d.get('module') if ((module_alias is None) or (len(module_alias) == 0)) else module_alias
                if (func_name is None) or (module_name is None):
                    response['status'] = '{} is undefined.'.format(func)
                    return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
                data = {}
                data['__body__'] = __body__
                for k,v in request.query_params.items():
                    data[k] = v
                for k,v in kwargs.items():
                    k = __map__.get(k, k)
                    data[k] = v
                print('*** request -> {}'.format(data.get('__request__', {}).__class__.__name__))
                print('DEBUG: data -> {}'.format(['{} -> {}\n'.format(k,v) for k,v in data.items()]))
                data['__request__'] = request
                val = runner.exec(module_name, func_name, **data)
                response['response'] = val
            else:
                response['status'] = '{} is undefined for {}.'.format(func, request.method)
                return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        except Exception as ex:
            extype, ex, tb = sys.exc_info()
            formatted = traceback.format_exception_only(extype, ex)[-1]
            print('BEGIN: Exception')
            for l in traceback.format_exception(extype, ex, tb):
                print(l.rstrip())
            print('END!!! Exception')
            response = {}
            response['exception'] = formatted
            return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        return Response(response, status=status.HTTP_200_OK, content_type='application/json')


    def put(self, request, **kwargs):
        return self.post(request, **kwargs)


    def delete(self, request, **kwargs):
        return self.post(request, **kwargs)

    def options(self, request, **kwargs):
        response = {}
        response['status'] = 'Not Allowed.'
        return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='application/json')