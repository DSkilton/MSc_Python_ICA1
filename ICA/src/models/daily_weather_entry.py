from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class DailyWeatherEntry(Base):
    __tablename__ = 'daily_weather_entries'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    min_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    mean_temp = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)

    city = relationship("City", back_populates="weather_entries")

    def __repr__(self):
        return (f"DailyWeatherEntry(id={self.id}, date='{self.date}', city_id={self.city_id}, "
                f"temperature_max={self.max_temp}, temperature_min={self.min_temp}, precipitation={self.precipitation})")
