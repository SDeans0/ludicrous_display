from typing import Optional
import requests
import datetime as dt

from utils.dateutils import get_today


class LiveScoreApiClient:
    """
    A class for the livescore api client
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://livescore6.p.rapidapi.com/"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "livescore6.p.rapidapi.com",
        }

    def _do_get(self, endpoint: str, params: Optional[dict] = None):
        params = params or {}
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def get_matches(self, date: Optional[dt.date] = None):
        date = date or get_today() - dt.timedelta(days=1)
        datestr = date.strftime("%Y%m%d")
        endpoint = "matches/v2/list-by-date"
        params = {"Category": "soccer", "Date": datestr, "Timezone":0}
        return self._do_get(endpoint=endpoint, params=params)

    

if __name__ == "__main__":
    import os, time
    api_key = os.environ.get("RAPID_API_KEY")
    print(api_key)
    client = LiveScoreApiClient(api_key=api_key)
    x = client.get_matches()
    print(x)
    b=1
    # need to make a parser for this to puit it into a match object
