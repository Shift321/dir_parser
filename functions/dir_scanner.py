import datetime
import hashlib
import os
from typing import Optional, Dict

from models.directories import Directories
from models.files import Files
from utils.files import check_for_delete_files
from utils.files import file_hashes, old_hashes
from utils.dirsectories import dirs


def scan_directory(path, session, path_to_loging, loger, parent_dir_id: Optional[int] = None) -> Dict:
    """
    Рекурсивное сканирование директории
    """
    for i in os.scandir(path):
        full_path = os.path.split(i.path)
        if i.is_dir():
            if i.name not in dirs.keys():
                dirs[i.name] = []
            dirs[i.name].append(parent_dir_id)
            loger.write_logs(msg=f"dir path: {i.path}")
            check_dir = session.query(Directories).filter(Directories.parent_dir_id == parent_dir_id).filter(
                Directories.name == full_path[1]).all()
            if len(check_dir) == 0:
                directory = Directories(parent_dir_id=parent_dir_id, name=full_path[1])
                session.add(directory)
                session.flush()
                parent_id = directory.id
            else:
                parent_id = check_dir[0].id
            scan_directory(i.path, session=session, parent_dir_id=parent_id, path_to_loging=path_to_loging, loger=loger)
        else:
            loger.write_logs(msg=f"file path:{i.path}")
            sha256_hash = hashlib.sha256()
            try:
                with open(i.path, 'rb') as f:
                    for byte in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte)
            except FileNotFoundError:
                loger.write_logs(msg="No such file or directory", level="Error")

            stat_info = os.stat(i.path)
            mask = oct(stat_info.st_mode)[-3:]
            modified_date = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            start_file = session.query(Files).filter(Files.dir_id == parent_dir_id).filter(Files.name == i.name).all()
            if len(start_file) == 0:
                file = Files(dir_id=parent_dir_id, name=i.name, datetime_last_change=modified_date,
                             access_to_file=mask,
                             file_hash=sha256_hash.hexdigest())
                session.add(file)
            else:
                if start_file[0].file_hash != sha256_hash.hexdigest():
                    start_file[0].file_hash = sha256_hash.hexdigest()
                    start_file[0].datetime_last_change = modified_date
                    session.add(start_file[0])
                    session.flush()
                    session.refresh(start_file[0])
            check_for_delete_files(hash=sha256_hash.hexdigest(), session=session)
    session.commit()
    return {"file_hashes": file_hashes, "old_hashes": old_hashes, "dirs": dirs}
