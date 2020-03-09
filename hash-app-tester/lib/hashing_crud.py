'''
Created on Mar 6, 2020

@author: Jianying Zhang
'''

import json
import requests
from requests import codes
from aiohttp import ClientSession


def post_hash(url, headers, payload, timeout=10):
    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload), timeout=timeout)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def put_hash(url, headers, payload, timeout=10):
    try:
        response = requests.put(url, headers=headers,
                                data=json.dumps(payload), timeout=timeout)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def del_hash(url):
    try:
        response = requests.delete(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def post_shutdown(url, headers, payload):
    try:
        response = requests.post(url, headers=headers,
                                 data=payload)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def get_hash(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def get_hash_by_id(url, job_id):
    try:
        response = requests.get(url + '/' + str(job_id))
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def post_hash_by_id(job_id, url, headers, payload, timeout=10):
    try:
        response = requests.post(url + '/' + str(job_id), headers=headers,
                                 data=payload, timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def put_hash_by_id(job_id, url, headers, payload, timeout=10):
    try:
        response = requests.put(url + '/' + str(job_id), headers=headers,
                                data=payload, timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def del_hash_by_id(job_id, url):
    try:
        response = requests.delete(url + '/' + str(job_id))
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def post_hash_stats(url, headers, payload, timeout=10):
    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload), timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def put_hash_stats(url, headers, payload, timeout=10):
    try:
        response = requests.put(url, headers=headers,
                                data=json.dumps(payload), timeout=timeout)
        print(response)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def get_hash_stats(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


def del_hash_stats(url):
    try:
        response = requests.delete(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return e


async def post_hash_async(url, headers, payload):
    async with ClientSession() as session:
        async with session.post(url, headers=headers,
                                data=json.dumps(payload)) as response:
            content = await response.read()
            return response.status, content.decode()
