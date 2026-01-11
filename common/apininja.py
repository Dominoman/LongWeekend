import shelve

import requests
from flask import url_for


class Ninja:
    def __init__(self, api_key,shelve_file:str="shelve"):
        self.api_key = api_key
        self.shelve=shelve.open(shelve_file)

    def get_airline_logos(self, airline_code:str, cached:bool=True)-> dict[str, str] | None:
        """
        Fetches the logo URL for a given airline code.

        Args:
            cached:
            airline_code (str): The IATA code of the airline.

        Returns:
            str: The URL of the airline's logo.
        """
        logo_types = ["logo_url","brandmark_url","tail_logo_url"]

        if cached:
            logos = {}
            for logo_type in logo_types:
                if airline_code+logo_type in self.shelve:
                    logos[logo_type] = self.shelve[airline_code+logo_type]
            if len(logos)>0:
                return logos

        response = requests.get(f"https://api.api-ninjas.com/v1/airlines?iata={airline_code}",
                                headers={'X-Api-Key': self.api_key})
        if response.status_code == 200:
            data = response.json()[0]
            logos = {"logo_url":url_for('static', filename="app/static/logos/nologo.png")}
            for logo_type in logo_types:
                if logo_type in data:
                    logo_url = data[logo_type]
                    self.shelve[airline_code+logo_type]=logo_url
                    logos[logo_type]=logo_url
            return logos
        else:
            raise Exception(f"Error fetching logo: {response.status_code} - {response.text}")

    def get_flag(self,country_code:str,cached:bool=True):
        if cached:
            if country_code in self.shelve:
                return self.shelve[country_code]
        response = requests.get(f"https://api.api-ninjas.com/v1/countryflag?country={country_code}",
                                headers={'X-Api-Key': self.api_key})
        if response.status_code == 200:
            data = response.json()
            flag_url = data["rectangle_image_url"]
            self.shelve[country_code]=flag_url
            return flag_url
        else:
            raise Exception(f"Error fetching flag: {response.status_code} - {response.text}")
