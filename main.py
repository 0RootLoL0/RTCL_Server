import time
import json
import bcrypt
import sqlite3
import secrets
import datetime
import configparser
from re import *
from flask import Flask, request, g
app = Flask(__name__)
config = configparser.ConfigParser()
config.read("rtclServer.conf")

def connect_db():
    rv = sqlite3.connect(config.get("server", "urldb"))
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def isAddress(address):
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
    is_valid = pattern.match(address)
    if is_valid:
        return True
    else:
        return False

def isLesson(minStart, minEnd, inMin):
    if minStart <= inMin and minEnd >= inMin:
        return True
    else:
        return False

def getNumLesson(tables, min):
    Lesson = 0
    if not min < tables[0]["StartMinL"]:
        for table in tables:
            if isLesson(table["StartMinL"], table["EndMinL"] , min):
                break
            else:
                Lesson += 1
        Lesson+=1
    

    return {"count": len(tables), "num": Lesson}

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.commit()
        g.sqlite_db.close()

@app.route('/')
def hello_world():
    return 'It is api bro! Go http://github.com/0RootLoL0'

@app.route('/getTime')
def getTime():
    return str(int(time.time()))

@app.route('/loginDevice')
def loginDevice():
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    print(email, password)
    if isAddress(email):
        db = get_db()
        cur = db.execute("SELECT \"passwd_hui\",\"token_devices\" FROM \"main\".\"users_rootlolhui\" WHERE \"email\" LIKE \'"+email+"\';")
        entries = cur.fetchall()
        if len(entries) > 0:
            print(bcrypt.checkpw(password.encode("utf-8"), entries[0]["passwd_hui"].encode("utf-8")))
            if bcrypt.checkpw(password.encode("utf-8"), entries[0]["passwd_hui"].encode("utf-8")):
                return json.dumps({"mess": str(entries[0]["token_devices"])})

    return json.dumps({"mess": "error"})

@app.route('/getLesson')
def getLesson():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        now = datetime.datetime.now()
        Lesson = getNumLesson(json.loads(entries[0]["schedule_calls"]), now.hour*60+now.minute)
        print(Lesson)
        if Lesson["num"] == 0:
            mess = "не началиь"
        elif Lesson["num"] > Lesson["count"]:
            mess = "кончились"
        else:
            mess = json.loads(entries[0]["lessons_monday"])[Lesson["num"]-1]["Lesson"]
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

@app.route('/getClass')
def getClass():
    token = request.args.get('token', '')
    if token == "":
        return "{\"mess\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        now = datetime.datetime.now()
        Lesson = getNumLesson(json.loads(entries[0]["schedule_calls"]), now.hour*60+now.minute)
        print(Lesson)
        if Lesson["num"] == 0:
            mess = "не началиь"
        elif Lesson["num"] > Lesson["count"]:
            mess = "кончились"
        else:
            mess = json.loads(entries[0]["class_monday"])[Lesson["num"]-1]["class"]
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

@app.route('/getFIO')
def getFIO():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        name = entries[0]["name"]
        lastname = entries[0]["lastname"]
        mess = lastname +" "+name
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
@app.route('/addMessYA')
def addMessYA():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        db.execute('UPDATE "main"."users_rootlolhui" SET "mess_ya"='+str(entries[0]["mess_ya"] + 1)+' WHERE "token_clock"=\''+str(int(token))+'\';')
        db.commit()
        mess = "ok"
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

@app.route('/getMessYA')
def getMessYA():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        mess = str(entries[0]["mess_ya"])
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
@app.route('/addMessInfo')
def addMessInfo():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        db.execute('UPDATE "main"."users_rootlolhui" SET "mess_info"='+str(entries[0]["mess_info"] + 1)+' WHERE "token_clock"=\''+str(int(token))+'\';')
        db.commit()
        mess = "ok"
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

@app.route('/getMessInfo')
def getMessInfo():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        mess = str(entries[0]["mess_info"])
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
@app.route('/addMessTrig')
def addMessTrig():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        db.execute('UPDATE "main"."users_rootlolhui" SET "mess_trig"='+str(entries[0]["mess_trig"] + 1)+' WHERE "token_clock"=\''+str(int(token))+'\';')
        db.commit()
        mess = "ok"
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})

@app.route('/getMessTrig')
def getMessTrig():
    token = request.args.get('token', '')
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+str(int(token))+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        mess = str(entries[0]["mess_trig"])
    else:
        mess = "you invalid"
    return json.dumps({"mess": str(mess)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5010)
