"""Encrypt Decrypt Command Line Tool"""
import argparse
import getpass
import pathlib
from argparse import ArgumentParser, Namespace
from os import walk
from typing import Sequence, Any
from time import time
from tqdm import tqdm
from modes import Append, Decrypt, Encrypt

class Password(argparse.Action):
    """Create Password class to use in argparse.Action"""
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = ...) -> None:
        if values is None:
            values=getpass.getpass()

        setattr(namespace, self.dest, values)

def file_name(value: str):
    """Validate if typed filename is correct (it must ends with sufix '.txt' or . '.crp'"""
    if value.endswith(('.txt', '.crp')):
        return value
    raise argparse.ArgumentError(
        None,
        'Złe rozszerzenie pliku! Poprawne to szyfrowanie: ".txt", deszyfrowanie: ".crp"'
    )

def list_of_files(args):
    """Creates a list of files"""
    files_to_process=[]
    if args.directory:
        for path, _ , files in walk(args.directory):
            for file in files:
                if file.endswith(('.txt', '.crp')):
                    files_to_process.append(f'{path}\{file}')
    elif args.file:
        files_to_process = args.file
    return files_to_process

def main(args):
    """Main module"""
    files_to_process = list_of_files(args)

    if args.verbose >=3:
        files_to_process = tqdm(files_to_process)

    processes = {}

    for file in files_to_process:
        path = pathlib.Path(file)
        if args.mode == 'encrypt':
            process = Encrypt(path, args.password)
        elif args.mode == 'decrypt':
            process = Decrypt(path, args.password)
        elif args.mode == 'append':
            text = input('\nPodaj tekst, który chcesz dopisać do pliku: ')
            process = Append(path, args.password, text)

        processes[file] = process

    for file, process in processes.items():
        before = time()
        process.start()
        after = time()
        if args.verbose > 0 and args.verbose <= 2:
            print(file, end='\n')
            if args.verbose > 1:
                print(f'time of process: {after-before}')

    for file, process in processes.items():
        process.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Decrypt encrypt tool',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-m',
        '--mode',
        choices=['decrypt', 'encrypt', 'append'],
        required=True,
        help='''decrypt -> decrypt file
    encrypt -> encrypt file
    append -> append text to encrypt'''
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0
    )

    parser.add_argument(
        '-p',
        '--password',
        required=True,
        help='Enter Password',
        nargs='?',
        dest='password',
        action=Password
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-f',
        '--file',
        action='append',
        type=file_name,
        help='list of files to process'
    )
    group.add_argument(
        '-d',
        '--directory',
        help='directory fo folders with files to process'
    )


    args = parser.parse_args()
    main(args)
