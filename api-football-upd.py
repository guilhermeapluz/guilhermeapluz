from classtoimport.ConnectMySql import ConnectMySql
from classtoimport.RapidApi import RapidApi
from classtoimport.SaveFile import SaveFile
from classtoimport.Settings import Settings 
from datetime import datetime
import logging as log


def main():

    conn = ConnectMySql()
    endpoint = RapidApi()
    savefile = SaveFile()
    settings = Settings()

    dateToday = datetime.today()
    settings.set({
        "section":"parameters",
        "parameter":"lastupdate",
        "value":str(dateToday.strftime("%Y-%m-%d"))
    })

    logPath = "C:\\Users\\guilh\\Documents\\api_footbal\\logs\\"
    logFilename = dateToday.strftime("%Y%m%d_%H%M%S")+".log"
    log.basicConfig(filename=logPath+logFilename, encoding='utf-8', level=log.INFO, format='%(levelname)s   %(asctime)s   %(message)s')

    sql  = "select f.id fixture, l.id league, f.status "
    sql += "from fixtures f "
    sql += "left join leagues l on l.id = f.league "
    sql += "where status not in ('FT','PEN','AET') "
    sql += "and date <= ' " + dateToday.strftime("%Y-%m-%d") + " ' "

    sqlREsult = conn.mysql_select(sql,type=1) # type<>None (list) / type=None (dict)
   
    fldToUpd = []
    for item in sqlREsult:
        # 0 = fixture; 1 = league; 2 = status

        param ={"id":item[0]}
        fixtures = endpoint.getFixtures("fixtures",param)
        fixtures = fixtures[0]
        
        if fixtures["teams"]["home"]["winner"]:
            winner = 'home'
        elif fixtures["teams"]["away"]["winner"]:
            winner = 'away'
        else: winner = None


        fldToUpd.append([
            fixtures["fixture"]["referee"],
            fixtures["fixture"]["date"],
            fixtures["fixture"]["status"]["short"],
            winner,
            fixtures["fixture"]["id"]
        ])

    a = conn.mysql_upd_fixture(fldToUpd)
    print(a.rowcount,' linhas alteradas.')
    

if __name__ == '__main__':
    main()