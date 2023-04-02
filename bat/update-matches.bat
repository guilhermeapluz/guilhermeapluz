ECHO "=== STARTING MYSQL ==="
net start MySQL_3306

ECHO "=== UPDATING MATCHES ==="
python C:\Users\guilh\Documents\api_footbal\api-football-upd.py

ECHO "=== STOPING MYSQL ==="
net stop MySQL_3306