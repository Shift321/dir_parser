import yaml


def read_config(path):
    """
    Чтение конфига
    """
    with open(path, "r") as stream:
        conf = yaml.safe_load(stream)
        directory_path = conf['conf'][0]['directory']
        database_path = conf['conf'][1]['database']
        log_path = conf['conf'][2]['log']

        data = {"log": log_path, "verbose": False, "directory_path": directory_path, "database_path": database_path}
        return data
