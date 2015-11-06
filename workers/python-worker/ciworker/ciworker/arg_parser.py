import argparse


def get_args():

    parser = argparse.ArgumentParser(description='Start python-worker.')
    parser.add_argument('config', type=str, help='Configuration file location.')
    return parser.parse_args()
