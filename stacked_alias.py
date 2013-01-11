#!/usr/bin/python
# -*- coding: utf-8 -*-

import exceptions
import logging
import operator
import optparse
import os
import random
import re
import shlex
import sys
import subprocess
import unittest

LOGGING_LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
    }

DEFAULT_LOGGING_LEVEL = logging.ERROR
# Expand the tilde into the user's home directory path.
ALIAS_FILE = os.path.expanduser('~/alias_list')


class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""

        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""

        if self.fall or not args:
            return True
        elif self.value in args:

            # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class Alias(object):

    def __new__(cls, *args, **kwargs):
        obj = super(Alias, cls).__new__(cls)

        # print('__new__ called. got new obj id=0x%x' % id(obj))

        return obj

    def __init__(
        self,
        name,
        dir,
        ):

        self.name = name
        self.dir = dir


class Alias_list(object):

    def __new__(cls, *args, **kwargs):
        obj = super(Alias_list, cls).__new__(cls)
        return obj

    def __init__(self, alias_file):

        self.list = []
        self.alias_file = alias_file
        self._process_aliases()

    def _process_aliases(self):

        if os.path.exists(self.alias_file):
            f = open(self.alias_file, 'r')
	    logging.debug('Reading file %s' % self.alias_file)

            for line in f.readlines():
                # Split the string into individual fields.
                line.replace(' ', '')
                (alias, dir) = line.strip().split(',')
                self.list.append(Alias(alias.strip(), dir.strip()))

                f.close()

            # Sort the aliasList in place by name
            self.list.sort(key=operator.attrgetter('name'))

            else:
                # Create the file.
                f = open(self.alias_file, 'w')
                f.close()

    def find(self, stacked_alias_str):

        list_of_aliases = stacked_alias_str.split('.')

        directory = ''

        for alias_name in reversed(list_of_aliases):
            for alias in self.list:
                if alias_name == alias.name:
                    logging.debug('directory: %s' % alias.dir)
                    directory = alias.dir + directory
                    break

        directory.replace(' ', '')
        return directory

    def insert(self, alias_fields_str):

        # Parse the alias string: [name, directory]
        alias_fields_str.replace(' ', '')

        (name, dir) = alias_fields_str.strip().split(',')

        # Verify the alias name is not a duplicate of one already present in the list.
        for existing_alias in self.list:
            if name == existing_alias.name:
                #logging.error('alias name %s already exists' % name)
                print('Error. Alias name %s already exists' % name)
                return

        logging.debug('inserting alias name %s' % name)

        # If the directory name doesn't begin with a '/' add one.
        if dir[0] != '/':
            dir = '/' + dir

        # Add the alias to the list.
        self.list.append(Alias(name, dir))

        # Write the list to file.
        # More error checking here...
        open(self.alias_file, 'a').write('%-18s %s\n' % (name + ',', dir))

        #f.close()

    def remove(self, alias_name):

        update_file = 0

        for existing_alias in self.list:
            if alias_name == existing_alias.name:
                self.list.remove(existing_alias)
                update_file = 1
                break

        if update_file:
            self._write_alias_file()

        return

    def _write_alias_file(self):

        f = open(self.alias_file, 'w')
        f.seek(0)

        for alias in self.list:
            f.write('%-18s %s\n' % (alias.name + ',', alias.dir))

        f.truncate()
        f.close()
        return

    def display(self):

        print '%-18s %s' % ('name', 'directory')
        print '%-18s %s' % ('----', '---------')
        for alias in self.list:
            print '%-18s %s' % (alias.name, alias.dir)

        return

def main():

    parser = optparse.OptionParser()
    parser.add_option('-l', '--logging_level', help='Logging level')
    parser.add_option('-f', '--logging_file', help='Logging file name')
    parser.add_option('-a', '--alias', help='Alias')
    parser.add_option('-i', '--insert_alias', help='Insert an alias')
    parser.add_option('-r', '--remove_alias', help='Remove an alias')
    parser.add_option('-d', '--display_aliases', help='Display aliases')

    (options, args) = parser.parse_args()

    #print(options)
    #print(args)

    if options.logging_level == None:
        numeric_level = DEFAULT_LOGGING_LEVEL
    else:

        # assuming loglevel is bound to the string value obtained from the
        # command line argument. Convert to upper case to allow the user to
        # specify -logging_level DEBUG or -logging_level debug

        numeric_level = getattr(logging, options.logging_level.upper(),
                                None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s'
                             % options.logging_level)

    logging.basicConfig(level=numeric_level,
                        filename=options.logging_file,
                        format='%(levelname)-8s: %(funcName)20s(): %(lineno)5d: %(message)s'
                        , datefmt='%Y-%m-%d %H:%M:%S')  # '%(asctime)s: '

    logging.debug("Alias option:  %s " % options.alias)

    # Split the cmd string into individual commands using the pipe as a delimiter.
    # list_of_aliases = options.alias.split(".")
    alias_list = Alias_list(ALIAS_FILE)

    if options.display_aliases == '1':
        alias_list.display()

    # Perform actions based on the command line options.

    # Bail out if no alias to process.
    if options.alias != None:
        directory = alias_list.find(options.alias)
        print '%s' % directory

    if options.insert_alias != None:
        #print "====> %s" % (options.insert_alias)
        alias_list.insert(options.insert_alias)

    if options.remove_alias != None:
        alias_list.remove(options.remove_alias)

    return


if __name__ == '__main__':
    main()

