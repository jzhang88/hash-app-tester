'''
Created on Mar 6, 2020

@author: Jianying Zhang
'''
import unittest
from datetime import datetime
import os
from requests import codes
from hashing_crud import post_hash, put_hash, del_hash
from string_hash_utils import gen_password


class TestPOST(unittest.TestCase):

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

    def test_valid_post_2000(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        response = post_hash(url, self.headers, payload)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(int(response.text), 0, 'Invalid Job Id Returned')

    def test_valid_post_returns_id_immediately_2010(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        before_post = datetime.now()
        response = post_hash(url, self.headers, payload)
        after_post = datetime.now()
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(int(response.text), 0, 'Invalid Job Id Returned')
        self.assertTrue((after_post - before_post).total_seconds()
                        < 5, 'Job Id Did not Return Immediately')

    def test_first_post_returns_job_id_one_2020_1000_1020_1030(self):
        new_port = 9099

        self._restart_app(9099)
        url = self.base_url + ':' + str(new_port) + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        response = post_hash(url, self.headers, payload)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertEqual(int(response.text), 1, 'Invalid Job Id Returned')

    def test_valid_post_increments_job_id_by_one_2030(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        response = post_hash(url, self.headers, payload)
        id1 = int(response.text)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(id1, 0, 'Invalid Job Id Returned')

        payload = {'password': 'angrybird'}
        response = post_hash(url, self.headers, payload)
        id2 = int(response.text)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(id2, 0, 'Invalid Job Id Returned')
        self.assertEqual(id2 - id1, 1, 'Wrong Job Id increment')

    def test_post_with_empty_password_2040(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': ''}
        response = post_hash(url, self.headers, payload)
        id = int(response.text)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(id, 0, 'Invalid Job Id Returned')

    def test_post_with_none_password_2050(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = "{'password': None}"
        response = post_hash(url, self.headers, payload)
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Malformed Input',
                         'Invalid Error Message')

    def test_post_without_password_2060(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'something': 'else'}
        response = post_hash(url, self.headers, payload)
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Malformed Input',
                         'Invalid Error Message')

    def test_post_with_non_string_password_2070(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = "{'password': abcd}"  # abcd without quotes
        response = post_hash(url, self.headers, payload)
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Malformed Input',
                         'Invalid Error Message')

    def test_post_with_long_password_2080(self):
        password = gen_password(2048)
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': password}
        response = post_hash(url, self.headers, payload)
        id = int(response.text)
        self.assertEqual(response.status_code, codes.OK, 'INVALID Status Code')
        self.assertGreater(id, 0, 'Invalid Job Id Returned')

    def test_post_password_with_special_chars_2090(self):
        special_chars = '! @#$%^&*()-_+=[{]}\|;:,./?'
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': special_chars}
        response = post_hash(url, self.headers, payload)
        id = int(response.text)
        self.assertEqual(response.status_code,
                         codes.OK, 'INVALID Status Code')
        self.assertGreater(id, 0, 'Invalid Job Id Returned')

    def test_post_password_in_other_language_2100(self):
        special_chars = 'パスワード'
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': special_chars}
        response = post_hash(url, self.headers, payload)
        id = int(response.text)
        self.assertEqual(response.status_code,
                         codes.OK, 'INVALID Status Code')
        self.assertGreater(id, 0, 'Invalid Job Id Returned')

    def test_post_with_invalid_payload_2110(self):
        invalid_payload = "{'password': }"
        url = self.base_url + ':' + self.port + '/' + 'hash'
        response = post_hash(url, self.headers, invalid_payload)
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Malformed Input',
                         'Invalid Error Message')

    def test_post_with_wrong_header_2120(self):
        payload = {'password': 'angrymonkey'}
        url = self.base_url + ':' + self.port + '/' + 'hash'
        wrong_headers = {'Content-Type': 'multipart/form-data'}
        response = post_hash(url, wrong_headers, payload)
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Malformed Input',
                         'Invalid Error Message')

    def test_post_with_wrong_header_2130(self):
        payload = None
        url = self.base_url + ':' + self.port + '/' + 'hash'
        wrong_headers = {'Content-Type': 'multipart/form-data'}
        response = post_hash(url, wrong_headers, payload)
        self.assertEqual(response.status_code,
                         codes.BAD_REQUEST, 'INVALID Status Code')
        self.assertEqual(response.text.strip(), 'Malformed Input',
                         'Invalid Error Message')

    def test_put_hash_not_supported_5000(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        payload = {'password': 'angrymonkey'}
        response = put_hash(url, self.headers, payload)
        self.assertEqual(response.status_code,
                         codes.NOT_ALLOWED, 'INVALID Status Code')

    def test_delete_hash_not_supported_5010(self):
        url = self.base_url + ':' + self.port + '/' + 'hash'
        response = del_hash(url)
        self.assertEqual(response.status_code,
                         codes.NOT_ALLOWED, 'INVALID Status Code')


if __name__ == "__main__":
    unittest.main()
