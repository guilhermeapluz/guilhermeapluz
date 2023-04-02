from datetime import date
import configparser

SETTINGS_FILE = "C:\\Users\\guilh\\Documents\\api_footbal\\settings.ini"

class Settings:
    def __init__(self):
        self.sett = configparser.ConfigParser()
        self.sett.read(SETTINGS_FILE)

        
    def set(self,par):
        
        self.sett.set(par["section"],par["parameter"],par["value"])
        with open(SETTINGS_FILE, 'w') as configfile:
            self.sett.write(configfile)

    def get(self,par):

        parSett = self.sett.get(par["section"],par["parameter"])
        return parSett
