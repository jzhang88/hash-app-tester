'''
Created on Mar 7, 2020

@author: Jianying Zhang
'''
import unittest
from datetime import datetime
import os
import json
from requests import codes
from hashing_crud import post_hash, get_hash, get_hash_by_id, get_hash_stats
from string_hash_utils import gen_password, get_sha512_hashing,\
    get_base64_encoding


class TestGet(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1'
        self.port = '8088'
        self.headers = {'Content-Type': 'application/json'}
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

    def test_get_valid_job_id_works_5_seconds_after_hash_3010(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        pwd = gen_password(12)
        payload = {'password': pwd}
        before_post = datetime.now()
        response = post_hash(url, self.headers, payload)
        job_id = response.text
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(int(job_id), 0, 'Invalid Job Id Returned')
        sha512_hash = get_sha512_hashing(pwd)
        base64_hash = get_base64_encoding(sha512_hash)
        response = get_hash_by_id(url, job_id)
        after_post = datetime.now()
        time_delta = (after_post - before_post).total_seconds()
        self.assertTrue(5 < time_delta < 6,
                        'Job Id Did not Return Immediately')
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertEqual(response.text, base64_hash, 'Invalid Hash Returned')

    def test_get_valid_job_id_returns_correct_hash_3020(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        pwd = gen_password(12)
        payload = {'password': pwd}
        response = post_hash(url, self.headers, payload)
        job_id = response.text
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(int(job_id), 0, 'Invalid Job Id Returned')
        sha512_hash = get_sha512_hashing(pwd)
        base64_hash = get_base64_encoding(sha512_hash)
        response = get_hash_by_id(url, job_id)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertEqual(response.text, base64_hash, 'Invalid Hash Returned')

    def test_get_valid_job_id_returns_correct_hash_for_special_chars_3030(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        pwd = '! @#$%^&*()-_+=[{]}\|;:,./?'
        payload = {'password': pwd}
        response = post_hash(url, self.headers, payload)
        job_id = response.text
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(int(job_id), 0, 'Invalid Job Id Returned')
        sha512_hash = get_sha512_hashing(pwd)
        base64_hash = get_base64_encoding(sha512_hash)
        response = get_hash_by_id(url, job_id)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertEqual(response.text, base64_hash, 'Invalid Hash Returned')

    def test_get_valid_job_id_returns_correct_hash_for_long_password_3040(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        pwd = gen_password(2048)
        payload = {'password': pwd}
        response = post_hash(url, self.headers, payload)
        job_id = response.text
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(int(job_id), 0, 'Invalid Job Id Returned')
        sha512_hash = get_sha512_hashing(pwd)
        base64_hash = get_base64_encoding(sha512_hash)
        response = get_hash_by_id(url, job_id)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertEqual(response.text, base64_hash, 'Invalid Hash Returned')

    def test_get_valid_job_id_returns_correct_hash_i28n_3050(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        pwd = '密码'
        payload = {'password': pwd}
        response = post_hash(url, self.headers, payload)
        job_id = response.text
        self.assertEqual(response.status_code, codes.OK,
                         'INVALID Status Code')
        self.assertGreater(int(job_id), 0, 'Invalid Job Id Returned')
        sha512_hash = get_sha512_hashing(pwd)
        base64_hash = get_base64_encoding(sha512_hash)
        response = get_hash_by_id(url, job_id)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertEqual(response.text, base64_hash, 'Invalid Hash Returned')

    def test_get_hash_with_non_existing_job_id_3060(self):
        url = self.base_url + ':' + self.port + '/' + 'stats'
        response = get_hash_stats(url)
        if response.status_code == codes.OK:
            current_jobs = json.loads(response.text)['TotalRequests']
            print(current_jobs)
            url = self.base_url + ':' + self.port + '/' + 'hash'
            response = get_hash_by_id(url, current_jobs + 1000)
            self.assertEqual(response.status_code,
                             codes.BAD_REQUEST, 'INVALID Status Code')
            self.assertEqual(response.text.strip(),
                             'Hash not found', 'Invalid Error Message')
        else:
            self.fail('Failed to Get Hash Stats')

    def test_get_hash_with_non_digital_job_id_3070(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        response = get_hash_by_id(url,  'one')
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Invalid Syntax',
                         'Invalid Error Message')
        # BUG: Need to formalize the error message. Raw error message is returned:
        # strconv.Atoi: parsing "one": invalid syntax

    def test_get_hash_without_job_id_3080(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        response = get_hash(url)
        print(response)
        self.assertEqual(response.status_code,
                         codes.NOT_ALLOWED, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'GET Not Supported',
                         'Invalid Error Message')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
