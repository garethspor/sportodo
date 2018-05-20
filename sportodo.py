''' A simple commandline todo list utility
'''
import argparse
import json
import os
import sys

TODO_FILENAME = '.' + os.path.splitext(__file__)[0] + '.json'

def init(args):
    """ initialize a todo file in the current dir
    """
    cwd = os.getcwd()
    list_path = os.path.join(cwd, TODO_FILENAME)
    if os.path.exists(list_path):
        print('This directory: {} is already intialized'.format(cwd))
        return 1
    empty_list = []
    with open(list_path, 'w') as fileobj:
        json.dump(empty_list, fileobj, indent=2)
    print('Empty todo list initialized in {}'.format(cwd))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='cmd')

    init_subparser = subparsers.add_parser('init')
    init_subparser.set_defaults(func=init)

    args = parser.parse_args()
    return args.func(args)


if __name__== '__main__':
    sys.exit(main())