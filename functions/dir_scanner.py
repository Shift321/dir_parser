import datetime
import hashlib
import os
from typing import Optional

from models.directories import Directories
from models.files import Files


def scan_directory(path, session, path_to_loging, loger, parent_dir_id: Optional[int] = None) -> None:
    """
    Рекурсивное сканирование директории
    """
    for i in os.scandir(path):
        full_path = os.path.split(i.path)
        if i.is_dir():
            loger.write_logs(msg=f"dir path: {i.path}")
            directory = Directories(parent_dir_id=parent_dir_id, name=full_path[1])
            session.add(directory)
            session.flush()
            parent_id = directory.id
            scan_directory(i.path, session=session, parent_dir_id=parent_id, path_to_loging=path_to_loging, loger=loger)
        else:
            loger.write_logs(msg=f"file path:{i.path}")
            sha256_hash = hashlib.sha256()
            with open(i.path, 'rb') as f:
                for byte in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte)
            stat_info = os.stat(i.path)
            mask = oct(stat_info.st_mode)[-3:]
            modified_date = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            file = Files(dir_id=parent_dir_id, name=i.name, datetime_last_change=modified_date,
                         access_to_file=mask,
                         file_hash=sha256_hash.hexdigest())
            session.add(file)
    session.commit()
