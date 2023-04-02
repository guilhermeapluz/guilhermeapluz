from classtoimport.Settings import Settings 
import mysql.connector
import logging as log

class ConnectMySql:
    
    # Replace the placeholder values with your own database connection details
    def __init__(self):
        self
        self.set = Settings()
    
    def mysql_connetc(self):

        host = self.set.get({"section":"mysql","parameter":"host"})
        port = self.set.get({"section":"mysql","parameter":"port"})
        user = self.set.get({"section":"mysql","parameter":"user"})
        password = self.set.get({"section":"mysql","parameter":"password"})
        database = self.set.get({"section":"mysql","parameter":"db"})
       
        try:
            conn = mysql.connector.connect(
            host = host,#"127.0.0.1",
            port = port,#"3306",
            user = user, #"root",
            password = password, #"emrehliug",
            database = database #"api_footbal_tst"
            # database="api-football-new"
        )
        except Exception as excpt:
            log.exception(excpt)

        return conn
    
    def mysql_upd_fixture(self,fields):
        mysql = self.mysql_connetc()
        cursor = mysql.cursor()
        

        sqlUpd  = "update fixtures"
        sqlUpd += "   set referee = %s,"
        sqlUpd += "       date = %s,"
        sqlUpd += "       status = %s,"
        sqlUpd += "  	  winner = %s"
        sqlUpd += " where id = %s"

        if len(fields) > 1:
            cursor.executemany(sqlUpd,fields)
        else: cursor.execute(sqlUpd,fields)
        
        mysql.commit()

        return cursor



    def mysql_select(self,sqlSelect=None,tableName=None,sqlPar=None,type=None):

        connInsert = self.mysql_connetc()
        cursor = connInsert.cursor()
        
        if sqlSelect == None:
            sqlSelect = "SELECT * FROM "+ tableName +" WHERE 1=1 "
            sqlValues = []

        
            if sqlPar:
                for itemId,itemValue in sqlPar.items():

                    if type(itemValue) is list:

                            sqlSelect = sqlSelect+"AND "+ itemId +" in ("
                            for i in itemValue:

                                if len(itemValue)-1 == itemValue.index(i):
                                    sqlSelect = sqlSelect+"%s"
                                else:
                                    sqlSelect = sqlSelect+"%s,"

                                sqlValues.append(i)

                            sqlSelect = sqlSelect+")"
                    else:
                        sqlSelect = sqlSelect+"AND "+ itemId +" = %s "
                        sqlValues.append(itemValue)

            #print(sqlSelect)
            #cursor.execute(sqlSelect,sqlValues)
            
            try:
                cursor.execute(sqlSelect,sqlValues)
            except Exception as excpt:
                log.exception(excpt)
            

        else:
            #print(sqlSelect)
            #cursor.execute(sqlSelect)

            try:
                cursor.execute(sqlSelect)
            except Exception as excpt:
                log.exception(excpt)
        
        
        sqlResult = cursor.fetchall()
        cursor.close()

        if sqlResult == []:
            dictResult = None
        
        else:
            dictResult = {}

            for iCurDes in range(len(cursor.description)):
                dictResult[cursor.description[iCurDes][0]]=[]
                for row in sqlResult:
                    dictResult[cursor.description[iCurDes][0]].append(row[iCurDes])

        sqlReturn = {"dict":dictResult,
                    "list":sqlResult}
        
        if type is None:
            return dictResult #dictResult
        else: return sqlResult
        

    def mysql_select_old(self,sql):

        connInsert = self.mysql_connetc()
        cursor = connInsert.cursor()

        cursor.execute(sql)
        sqlResult = cursor.fetchall()

        cursor.close()
        connInsert.close()

        return sqlResult


    def mysql_insert(self,sqlInsert,sqlPar,multiInsert=0):

        connInsert = self.mysql_connetc()
        cursor = connInsert.cursor()

        if multiInsert == 0:
            cursor.execute(sqlInsert,sqlPar)
            connInsert.commit()

            rows = cursor.lastrowid
        else:
            cursor.executemany(sqlInsert,sqlPar)
            connInsert.commit()
            
            rows = cursor.rowcount

        # Close the cursor and connection to the database
        cursor.close()
        connInsert.close()
        
        return rows
        
    def mysqlInsert_fixture(self,data):

        table = "fixtures"

        fixturesAdd = []
        for item in data:

            #winner = 'draw'
            if item["teams"]["home"]["winner"]:
               winner = 'home'
            elif item["teams"]["away"]["winner"]:
                winner = 'away'
            else: winner = None

            fixturesAdd.append((item["fixture"]["id"],
                                item["fixture"]["referee"],
                                item["fixture"]["date"],
                                item["league"]["id"],
                                item["league"]["season"],
                                item["teams"]["home"]["id"],
                                item["teams"]["away"]["id"],
                                item["fixture"]["status"]["short"],
                                winner))

        sql = "INSERT INTO "+ table +" (id, referee, date, league, season, home, away, status, winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.mysql_insert(sql,fixturesAdd,2)

        return


    def insertRapidApi(self,data,table,param=None):

        
        if table == "countries":
            aCountries = []

            for item in data:

                print(item)
        
                if item["flag"] == None:
                    item["flag"] == "NULL"
                
                if item["code"] == None:
                    item["code"] == "NULL"

                aCountries.append((item["name"], item["code"], item["flag"]))

            sql = "INSERT INTO " + table + " (name, id, flag) VALUES (%s, %s, %s)"
            #self.mysql_insert(sql,aCountries,2)

            try:
                self.mysql_insert(sql,aCountries,2)
            except Exception as excpt:
                log.exception(excpt)
            

        elif table == "leagues":

            print("LEAGUES...")
            for item in data:

                log.info("> LEAGUES < NAME: " + item["league"]["name"] + " | ID: " + str(item["league"]["id"]))
                

                if item["league"]["logo"] == None:
                    item["league"]["logo"] == "NULL"
                
                sql = "INSERT INTO " + table + " (league, id, logo, country, country_name, flag) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (item["league"]["name"],
                            item["league"]["id"],
                            item["league"]["logo"],
                            item["country"]["code"],
                            item["country"]["name"],
                            item["country"]["flag"])

                #self.mysql_insert(sql,values)

                try:
                    self.mysql_insert(sql,values)
                except Exception as excpt:
                    log.exception(excpt)
                
                print("SEASONS...")
                aSeasons = []
                for season in item["seasons"]:
                    log.info("> SEASONS < NAME: " + item["league"]["name"] + " | ID: " + str(item["league"]["id"]) + " | SEASON: " + str(season["year"]))

                    if season["end"] == None:
                        season["end"] == "NULL"

                    aSeasons.append((season["year"],
                                    season["start"],
                                    season["end"],
                                    season["current"],
                                    item["league"]["id"]
                                    ))

                sql = "INSERT INTO seasons (year, start, end, current, league) VALUES (%s, %s, %s, %s, %s)"
                #self.mysql_insert(sql,aSeasons,2)

                try:
                    self.mysql_insert(sql,aSeasons,2)
                except Exception as excpt:
                    log.exception(excpt)

        elif table == "teams":

            teamsAdd = []
            for item in data:
                
                existTeam = self.mysql_select(None,table,{"id":item["team"]["id"]})
                if existTeam is None:
                    teamsAdd.append((item["team"]["id"],
                                    item["team"]["code"],
                                    item["team"]["name"],
                                    item["team"]["logo"]))

            sql = "INSERT INTO "+ table +" (id, code, name, logo) VALUES (%s, %s, %s, %s)"
            #self.mysql_insert(sql,teamsAdd,2)

            try:
                self.mysql_insert(sql,teamsAdd,2)
            except Exception as excpt:
                log.exception(excpt)

            

        

        elif table == "events":
            
            #eventsAdd = data
            eventsAdd = []
            for item in data:

                eventsAdd.append((
                    param["fixture"],
                    item["team"]["id"],
                    item["time"]["elapsed"],
                    item["type"],
                    item["detail"],
                    item["time"]["extra"]
                ))
                

            sql = "INSERT INTO "+ table +" (fixture, team, time, type, detail, extra_time) VALUES (%s, %s, %s, %s, %s, %s)"
            #self.mysql_insert(sql,eventsAdd,2)
            #print("EVENTOS ADICIONADOS")

            try:
                self.mysql_insert(sql,eventsAdd,2)
            except Exception as excpt:
                log.error(table +" nao foram inseridos.")
                log.exception(excpt)
                

        elif table == "fixtures":
            
            fixturesAdd = []
            for item in data:

                if item["teams"]["home"]["winner"]:
                   winner = 'home'
                elif item["teams"]["away"]["winner"]:
                    winner = 'away'
                else: winner = None

                fixturesAdd.append((
                    item["fixture"]["id"],
                    item["fixture"]["referee"],
                    item["fixture"]["date"],
                    item["league"]["id"],
                    item["league"]["season"],
                    item["teams"]["home"]["id"],
                    item["teams"]["away"]["id"],
                    item["fixture"]["status"]["short"],
                    winner
                ))

            sql = "INSERT INTO "+ table +" (id, referee, date, league, season, home, away, status, winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            #self.mysql_insert(sql,fixturesAdd,2)

            try:
                self.mysql_insert(sql,fixturesAdd,2)
            except Exception as excpt:
                log.exception(excpt)

        