'''
Created on Mar 8, 2020

@author: Jianying Zhang
'''
import unittest
import os

import time
import json
import jsonschema
from requests import codes
from hashing_crud import post_hash, get_hash_stats, post_hash_stats, put_hash_stats, del_hash_stats
from string_hash_utils import gen_password


class TestGetStats(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1'
        self.port = '8088'
        self.headers = {'Content-Type': 'application/json'}
        PATH = os.path.dirname(os.path.abspath(__file__))
        SCHEMA_PATH = os.path.join(PATH, '..\schema\hash_stats.json')
        with open(SCHEMA_PATH) as f:
            self.stats_schema = json.load(f)
        print(self.stats_schema)
        # TODO: start app

    @staticmethod
    def _restart_app(port=8088):
        os.environ['PORT'] = str(port)
        p = os.system(
            'start /min C:\\tmp\\jumpcloud\\broken-hashserve_win.exe')

    @staticmethod
    def _terminate_app():
        os.system("TASKKILL /F /IM broken-hashserve_win.exe")

    @classmethod
    def setUpClass(cls):
        cls._restart_app()

    @classmethod
    def tearDownClass(cls):
        cls._terminate_app()

    def test_get_hash_stats_returns_properly_when_no_job_exists_4000(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        # validate reponse against the json schema
        jsonschema.validate(response.json(), self.stats_schema)
        self.assertEqual(
            response.json()['TotalRequests'], 0, 'Invalid Initial Value for TotalRequests')
        self.assertEqual(
            response.json()['AverageTime'], 0, 'Invalid Initial Value for AverageTime')

    def test_get_hash_stats_returns_properly_4010(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        # validate reponse against the json schema
        jsonschema.validate(response.json(), self.stats_schema)
        job_count, avgTime = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        if job_count > 0:
            self.assertTrue(
                avgTime > 0, 'Invalid AverageTime Returned in Stats')

    def test_get_hash_stats_returns_updated_stats_4020(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        # validate reponse against the json schema
        jsonschema.validate(response.json(), self.stats_schema)
        job_count, avgTime = response.json()['TotalRequests'], response.json()[
            'AverageTime']

        for i in range(3):
            password = gen_password()
            post_url = self.base_url + ':' + self.port + '/' + 'hash'
            payload = {'password': password}
            post_hash(post_url, self.headers, payload)

        time.sleep(5)
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        # validate reponse against the json schema
        jsonschema.validate(response.json(), self.stats_schema)
        new_job_count, avgTime = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        self.assertEqual(new_job_count, job_count + 3,
                         'Invalid TotalRequests Returned')
        self.assertTrue(
            avgTime > 0, 'BUG: Invalid AverageTime Returned in Stats')

    def test_post_stats_not_supported_5050(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        # Get current stats
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        job_count1, avgTime1 = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        payload = {"TotalRequests": 999999999, "AverageTime": 100000000}
        # verify post stats is not supported
        response = post_hash_stats(url, self.headers, payload)
        self.assertEqual(response.status_code,
                         codes.NOT_ALLOWED, 'INVALID Status Code')
        # verify stats are not changed
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        job_count2, avgTime2 = response.json()['TotalRequests'], response.json()[
            'AverageTime']

    def test_put_stats_not_supported_5060(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        # Get current stats
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        job_count1, avgTime1 = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        payload = {"TotalRequests": 999999999, "AverageTime": 100000000}
        # verify post stats is not supported
        response = put_hash_stats(url, self.headers, payload)
        self.assertEqual(response.status_code,
                         codes.NOT_ALLOWED, 'INVALID Status Code')
        # verify stats are not changed
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        job_count2, avgTime2 = response.json()['TotalRequests'], response.json()[
            'AverageTime']

    def test_delete_stats_not_supported_5070(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        # Get current stats
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        job_count1, avgTime1 = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        payload = {"TotalRequests": 999999999, "AverageTime": 100000000}
        # verify delete stats is not supported
        response = del_hash_stats(url)
        self.assertEqual(response.status_code,
                         codes.NOT_ALLOWED, 'INVALID Status Code')
        # verify stats are not changed
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        job_count2, avgTime2 = response.json()['TotalRequests'], response.json()[
            'AverageTime']


if __name__ == "__main__":
    unittest.main()
