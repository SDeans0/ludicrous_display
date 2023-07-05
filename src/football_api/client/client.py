import requests


class SimpleFootballApiClient:
    """
    A class for the simple football api client
    you can get transfers, fixtures, results, competitions, and news.

    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://football98.p.rapidapi.com/"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "football98.p.rapidapi.com",
        }

    def _do_get(self, endpoint: str):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_transfers(self, chamionship: str):
        endpoint = f"{chamionship}/transfers"
        return self._do_get(endpoint=endpoint)

    def get_fixtures(self, chamionship: str):
        endpoint = f"{chamionship}/fixtures"
        return self._do_get(endpoint=endpoint)

    def get_results(self, chamionship: str):
        endpoint = f"{chamionship}/results"
        return self._do_get(endpoint=endpoint)

    def get_competitions(self):
        endpoint = "competition"
        return self._do_get(endpoint=endpoint)

    def get_news(self, chamionship: str):
        endpoint = f"{chamionship}/news"
        return self._do_get(endpoint=endpoint)

if __name__ == "__main__":
    import os, time
    api_key = os.environ.get("RAPID_API_KEY")
    print(api_key)
    client = SimpleFootballApiClient(api_key=api_key)
    for league in ("premierleague","thechampionship", "leagueone","leaguetwo"):
        x = client.get_transfers(chamionship=league)
        time.sleep(1)
        print(x)