import argparse


def create_parser() -> argparse.ArgumentParser():
    """
    Создание парсера аргументов из консоли
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required=True, help="You should pass the directory where should scan")
    parser.add_argument("-b", "--database", required=True, help="pass the path to database")
    parser.add_argument("-v", "--verbose", action="store_true", help="if you need to show all in console")
    parser.add_argument("-l", "--log", required=True, help="path to log file")
    return parser
