from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)

    # Relationship to Country model
    country = relationship("Country", back_populates="cities")
    weather_entries = relationship('DailyWeatherEntry', back_populates='city', cascade="all, delete-orphan")

    def __str__(self):
        print("STRING FUNCTION")
        name = self.name if self.name is not None else 'Unknown'
        latitude = self.latitude if self.latitude is not None else 'Unknown'
        longitude = self.longitude if self.longitude is not None else 'Unknown'
        country_id = self.country_id if self.country_id is not None else 'Unknown'

        # Handle related Country object
        if self.country:
            country_name = self.country.name if self.country.name else 'Unknown'
        else:
            country_name = 'Unknown'

        return (f"City(id={self.id}, name='{name}', latitude={latitude}, "
                f"longitude={longitude}, country_id={country_id}, country_name='{country_name}')")