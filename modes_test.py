"""Tests of modes of the Encrypt Decrypt Command Line Tool"""
import os
import pathlib
from modes import Append, Encrypt, Decrypt

def test_encrypt():
    """Test of encrypt mode"""
    path = pathlib.Path('test.txt')
    with open (path, 'w', encoding='utf8') as file:
        file.write('Encryption Test')

    process = Encrypt(path, 'password')
    process.run()

    assert os.path.isfile('test.crp')

    with open ('test.crp', 'r', encoding='utf8') as file:
        encrypted_content = file.read()
        assert encrypted_content[0:9] == 'gAAAAABiw'

def test_append():
    """Test of append mode"""
    path = pathlib.Path('test.crp')
    process = Append(path, 'password', 'Append Test Text')
    process.run()

    assert os.path.isfile('test.crp')

def test_decrypt():
    """Test of decrypt mode"""
    path = pathlib.Path('test.crp')
    process = Decrypt(path, 'password')
    process.run()

    assert os.path.isfile('test.txt')

    with open ('test.txt', 'r', encoding='utf8') as file:
        decrypted_dontent = file.read()
        assert decrypted_dontent == 'Encryption Test\nAppend Test Text'

    os.remove('test.txt')
