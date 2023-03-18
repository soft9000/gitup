#!/usr/bin/env python3
''' MISSION: Create & manage a `classic` (aka: space delimited hex16) string-to-file
input -n- output strategy for GITUP.

File: SaveIO.py
Author: Randall Nagy'''

import os
import os.path
import time


FILE_TYPE = '.gitup' # NOTE: Any upload / download file suffix must be unique!

class HexED16:
    ''' A classic, space-delimited, encoder / decoder for HEX16 '''
    @staticmethod
    def encode(a_string)->str():
        ''' Return an encoded string, else None'''
        if not a_string:
            return None
        result = ''
        for achar in a_string:
            result += hex(ord(achar))
            result += ' '
        return result.strip()

    @staticmethod
    def decode(a_string)->str():
        ''' Return a decoded string, else None'''
        if not a_string:
            return None
        result = ''
        for achar in a_string.split(' '):
            result += chr(int(achar,16))
        return result

class LastFile:
    ''' Supporting class: Used to add and detect the last file used. '''
    @staticmethod
    def make_filename(file_type = FILE_TYPE):
        ''' Use the time to create an easily sortable filename.'''
        return str(time.time()) + file_type

    @staticmethod
    def make_file(a_folder, file_type = FILE_TYPE):
        ''' Create a fully-qualified file name in a_folder.
            POSIX file names are assumed. '''
        if not a_folder.endswith('/'):
            a_folder += '/'
        return a_folder + LastFile.make_filename(file_type)

class IoString:
    ''' Main class: Used to encode + decode sortable, file-based strings. '''

    def __init__(self, git_folder, file_type = FILE_TYPE):
        ''' Share the location of your `git` project. '''
        if not os.path.exists(git_folder):
            raise Exception(f"Gitup: Unable to access git_folder=[{git_folder}].")
        self.git_folder = git_folder
        if not file_type:
            raise Exception(f"Gitup: Unique file type / file suffix is required.")
        self.file_type = file_type
        
    def list_all(self)->str():
        ''' Return a sorted() list of GITUP files in your initalized location. '''
        nodes = []
        for node in os.listdir(self.git_folder):
            if node.endswith(self.file_type):
                nodes.append(node)
        return sorted(nodes)
        
    def save_out(self, a_string)->bool:
        ''' Encode + place the results into a fully-qualified time-stamped (GITUP) file name. '''
        afile = LastFile.make_file(self.git_folder)
        adump = HexED16.encode(a_string)
        with open(afile, 'w') as fh:
            print(adump, file=fh)
        return os.path.exists(afile)

    def read_latest(self)->str():
        ''' Read, decode, and return the results of the latest GITUP file. '''
        nodes = self.list_all()
        if not nodes:
            return None
        afile = nodes[-1]
        if not afile:
            return None
        with open(afile) as fh:
            return HexED16.decode(fh.read())

    def remove_all_files(self)->bool:
        for node in self.list_all():
            os.remove(node)
            if os.path.exists(node):
                return False
        return True


if __name__ == '__main__':
    test = IoString('.')
    test.remove_all_files()
    if not test.save_out('nagy'):
        raise Exception("Unable to save file.")
    results = test.read_latest()
    print(results)
    if results != 'nagy':
        raise Exception("Unable to read file.")
    results = test.list_all()
    if not results:
        raise Exception("Unable list file.")
    success = False
    if len(results) == 1:
        test.remove_all_files()
        if not test.list_all():
            print("Testing success.")
            success = True
    if not success:
        print("Testing regression.")
        
    
