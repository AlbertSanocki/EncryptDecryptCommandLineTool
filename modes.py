"""Commandline tool modes of operation"""
import base64
from threading import Thread
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Resources(Thread):
    '''resources needed to encryption and decryption of file.
    '''
    def __init__(self, path, password):
        self.password = password
        self.path = path
        Thread.__init__(self)

    @staticmethod
    def create_key(password):
        """Create key to Fernet"""
        salt = b'SZ3Z?v=D#1SGcsHw6kuCAe3SxKTRyRqxzG1KQRtTxA8j?nwe?i#zco04w0YSM5a:4eFNoeULfh7!NSBGP-bLV50X1pJxY2jUDc+D'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode('utf8')))

class Append(Resources):
    """Decrypt a file, type and add text to that file then encrypt it again"""
    def __init__(self,path, password, text):
        self.text = text
        super().__init__(path, password)

    def run(self):
        try:
            with open(self.path, 'r',encoding='utf8') as file:
                data_to_decrypt = file.read()

            fernet = Fernet(self.create_key(self.password))
            decrypted_data = fernet.decrypt(data_to_decrypt.encode('utf8'))
            new_data_to_encrypt = decrypted_data.decode('utf8') + '\n' + self.text
            encrypted_data = fernet.encrypt(new_data_to_encrypt.encode('utf8'))

            with open(self.path, 'w',encoding='utf8') as file:
                file.write(encrypted_data.decode('utf8'))
        except InvalidToken:
            print(f'Błędne hasło dla pliku: {self.path}')

class Decrypt(Resources):
    """Decrypt file using its path"""
    def run(self):
        try:
            with open(self.path, 'r',encoding='utf8') as file:
                data_to_decrypt = file.read()

            fernet = Fernet(self.create_key(self.password))
            decrypted_data = fernet.decrypt(data_to_decrypt.encode('utf8'))

            with open(self.path.rename(self.path.with_suffix('.txt')), 'w',encoding='utf8') as file:
                file.write(decrypted_data.decode('utf8'))
        except InvalidToken:
            print(f'Błędne hasło dla pliku: {self.path}')

class Encrypt(Resources):
    """Encrypt file using its path. Change sufix to .crp"""
    def run(self):
        try:
            with open(self.path, 'r',encoding='utf8') as file:
                data_to_encrypt = file.read()

            fernet = Fernet(self.create_key(self.password))
            encrypted_data = fernet.encrypt(data_to_encrypt.encode('utf8'))

            with open(self.path.rename(self.path.with_suffix('.crp')),'w',encoding='utf8') as file:
                file.write(encrypted_data.decode('utf8'))
        except InvalidToken:
            print(f'Błędne hasło dla pliku: {self.path}')
