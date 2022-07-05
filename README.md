# EncryptDecryptCommandLineTool

Script that allows you to encrypt and decrypt text files with ".txt" extension.

We can provide the path to the file directly or the entire folder - in this case, the program will go through the folder and encrypt or decrypt all the".txt" files in it.

The program is run from the command line with the following modes:

- decrypt -> decrypt file

- encrypt -> encrypt file

- append -> append text to encrypted file

The application is multithreaded.

Fernet is used for encryption and decryption. Encrypted files are protected by a password that we create during encryption.

The password can be entered immediately at startup or entered after startup - then it is not visible.

-example with entered password:

python main.py -m encrypt -f file.txt -f file2.txt -p password

-example without entered password:

python main.py -m encrypt -f file.txt -f file2.txt -p

- in this case program will ask for password in next step. Password is invisible and safe.
