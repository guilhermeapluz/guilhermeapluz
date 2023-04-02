import logging as log
import json

class SaveFile:
    
    def __init__(self):
        self.jsonPath = "C:\\Users\\guilh\\Documents\\api_footbal\\json\\"
        return
    

    def Json(self,data,fileName):
        
        try:
            json_object = json.dumps(data, indent=4)
            with open(self.jsonPath+fileName+".json", "w") as outfile:
                outfile.write(json_object)
        except Exception as excpt:
            log.exception(excpt)

        