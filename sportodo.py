''' A simple commandline todo list utility
'''
import argparse
import sys


def init(args):
    print args


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='cmd')

    init_subparser = subparsers.add_parser('init')
    init_subparser.set_defaults(func=init)

    args = parser.parse_args()
    args.func(args)

    return 0


if __name__== '__main__':
    sys.exit(main())