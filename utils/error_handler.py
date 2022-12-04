import os


class ErrorHandler:

    @staticmethod
    def check_args(data, loger):
        directory = os.access(data['directory_path'], os.X_OK)
        if not directory:
            loger.write_logs(msg="Wrong directory path", level="Error")
            loger.finish_logs()
            raise FileNotFoundError("Wrong directory path")
