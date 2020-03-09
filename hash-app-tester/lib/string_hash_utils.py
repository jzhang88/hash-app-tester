'''
Created on Mar 7, 2020

@author: Jianying Zhang
'''

import hashlib
import base64
import random
import string


def get_sha512_hashing(str):
    '''returns SHA512 hash for a given string'''
    sha = hashlib.sha512()
    sha.update(str.encode())
    return sha.digest()


def get_base64_encoding(byteString):
    '''returns BASE64 hash for a given string'''
    return base64.b64encode(byteString).decode() if type(byteString) == bytes else None


def gen_password(length=random.randint(8, 128)):
    '''generate a random password string for test cases'''
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for i in range(length))
    return password


if __name__ == '__main__':
    print(get_base64_encoding('abc'))
    print(gen_password())
