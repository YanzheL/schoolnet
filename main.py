#!/usr/bin/python3

from argparse import ArgumentParser

from common_utils_py.logger_router import LoggerRouter
from net_client import NetClient


def main(argv):
    try:
        client = NetClient(argv.username, argv.password)
        if argv.method == 'login':
            client.login()
        else:
            client.logout()
    except:
        import traceback
        traceback.print_exc()
    finally:
        LoggerRouter().stop()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-u', '--username', required=True, type=str
    )
    parser.add_argument(
        '-p', '--password', required=True, type=str
    )
    parser.add_argument(
        '-m', '--method', required=True, choices=['login', 'logout']
    )

    main(parser.parse_args())
