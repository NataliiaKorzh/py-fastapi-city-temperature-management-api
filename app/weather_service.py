import os
import httpx

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("API_KEY")


async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=URL,
            params={"key": API_KEY, "q": city, "aqi": "no"},
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error during fetching"
            )

        response = response.json()

    return response["current"]["temp_c"]
