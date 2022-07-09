from sqlalchemy import Column, Integer, String

from api.db import Base


class ImageInfo(Base):
    __tablename__ = "image_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String(255))
    title = Column(String(1024))

    def __repr__(self):
        return f"<Filename {self.filename}>"
