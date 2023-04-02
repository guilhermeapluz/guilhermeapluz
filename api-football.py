from classtoimport.ConnectMySql import ConnectMySql
from classtoimport.RapidApi import RapidApi
from classtoimport.SaveFile import SaveFile
from datetime import datetime
import logging as log

def main():

    conn = ConnectMySql()
    endpoint = RapidApi()
    savefile = SaveFile()

    dateToday = datetime.today()
    logPath = "C:\\Users\\guilh\\Documents\\api_footbal\\logs\\"
    logFilename = dateToday.strftime("%Y%m%d_%H%M%S")+".log"
    log.basicConfig(filename=logPath+logFilename, encoding='utf-8', level=log.INFO, format='%(levelname)s   %(asctime)s   %(message)s')


    table = "leagues"
    
    seasons = ["2022"]
    leagues = ["39","135","78","61","39","140","270","128"]


    for league in leagues:
        dataLeagues = endpoint.getLeagues(table,{"id":league})
        
        savefile.Json(dataLeagues[0],table+"\\"+str(league))
        conn.insertRapidApi(dataLeagues,table)

        for season in seasons: #dataLeagues[0]["seasons"]:

            param ={"league":league,"season":season}
            

            print("TEAMS...")
            dataTeams = endpoint.getTeams("teams",param)
            savefile.Json(dataTeams[0],"teams\\"+league)
            conn.insertRapidApi(dataTeams,"teams")
            log.info("> TEAMS < LEAGUE: " + str(league) + " | SEASON: " + str(season))


            print("FIXTURES...")
            dataFixtures = endpoint.getFixtures("fixtures",param)
            savefile.Json(dataFixtures[0],"fixtures\\"+str(dataFixtures[0]["fixture"]["id"]))
            conn.insertRapidApi(dataFixtures,"fixtures")
            log.info("> FIXTURES < LEAGUE: " + str(league) + " | SEASON: " + str(season))

            print("EVENTS...")

            for fixture in dataFixtures:

                param = {"fixture": fixture["fixture"]["id"],"type":"Goal"}
                dataEvents = endpoint.getEvents("events",param)
                
                if len(dataEvents)>0:
                    savefile.Json(dataEvents[0],"events\\" + str(league) + "_" + str(fixture["fixture"]["id"]))
                    conn.insertRapidApi(dataEvents,"events",param)          
                    log.info("> EVENTS < LEAGUE: " + str(league) + " | SEASON: " + str(season) + " | FIXTURE: " + str(fixture["fixture"]["id"]))


            print("\n")

        print(dataLeagues[0]["league"]["name"] + " (" + str(dataLeagues[0]["league"]["id"]) + ") Finished")
        log.info(dataLeagues[0]["league"]["name"] + " (" + str(dataLeagues[0]["league"]["id"]) + ") Finished")
    
    totalTimeExec = datetime.today()-dateToday
    log.info("Tempo total de execução: "+str(totalTimeExec))
    


if __name__ == '__main__':
    main()