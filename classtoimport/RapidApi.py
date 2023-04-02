import requests
import logging as log

class RapidApi:
    
    def __init__(self):

        self
        self.url = "https://api-football-v1.p.rapidapi.com/v3/"
        self.key = "HeqAaRKMZnmshWCjl8pEb6RXhJCWp1GqMzdjsnsxcbv50oyARa"
        self.host = "api-football-v1.p.rapidapi.com"
        

    
       
    def getCountries(self,endpoint):
        # Make a request to the API and get the data
        url = self.url + endpoint 
        headers = { "X-RapidAPI-Key": self.key,"X-RapidAPI-Host": self.host }
        
        try:
            response = requests.request("GET", url, headers=headers)
            data = response.json()
        except Exception as excpt:
            log.exception(excpt)
        

        return data["response"]

    def getLeagues(self,endpoint,par):
        
        url = self.url + endpoint 
        headers = { "X-RapidAPI-Key": self.key,"X-RapidAPI-Host": self.host }

        try:
            response = requests.request("GET", url, headers=headers,params=par)
            data = response.json()
        except Exception as excpt:
            log.exception(excpt)

        return data["response"]

    def getFixtures(self,endpoint,param):
        
        url = self.url + endpoint 
        headers = { "X-RapidAPI-Key": self.key,"X-RapidAPI-Host": self.host }
        
        #response = requests.request("GET", url, headers=headers,params=param)
        #data = response.json()

        try:
            response = requests.request("GET", url, headers=headers,params=param)
            data = response.json()
        except Exception as excpt:
            log.exception(excpt)

        return data["response"]

    def getTeams(self,endpoint,param):
        
        url = self.url + endpoint 
        headers = { "X-RapidAPI-Key": self.key,"X-RapidAPI-Host": self.host }
        
        #response = requests.request("GET", url, headers=headers,params=param)
        #data = response.json()

        try:
            response = requests.request("GET", url, headers=headers,params=param)
            data = response.json()
        except Exception as excpt:
            log.exception(excpt)

        return data["response"]

    def getEvents(self,endpoint,param):

        url = self.url +"fixtures/"+endpoint 
        headers = { "X-RapidAPI-Key": self.key,"X-RapidAPI-Host": self.host }
        
        #response = requests.request("GET", url, headers=headers,params=param)
        #data = response.json()

        try:
            response = requests.request("GET", url, headers=headers,params=param)
            data = response.json()
        except Exception as excpt:
            log.exception(excpt)

        return data["response"]