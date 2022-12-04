from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Directories(Base):
    __tablename__ = "directories"

    id: int = Column(Integer, primary_key=True)
    parent_dir_id: Optional[int] = Column(Integer)
    name: str = Column(String)

    file = relationship("Files", back_populates="dir")

    def __init__(self, parent_dir_id, name):
        self.parent_dir_id = parent_dir_id
        self.name = name
