'''
Created on Mar 9, 2020

@author: Jianying Zhang
'''
import unittest
import os
import asyncio
from requests import codes
from hashing_crud import post_hash_async
from string_hash_utils import gen_password


class Test(unittest.TestCase):

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

    def test_verify_simultanenous_hashing_is_supported_7000(self):
        loop = asyncio.get_event_loop()
        tasks = []
        url = "http://127.0.0.1:8088/hash"
        TOTAL_REQ = 30  # Number of requests to send in parallel
        for i in range(TOTAL_REQ):
            pwd = gen_password(12)
            payload = {'password': pwd}
            task = asyncio.ensure_future(
                post_hash_async(url, self.headers, payload))
            tasks.append(task)
        finished = loop.run_until_complete(asyncio.wait(tasks))
        for task in finished:
            for response in task:
                print(response)
                print(response.result())
                self.assertEqual(response.result()[0],
                                 codes.OK, 'INVALID Status Code')
                self.assertGreater(int(response.result()[1]), 0,
                                   'Invalid Job Id Returned')

        loop.close()


if __name__ == "__main__":
    unittest.main()
