from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


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
