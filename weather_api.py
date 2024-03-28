import requests
from typing import Dict


CLOUD_COVER_MAPPER = {
    1: "0%-6%",
    2: "6%-19%",
    3: "19%-31%",
    4: "31%-44%",
    5: "44%-56%",
    6: "56%-69%",
    7: "69%-81%",
    8: "81%-94%",
    9: "94%-100%",
}
SEEING_MAPPER = {
    1: "<0.5",
    2: "0.5-0.75",
    3: "0.75-1",
    4: "1-1.25",
    5: "1.25-1.5",
    6: "1.5-2",
    7: "2-2.5",
    8: ">2.5",
}
TRANSPARENCY_MAPPER = {
    1: "<0.3",
    2: "0.3-0.4",
    3: "0.4-0.5",
    4: "0.5-0.6",
    5: "0.6-0.7",
    6: "0.7-0.85",
    7: "0.85-1",
    8: ">1",
}
LIFTED_INDEX_MAPPER = {
    -10: "Below -7",
    -6: "-7 to -5",
    -4: "-5 to -3",
    -1: "-3 to 0",
    2: "0 to 4",
    6: "4 to 8",
    10: "8 to 11",
    15: "Over 11",
}
RELATIVE_HUMIDITY_MAPPER = {
    -4: "0%-5%",
    -3: "5%-10%",
    -2: "10%-15%",
    -1: "15%-20%",
    0: "20%-25%",
    1: "25%-30%",
    2: "30%-35%",
    3: "35%-40%",
    4: "40%-45%",
    5: "45%-50%",
    6: "50%-55%",
    7: "55%-60%",
    8: "60%-65%",
    9: "65%-70%",
    10: "70%-75%",
    11: "75%-80%",
    12: "80%-85%",
    13: "85%-90%",
    14: "90%-95%",
    15: "95%-99%",
    16: "100%",
}
WIND_SPEED_MAPPER = {
    1: "Below 0.3m/s (calm)",
    2: "0.3-3.4m/s (light)",
    3: "3.4-8.0m/s (moderate)",
    4: "8.0-10.8m/s (fresh)",
    5: "10.8-17.2m/s (strong)",
    6: "17.2-24.5m/s (gale)",
    7: "24.5-32.6m/s (storm)",
    8: "32.6-36.7m/s (hurricane)",
    9: "36.7-41.4m/s (hurricane+)",
    10: "41.4-46.2m/s (hurricane+)",
    11: "46.2-50.9m/s (hurricane+)",
    12: "50.9-55.9m/s (hurricane+)",
    13: "Over 55.9m/s (hurricane+)",
}

class SevenTimerWeatherApi:
    """ Weather Api for 7timer """

    def __init__(self):
        self.host = "https://www.7timer.info/bin/astro.php"

    def get_weather_data(self, lon, lat, product="astro", output="json"):
        params = { "lon": lon, "lat": lat, "product": product, "output": output}
        response = requests.get(self.host, params=params, timeout=10)
        if response.status_code == 200:
            return [self._convert_format(data) for data in response.json()['dataseries']]
        return []
    
    def _convert_format(self, data: Dict, unknown_symbol="-") -> Dict:
        cloud_cover = CLOUD_COVER_MAPPER.get(data.get('cloudcover', 0), unknown_symbol)
        seeing = SEEING_MAPPER.get(data.get("seeing", 0), unknown_symbol)
        transparency = TRANSPARENCY_MAPPER.get(data.get("transparency", 0), unknown_symbol)
        lifted_index = LIFTED_INDEX_MAPPER.get(data.get("lifted_index", 0), unknown_symbol)
        relative_humidity = RELATIVE_HUMIDITY_MAPPER.get(data.get("rh2m", 0), unknown_symbol)
        wind_direction = data.get("wind10m", {}).get("direction", unknown_symbol)
        speed = WIND_SPEED_MAPPER.get(data.get("wind10m", {}).get("speed", 0), unknown_symbol)
        temperature = data.get("temp2m", unknown_symbol)
        precipitation_type = data.get("prec_type", unknown_symbol)
        return {
            "timepoint": data["timepoint"],
            "cloud_cover": cloud_cover,
            "seeing": seeing,
            "transparency": transparency,
            "lifted_index": lifted_index,
            "relative_humidity": relative_humidity,
            "wind_direction": wind_direction,
            "speed": speed,
            "temperature": temperature,
            "precipitation_type": precipitation_type,
        }


if __name__ == '__main__':
    api = SevenTimerWeatherApi()
    result = api.get_weather_data(lon=113.534147, lat=22.806959)
    print(result)
