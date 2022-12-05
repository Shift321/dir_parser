# Directories parser

Тестовое задание для компании Timeweb
## Техническое задание
Первое задание
Создать скрипт, который наполняет базу данных sqlite3 информацией о файлах в
директории (рекурсивно, то есть включая вложенные директории). Структура базы:
1. Таблица directories:
a. id директории
b. id родительской директории или NULL для корневой директории,
переданной в аргументе
c. название директории
2. Таблица files:
a. id файла
b. id директории файла
c. название файла
d. дата и время последнего изменения
e. права файла в формате xyz (например, 644)
f. sha256 хэш файла
Аргументы скрипта:
1. -d, --directory - полный или относительный путь к директории, из которой
наполняется база (обязательный аргумент)
2. -b --database - полный или относительный путь к базе данных, в которой будут
сохраняться данные по директории (обязательный аргумент)
3. -v, --verbose - флаг, показывающий, что необходимо выводить информацию на
консоль. По умолчанию скрипт не должен ничего выводить в терминал кроме
информации по использованию при недостаточных аргументах или аргументе
-h/--help (необязательный аргумент)
4. -l, --log - полный или относительный путь к файлу лога. Если в логе уже есть
записи, они должны остаться. (обязательный аргумент)
5. -h, --help - вывод информации по использованию скрипта (необязательный
аргумент)
Если директория не существует, а также если невозможно создать/получить доступ к
базе данных и логу, скрипт должен завершить выполнение с поясняющей ошибкой.
Логируемые сообщения:
1. Начало выполнения скрипта
2. Информация о полученных аргументах
3. Ошибки обработки аргументов, если они есть
4. Пути к файлам
5. Пути к директориям
6. Конец выполнения скрипта
Пути к файлам и директориям должны выводиться по очереди (один на строку) в
процессе обнаружения скриптом.
Формат лога следующий:
[дата время] тип_сообщения Сообщение
Типов сообщений всего два - ERROR для ошибок и INFO для всего остального.
При выполнении скрипта запрещается использовать внешние скрипты и утилиты.
Второе задание
Используя скрипт из первого задания в качестве модуля, создать скрипт, который
работает как демон. Демон должен следить за изменениями файлов, при этом
создавая, удаляя или меняя записи таблицы. Демону могут передаваться только
следующие аргументы:
1. -c, --config - путь к файлу конфигурации демона (обязательный)
2. -h, --help - вывод информации по использованию и завершение работы
(необязательный).
Файл конфигурации является YAML-файлом со структурой вида:
conf:
- directory: путь к директории
- database: путь к базе данных
- log: путь к файлу лога
Если файл конфигурации не существует или его содержимое не соответствует
представленной структуре, скрипт должен завершиться с выводом поясняющей
ошибки. Поля соваря conf в файле конфигурации соответствуют аргументам скрипта из
первого задания, но путь к логу здесь является обязательным.
Скрипт должен выполнять логирование аналогично первому заданию.
Завершение демона осуществляется по нажатию CTRL-C (завершение работы
логируется так же, как и в первом задании).
Бонус: написать systemd-unit для этого демона.
## Установка и запуск приложения


```bash
Скачать репозиторий
pip install requirements.txt
python main.py -d -b -l
```

## Main functions
Рекурсивное сканирование директории
```python
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
            with open(i.path, 'rb') as f:
                for byte in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte)
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
```
## Database
База данных sqlite в качестве ORM использовал sqlachlemy
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def make_engine(path):
    engine = create_engine(f'sqlite:///{path}')
    return engine


def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


Base = declarative_base()
```

## Models
Модель директории 
```python
class Directories(Base):
    __tablename__ = "directories"

    id: int = Column(Integer, primary_key=True)
    parent_dir_id: Optional[int] = Column(Integer)
    name: str = Column(String)

    file = relationship("Files", back_populates="dir")

    def __init__(self, parent_dir_id, name):
        self.parent_dir_id = parent_dir_id
        self.name = name

```
Модель файла
```python
class Files(Base):
    __tablename__ = "files"

    id: int = Column(Integer, primary_key=True)
    dir_id: int = Column(Integer, ForeignKey('directories.id'))
    name: str = Column(String)
    datetime_last_change: datetime = Column(DateTime)
    access_to_file: str = Column(String)
    file_hash: str = Column(String)

    dir = relationship("Directories", back_populates="file")

    def __init__(self, dir_id, name, datetime_last_change, access_to_file, file_hash):
        self.dir_id = dir_id
        self.name = name
        self.datetime_last_change = datetime_last_change
        self.access_to_file = access_to_file
        self.file_hash = file_hash
```