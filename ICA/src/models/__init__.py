from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .city import City
from .country import Country
from .daily_weather_entry import DailyWeatherEntry