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

