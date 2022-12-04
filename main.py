from database.database import Base, create_session, make_engine
from functions.dir_scanner import scan_directory
from utils.logger import CustomLogging
from utils.arg_parser import create_parser
from utils.error_handler import ErrorHandler


def get_parser_args():
    """
    Получение аргументов скрипта
    """
    parser = create_parser()
    args = parser.parse_args()
    data = {"log": args.log, "verbose": args.verbose, "directory_path": args.directory, "database_path": args.database}
    return data


def main(data):
    """
    Основной скрипт
    """
    custom_logging = CustomLogging(log_path=data['log'], verbose=data['verbose'])
    custom_logging.write_logs(msg=f"Script starts")
    ErrorHandler.check_args(data, loger=custom_logging)
    custom_logging.write_logs(msg=f"args : -d {data['directory_path']}, -b {data['database_path']},-l {data['log']}")
    engine = make_engine(data['database_path'])
    Base.metadata.create_all(engine)
    session = create_session(engine)
    scan_directory(path=data['directory_path'], session=session, path_to_loging=data['log'], loger=custom_logging)
    custom_logging.finish_logs()


if __name__ == '__main__':
    """
    Запуск всего скрипта
    """
    main(get_parser_args())