
from sqlalchemy import create_engine,orm
import config
import time,datetime,sys,os,pandas as pd 

'''
config = {}
config["user"] = "root"
config["password"] = "tocodetech"
config["ip"] = "localhost"
config["database"] = "myworld"


dbConfig = {
    'user':'root',
    'password':'tocodetech',
    'ip':'localhost',
    'database':'myworld'
    }

print(dbConfig['user'])

'''

def dbConnect():
    engine = create_engine('mysql+pymysql://' + config.user + ':' + config.password + '@' + config.ip + '/'+config.database+'?charset=utf8')
    dbSession = orm.sessionmaker()
    dbSession.configure(bind=engine)
    #session = dbSession()
    return engine

def execQry(engine,queryStmt,param):
	if param:
		dataFrame = pd.read_sql(queryStmt, con=engine, params=param)
	else:
		dataFrame = pd.read_sql(queryStmt, con=engine)

	return dataFrame

def connectAndExec(queryStmt,param):
	engine = dbConnect()
	if not engine == "FAILURE":
		outputDF = execQry(engine,queryStmt,param)
	dbDisConnect(engine)
	return outputDF

def dbDisConnect(engine):
	return "DISCONNECTED SUCCESS"

