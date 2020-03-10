'''
Created on Mar 6, 2020

@author: Jianying Zhang
'''

import json
import requests
from requests import codes
from aiohttp import ClientSession


def post_hash(url, headers, payload, timeout=10):
    '''base function for test cases to send post /hash'''
    if payload:
        payload = json.dumps(payload)
    try:
        response = requests.post(url, headers=headers,
                                 data=payload, timeout=timeout)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def put_hash(url, headers, payload, timeout=10):
    '''base function for test cases to send put /hash'''
    try:
        response = requests.put(url, headers=headers,
                                data=json.dumps(payload), timeout=timeout)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def del_hash(url):
    '''base function for test cases to send delete /hash'''
    try:
        response = requests.delete(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def post_shutdown(url, headers, payload):
    '''base function for test cases to send post shutdown'''
    try:
        response = requests.post(url, headers=headers,
                                 data=payload)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def get_hash(url):
    '''base function for test cases to send get /hash'''
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def get_hash_by_id(url, job_id):
    '''base function for test cases to send get /hash/<id>'''
    try:
        response = requests.get(url + '/' + str(job_id))
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def post_hash_by_id(job_id, url, headers, payload, timeout=10):
    '''base function for test cases to send post /hash/<id>'''
    try:
        response = requests.post(url + '/' + str(job_id), headers=headers,
                                 data=payload, timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def put_hash_by_id(job_id, url, headers, payload, timeout=10):
    '''base function for test cases to send put /hash/<id>'''
    try:
        response = requests.put(url + '/' + str(job_id), headers=headers,
                                data=payload, timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def del_hash_by_id(job_id, url):
    '''base function for test cases to send delete /hash/<id>'''
    try:
        response = requests.delete(url + '/' + str(job_id))
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def post_hash_stats(url, headers, payload, timeout=10):
    '''base function for test cases to send post /hash/stats'''
    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload), timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def put_hash_stats(url, headers, payload, timeout=10):
    '''base function for test cases to send put /hash/stats'''
    try:
        response = requests.put(url, headers=headers,
                                data=json.dumps(payload), timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def get_hash_stats(url):
    '''base function for test cases to send get /hash/stats'''
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def del_hash_stats(url):
    '''base function for test cases to send delete /hash/stats'''
    try:
        response = requests.delete(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


async def post_hash_async(url, headers, payload):
    '''base function for test cases to send multiple post /hash in parallel'''
    async with ClientSession() as session:
        async with session.post(url, headers=headers,
                                data=json.dumps(payload)) as response:
            content = await response.read()
            return response.status, content.decode()
