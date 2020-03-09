'''
Created on Mar 8, 2020

@author: Jianying Zhang
'''
import unittest
import os

import time
from requests import codes
from hashing_crud import post_hash, get_hash_stats, post_shutdown


class TestPostShutdown(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1'
        self.port = '8088'
        self.headers = {'Content-Type': 'application/json'}

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

    def test_post_shutdown_response_no_active_hashing_6000_6020(self):
        # make sure app is up
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        # shutdown app
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = 'shutdown'
        response = post_shutdown(url, None, payload)

        # verify the app is down
        time.sleep(1)
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        self.assertIn('No connection could be made because the target machine actively refused it',
                      str(response), 'App might Not be down')

    def test_post_shutdown_stops_app_gracefully_6010_6030(self):
        self._restart_app()
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        for i in range(5):
            response = post_hash(url, self.headers, payload, 1)
        payload = 'shutdown'
        response = post_shutdown(url, None, payload)
        # verify it shuts down gracefully when there are in-flight hashing
        self.assertEqual(response.status_code, codes.OK,
                         'Bug: INVALID Status Code')

        # verify stats reflects in-flight hashing before shutdown
        time.sleep(3)
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        job_count, avgTime = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertTrue(job_count >= 4, 'Invalid TotalRequests')

    def test_new_post_rejected_during_pending_shutdown_6040(self):
        self._restart_app()
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        for i in range(5):
            response = post_hash(url, self.headers, payload, 1)
        payload = 'shutdown'
        response = post_shutdown(url, None, payload)
        # verify it shuts down gracefully when there are in-flight hashing
        self.assertEqual(response.status_code, codes.OK,
                         'Bug: INVALID Status Code')

        # Verify new post hash is not accepted when shutdown is in progress
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        response = post_hash(url, self.headers, payload, 1)
        print(response.text)
        self.assertEqual(response.status_code,
                         codes.SERVICE_UNAVAILABLE, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Service Unavailable',
                         'Invalid Error Message')

        # verify stats reflects in-flight hashing before shutdown
        time.sleep(3)
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        job_count, avgTime = response.json()['TotalRequests'], response.json()[
            'AverageTime']
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertTrue(job_count >= 4, 'Invalid TotalRequests')


if __name__ == "__main__":
    unittest.main()
