from models.directories import Directories

dirs = {}
old_dirs = {}


def check_for_delete_dirs(session):
    directories = session.query(Directories).all()
    for i in directories:
        if i.name not in old_dirs.keys():
            old_dirs[i.name] = []
        old_dirs[i.name].append(i.parent_dir_id)
    return old_dirs


def delete_dirs(session, directs, old_directs):
    for i in old_directs:
        if i not in directs:
            directory = session.query(Directories).filter(Directories.name == i).one()
            session.delete(directory)
            session.flush()
        else:
            tmp_delete = set(old_directs) - set(directs)
            to_delete = session.query(Directories).filter(Directories.name == i).filter(
                Directories.parent_dir_id.in_(tmp_delete)).delete(synchronize_session=False)

            session.flush()
        session.commit()
