from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from vyperlogix.json import db

import os
import json

import logging
logger = logging.getLogger(__name__)

from pymongo import MongoClient

from vyperlogix.django import django_utils

def document_copy(doc):
    aDoc = {}
    try:
        for k in doc:
            aDoc[k] = doc[k] if (k != '_id') else str(doc[k])
    except:
        pass
    return aDoc


class RestAPI(APIView):
    """
    Handles New Project and other APIs with JSON response.
    """
    def get(self, request, format=None):
        response = {'method': request.method}
        response['GET'] = {}
        response['META'] = {}
        for k,v in request.META.items():
            response['META'][k] = str(v)
            
        for k,v in request.GET.items():
            response['GET'][k] = str(v)
        return Response(response, status=status.HTTP_200_OK, content_type='application/json')


    def get_payload(self, request):
        try:
            payload_data = json.loads(request.body)
        except Exception as ex:
            payload_data = {'exception' : ex}

        return payload_data

    
    def get_mongodb_connection(self, dbname=None):
        response = {}
        response['env'] = {}

        MONGO_URI = os.environ.get('MONGO_URI', default='')
        assert len(MONGO_URI) > 0, 'get_mongodb_connection :: (1) Problem with MONGO_URI ({}).'.format(MONGO_URI)
        response.get('env', {})['MONGO_URI'] = MONGO_URI

        mongo_user = os.environ.get('MONGO_user', default='')
        assert len(mongo_user) > 0, 'get_mongodb_connection :: (2) Problem with mongo_user ({}).'.format(mongo_user)
        response.get('env', {})['MONGO_user'] = mongo_user

        mongo_db = os.environ.get('MONGO_db', default='')
        assert len(mongo_db) > 0, 'get_mongodb_connection :: (3) Problem with mongo_db ({}).'.format(mongo_db)
        response.get('env', {})['MONGO_db'] = mongo_db

        mongo_authMechanism = os.environ.get('MONGO_auth', default='')
        assert len(mongo_authMechanism) > 0, 'get_mongodb_connection :: (4) Problem with mongo_authMechanism ({}).'.format(mongo_authMechanism)
        response.get('env', {})['MONGO_auth'] = mongo_authMechanism

        assert settings.MONGODB_DATABASES, 'Missing the settings.MONGODB_DATABASES ?'
        if (settings.MONGODB_DATABASES):
            password = settings.MONGODB_DATABASES.get('default', {}).get('password')
            assert password, 'Missing the password from settings.MONGODB_DATABASES ?'
            response['settings'] = settings.MONGODB_DATABASES

            try:
                response['client'] = MongoClient(MONGO_URI, username=mongo_user, password=password, authSource=mongo_db, authMechanism=mongo_authMechanism)
                response['db'] = response.get('client')[mongo_db  if ( (dbname is None) or (len(dbname) == 0) ) else dbname]
            except Exception as ex:
                response['exception'] = str(ex)
        return response
        

    def query(self, db, collection, key, doc_query):
        doc = db[collection].find_one({key: doc_query})
        return doc        


    def post(self, request, format=None):
        response = {'method':'post'}
        response['content_type'] = request.content_type
        response['method'] = request.method
        response['META'] = {}
        for k,v in request.META.items():
            response['META'][k] = str(v)

        payload_data = json.loads(request.body)
        try:
            response['data'] = payload_data
        except KeyError as ex:
            response['error'] = str(ex)

        return Response(response, status=status.HTTP_200_OK, content_type='application/json')


class MongoRestAPI(RestAPI):
    """
    Handles New Project and other APIs with JSON response.
    """
    def get(self, request, **kwargs):
        response = 'INVALID'
        return Response(response, status=status.HTTP_404_NOT_FOUND, content_type='text/html')

    def post(self, request, **kwargs):
        '''
        path('rest/mongodb/<slug:dbname>/<slug:collection>/<slug:key>/', mongo.MongoRestAPI.as_view()),
        
        POST http://127.0.0.1:8080/rest/mongodb/angularappgenerator/angularappgenerator/project-name/ HTTP/1.1
        content-type: application/json
        
        {
            "query": { "$regex" : "^\w" }
        }
        
        '''
        dbname = kwargs.get('dbname')
        collection = kwargs.get('collection')
        key = kwargs.get('key')
        logger.info('RestProjectAPI.get :: slug -> {}, collection -> {}, key -> {}'.format(dbname, collection, key))
        is_valid = lambda item:(item is not None) and (len(item) > 0)
        assert is_valid(dbname), '{} :: Missing dbname ({}).'.format(self.__class__, dbname)
        assert is_valid(collection), '{} :: Missing collection ({}).'.format(self.__class__, collection)
        
        data = self.get_payload(request)

        response = {}
        response["docs"] = []
        response["data"] = {}
        response['exception'] = ''
        for k,v in data.items():
            response.get('data', {})[k] = v
        doc_query = data.get('query')
        if (not is_valid(doc_query)):
            doc_query = {"$regex":".*"}

        is_deleting = False
        if (not is_valid(key)):
            key = [k for k in data.keys() if (k not in ['query'])][0]
            is_deleting = not is_valid(data.get(key))
            
        is_updating = is_valid(data.get(key))
        logger.debug('DEBUG: is_updating -> {}, is_deleting -> {}'.format(is_updating, is_deleting))

        mongo_connection = self.get_mongodb_connection(dbname=dbname)
        try:
            db = mongo_connection.get('db')
            assert db is not None, 'GET :: Mongo Connection issues ?'
            
            doc = self.query(db, collection, key, doc_query)
            if (not is_updating) and (not is_deleting):
                if (doc):
                    response.get('docs', []).append(document_copy(doc))
            else:
                __found__ = doc["_id"] if (doc is not None) else None
                if (is_updating):
                    if (__found__):
                        db[collection].find_one_and_update(
                            {"_id" : __found__},
                            {"$set":
                                {key: data.get(key)}
                            },upsert=True
                        )
                    else:
                        db[collection].insert_one({key: data.get(key)})
                elif (is_deleting):
                    db[collection].delete_one({"_id" : __found__})
                doc = self.query(db, collection, key, doc_query)
                if (doc):
                    response.get('docs', []).append(document_copy(doc))
        except Exception as ex:
            response['exception'] = str(ex)


        logger.debug('DEBUG: response -> ' + str(response))
        return Response(response, status=status.HTTP_200_OK, content_type='application/json')
