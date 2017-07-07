# coding: utf-8

"""
    RiseML API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.1.0
    Contact: contact@riseml.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class AdminApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def get_nodes(self, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_nodes(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[Node]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_nodes_with_http_info(**kwargs)
        else:
            (data) = self.get_nodes_with_http_info(**kwargs)
            return data

    def get_nodes_with_http_info(self, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_nodes_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[Node]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_nodes" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        resource_path = '/nodes'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['api_key']

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[Node]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            collection_formats=collection_formats)

    def get_users(self, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_users(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[User]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_users_with_http_info(**kwargs)
        else:
            (data) = self.get_users_with_http_info(**kwargs)
            return data

    def get_users_with_http_info(self, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_users_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[User]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_users" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        resource_path = '/users'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['api_key']

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[User]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            collection_formats=collection_formats)

    def update_or_create_node(self, id, hostname, cpus, mem, gpus, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_or_create_node(id, hostname, cpus, mem, gpus, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id:  (required)
        :param str hostname:  (required)
        :param int cpus:  (required)
        :param int mem:  (required)
        :param int gpus:  (required)
        :return: list[Node]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_or_create_node_with_http_info(id, hostname, cpus, mem, gpus, **kwargs)
        else:
            (data) = self.update_or_create_node_with_http_info(id, hostname, cpus, mem, gpus, **kwargs)
            return data

    def update_or_create_node_with_http_info(self, id, hostname, cpus, mem, gpus, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_or_create_node_with_http_info(id, hostname, cpus, mem, gpus, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id:  (required)
        :param str hostname:  (required)
        :param int cpus:  (required)
        :param int mem:  (required)
        :param int gpus:  (required)
        :return: list[Node]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'hostname', 'cpus', 'mem', 'gpus']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_or_create_node" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_or_create_node`")
        # verify the required parameter 'hostname' is set
        if ('hostname' not in params) or (params['hostname'] is None):
            raise ValueError("Missing the required parameter `hostname` when calling `update_or_create_node`")
        # verify the required parameter 'cpus' is set
        if ('cpus' not in params) or (params['cpus'] is None):
            raise ValueError("Missing the required parameter `cpus` when calling `update_or_create_node`")
        # verify the required parameter 'mem' is set
        if ('mem' not in params) or (params['mem'] is None):
            raise ValueError("Missing the required parameter `mem` when calling `update_or_create_node`")
        # verify the required parameter 'gpus' is set
        if ('gpus' not in params) or (params['gpus'] is None):
            raise ValueError("Missing the required parameter `gpus` when calling `update_or_create_node`")


        collection_formats = {}

        resource_path = '/nodes'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'id' in params:
            form_params.append(('id', params['id']))
        if 'hostname' in params:
            form_params.append(('hostname', params['hostname']))
        if 'cpus' in params:
            form_params.append(('cpus', params['cpus']))
        if 'mem' in params:
            form_params.append(('mem', params['mem']))
        if 'gpus' in params:
            form_params.append(('gpus', params['gpus']))

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['multipart/form-data'])

        # Authentication setting
        auth_settings = ['api_key']

        return self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[Node]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            collection_formats=collection_formats)

    def update_or_create_user(self, username, email, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_or_create_user(username, email, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str username:  (required)
        :param str email:  (required)
        :return: list[User]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.update_or_create_user_with_http_info(username, email, **kwargs)
        else:
            (data) = self.update_or_create_user_with_http_info(username, email, **kwargs)
            return data

    def update_or_create_user_with_http_info(self, username, email, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.update_or_create_user_with_http_info(username, email, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str username:  (required)
        :param str email:  (required)
        :return: list[User]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['username', 'email']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_or_create_user" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'username' is set
        if ('username' not in params) or (params['username'] is None):
            raise ValueError("Missing the required parameter `username` when calling `update_or_create_user`")
        # verify the required parameter 'email' is set
        if ('email' not in params) or (params['email'] is None):
            raise ValueError("Missing the required parameter `email` when calling `update_or_create_user`")


        collection_formats = {}

        resource_path = '/users'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'username' in params:
            form_params.append(('username', params['username']))
        if 'email' in params:
            form_params.append(('email', params['email']))

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['multipart/form-data'])

        # Authentication setting
        auth_settings = ['api_key']

        return self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[User]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            collection_formats=collection_formats)
