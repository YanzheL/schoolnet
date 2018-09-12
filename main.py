#!/usr/bin/python3

from argparse import ArgumentParser

from net_client import NetClient

from common_utils_py.logger_router import LoggerRouter

def main(argv):
    client = NetClient(argv.username, argv.password)
    if argv.method == 'login':
        client.login()
    else:
        client.logout()

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
