''' A simple commandline todo list utility
'''
from __future__ import print_function

import argparse
import json
import os
import sys

from list_classes import TodoListItem

TODO_FILENAME = '.todolo.json'


def find_list(path):
    while path:
        test_path = os.path.join(path, TODO_FILENAME)
        if os.path.exists(test_path):
            return test_path
        if path == os.path.sep:
            return None
        path = os.path.split(path)[0]


def find_and_load_list(path):
    list_path = find_list(path)
    if list_path is None:
        return None
    with open(list_path, 'r') as fileobj:
        list = json.load(fileobj)
    return list


def init(args):
    """ initialize a todo file in the current dir
    """
    cwd = os.getcwd()
    print(cwd)
    list_path = os.path.join(cwd, TODO_FILENAME)
    if os.path.exists(list_path):
        print('This directory: {} is already intialized'.format(cwd))
        return 1
    empty_list = []
    with open(list_path, 'w') as fileobj:
        json.dump(empty_list, fileobj, indent=2)
    print('Empty todo list initialized in {}'.format(cwd))
    return 0


def list(args):
    list = find_and_load_list(os.getcwd())
    print(list)


def add(args):
    print(args.text)
    new_item = TodoListItem.constrct_item_from_dict({'text':args.text})
    print(new_item)
    import pdb; pdb.set_trace()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='cmd')

    init_subparser = subparsers.add_parser(
        'init',
        help='initialize a todo list in current working dir')
    init_subparser.set_defaults(func=init)

    list_subparser = subparsers.add_parser(
        'list',
        help='enumerate the todo list items')
    list_subparser.set_defaults(func=list)

    add_subparser = subparsers.add_parser(
        'add',
        help='add a todo item')
    add_subparser.add_argument(
        'text',
        help='text of todo')
    add_subparser.set_defaults(func=add)

    args = parser.parse_args()
    return args.func(args)


if __name__== '__main__':
    sys.exit(main())
