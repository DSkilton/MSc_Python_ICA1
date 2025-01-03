from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    timezone = Column(String, nullable=False)

    cities = relationship("City", back_populates="country")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "timezone": self.timezone,
        }

    def __str__(self):
        name = self.name if self.name is not None else 'Unknown'
        timezone = self.timezone if self.timezone is not None else 'Unknown'
        return f"<Country(id={self.id}, name='{name}', timezone='{timezone}')>"
