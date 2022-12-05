import argparse


def create_parser_for_daemon():
    """
    Парсер аргументов для демона
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True,
                        help="Config should be .yaml file and exists : directory path,database path,log path.")
    return parser
