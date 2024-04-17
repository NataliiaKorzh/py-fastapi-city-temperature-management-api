from datetime import datetime

from sqlalchemy.orm import Session

from app.temperature.models import Temperature
from app.city.models import City
from app.weather_service import get_weather


async def update_temperature(db: Session):
    cities = db.query(City).all()
    temperatures = []

    for city_obj in cities:
        city_name = city_obj.name
        temperature = await get_weather(city_name)
        db_temperature = Temperature(
            city_id=city_obj.id,
            date_time=datetime.now(),
            temperature=temperature,
        )
        temperatures.append(db_temperature)

    db.bulk_save_objects(temperatures)
    db.commit()

    return temperatures


def get_temperatures(db: Session):
    return db.query(Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    return db.query(Temperature).filter(
        Temperature.city_id == city_id
    )
