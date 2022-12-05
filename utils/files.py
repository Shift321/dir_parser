from models.files import Files

file_hashes = []
old_hashes = []


def get_all_hashes_from_db(session):
    hasher = session.query(Files).all()
    for i in hasher:
        old_hashes.append(i.file_hash)
    return old_hashes


def check_for_delete_files(hash, ) -> None:
    """
    Создание двух списков с хэшами для сравнения их между собой
    """
    if hash not in file_hashes:
        file_hashes.append(hash)


def delete_files(hashes, session):
    """
    Удаление файлов из базы данных
    """
    for i in hashes:
        file = session.query(Files).filter(Files.file_hash == i).all()
        if len(file) != 0:
            session.delete(file[0])
            session.flush()
            session.commit()
