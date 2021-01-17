__copyright__ = """\
(c). Copyright 2008-2020, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 



THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os
from vyperlogix.decorators import expose

from vyperlogix.json import db

from django.conf import settings

__alias__ = "tenant-api"  # this is the module's alias wwhich couldl also be a version identifier to support API Versioning.
__ID__ = ''  # place your Tenant ID here. you get this when you register as a Tenant.
# Be careful to whom you grant access to this API.  This API is an Administrative API that allows Tenants to be Registered, Disabled or Removed.
# The __ID__ should be the ADMIN_ID and not a typical Tenant ID.

@expose.endpoint(method=['POST'], API='___register___')
def register_tenant(*args, **kwargs):
    '''
    This API registeres a new Tenant and makes the new Tenant Active.
    
    Tenants are identified via their email address.  Tenant Registration sends an email to the email address and invites the Tenant
    to click a link to activate their registration.
    '''
    import uuid
    response = {}
    is_registered = False
    print('*** kwargs -> {}'.format(kwargs))
    payload = kwargs.get('__body__', {})
    __userid__ = payload.get('userid')
    __uuid__ = payload.get('uuid', str(uuid.uuid4()))
    uuid = kwargs.get('uuid')
    __is_admin__ = db.is_uuid_admin(uuid)
    __is__ = db.is_userid_or_uuid(__userid__, __uuid__)
    print('(1) register_tenant :: __is_admin__ -> {}, __is__ -> {}'.format(__is_admin__, __is__))
    if (__is_admin__) and (not __is__):
        print('(2) register_tenant :: __is_admin__ -> {}, __is__ -> {}'.format(__is_admin__, __is__))
        is_registered = db.register_as_new_tenant(__userid__, __uuid__)
    
    response['args'] = {}
    for i, arg in enumerate(args):
        response.get('args', {})[i] = arg
    response['kwargs'] = {}
    for k,v in kwargs.items():
        if (k not in ['__request__']):
            response.get('kwargs', {})[k] = v
    response['__is__'] = __is__
    response['is_registered'] = is_registered
    return response


@expose.endpoint(method=['GET'], API='___list___')
def list_tenants(*args, **kwargs):
    '''
    This API lists current Tenants.
    
    '''
    response = {}
    uuid = kwargs.get('uuid')
    __is__ = db.is_uuid_admin(uuid)
    if (__is__):
        response['tenants'] = db.get_tenants()
    
    response['args'] = {}
    for i, arg in enumerate(args):
        response.get('args', {})[i] = arg
    response['kwargs'] = {}
    for k,v in kwargs.items():
        if (k not in ['__request__']):
            response.get('kwargs', {})[k] = v
    response['__is__'] = __is__
    return response


@expose.endpoint(method=['DELETE'], API='___remove___')
def remove_tenant(*args, **kwargs):
    '''
    This API deletes current Tenant by uuid.
    
    '''
    response = {}
    is_removed = False
    payload = kwargs.get('__body__', {})
    __userid__ = payload.get('userid')
    __uuid__ = payload.get('uuid')
    uuid = kwargs.get('uuid')
    __is_admin__ = db.is_uuid_admin(uuid)
    __is__ = db.is_uuid_registered(__uuid__)
    print('*** remove_tenant :: __uuid__ -> {}, __is__ -> {}'.format(__uuid__, __is__))
    if (__is_admin__) and (__is__):
        is_removed = db.remove_tenant(__uuid__)
    
    response['args'] = {}
    for i, arg in enumerate(args):
        response.get('args', {})[i] = arg
    response['kwargs'] = {}
    for k,v in kwargs.items():
        if (k not in ['__request__']):
            response.get('kwargs', {})[k] = v
    response['is_removed'] = is_removed
    return response


@expose.endpoint(method=['POST'], API='___enable___')
def enable_tenant(*args, **kwargs):
    '''
    This API enables current Tenant by uuid.
    
    '''
    response = {}
    is_enabled = False
    payload = kwargs.get('__body__', {})
    __uuid__ = payload.get('uuid')
    uuid = kwargs.get('uuid')
    __is_admin__ = db.is_uuid_admin(uuid)
    __is__ = db.is_uuid_registered(__uuid__)
    print('*** enable_tenant :: __uuid__ -> {}, __is__ -> {}'.format(__uuid__, __is__))
    if (__is_admin__) and (__is__):
        is_enabled = db.enable_tenant(__uuid__)
    
    response['args'] = {}
    for i, arg in enumerate(args):
        response.get('args', {})[i] = arg
    response['kwargs'] = {}
    for k,v in kwargs.items():
        if (k not in ['__request__']):
            response.get('kwargs', {})[k] = v
    response['is_enabled'] = is_enabled
    return response


@expose.endpoint(method=['POST'], API='___disable___')
def disable_tenant(*args, **kwargs):
    '''
    This API disablesa Tenant by uuid.
    
    '''
    response = {}
    is_disabled = False
    payload = kwargs.get('__body__', {})
    __uuid__ = payload.get('uuid')
    uuid = kwargs.get('uuid')
    __is_admin__ = db.is_uuid_admin(uuid)
    __is__ = db.is_uuid_registered(__uuid__)
    print('*** disable_tenant :: __uuid__ -> {}, __is__ -> {}'.format(__uuid__, __is__))
    if (__is_admin__) and (__is__):
        is_disabled = db.disable_tenant(__uuid__)
    
    response['args'] = {}
    for i, arg in enumerate(args):
        response.get('args', {})[i] = arg
    response['kwargs'] = {}
    for k,v in kwargs.items():
        if (k not in ['__request__']):
            response.get('kwargs', {})[k] = v
    response['is_disabled'] = is_disabled
    return response

