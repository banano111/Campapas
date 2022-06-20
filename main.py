from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from peewee import *
from playhouse.db_url import connect
import os
import json


DATABASE_URL = os.environ['DATABASE_URL']


db = PostgresqlDatabase('d3tbuori30q68u', dsn=DATABASE_URL)

class registeredscouts(Model):
    name = CharField()
    section = CharField()

    class Meta:
        database = db

class otherquestions(Model):
    fechaCamp = CharField()
    tienda = CharField()

    class Meta:
        database = db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    db.connect()

    data = registeredscouts.select()
    data2 = otherquestions.select()

    jsonStyle = { "RegisteredPeople": []}
    jsonStyle2 = { "OtherQuestion": []}

    for member in registeredscouts.select():
        memberData = {
            "name": member.name,
            "section": member.section
        }
        
        jsonStyle["RegisteredPeople"].append(memberData)

    for other in otherquestions.select():
        otherData = {
            "fechaCamp": other.fechaCamp,
            "tienda": other.tienda
        }
        
        jsonStyle2["OtherQuestion"].append(otherData)

    db.close()
    
    dataMan = jsonStyle["RegisteredPeople"]
    dataMan2 = jsonStyle2["OtherQuestion"]

    var1 = 0
    var2 = 0
    var3 = 0
    var4 = 0
    var5 = 0
    var6 = 0
    var7 = 0

    fechaCamp1 = 0
    fechaCamp2 = 0

    tiendaS = 0
    tiendaN = 0

    for other in dataMan2:
        if other["fechaCamp"] == "Fecha1":
            fechaCamp1 += 1
        else:
            fechaCamp2 += 1
        
        if other["tienda"] == "TiendaYes":
            tiendaS += 1
        else:
            tiendaN += 1
        
    other = {
        "fecha1": fechaCamp1,
        "fecha2": fechaCamp2,
        "tiendaS": tiendaS,
        "tiendaN": tiendaN
    }
    
    for member in dataMan:
        if member["section"] == "Papás o Invitado":
            var1 += 1
        elif member["section"] == "Castores":
            var2 += 1
        elif member["section"] == "Manada":
            var3 += 1
        elif member["section"] == "Tropa":
            var4 += 1
        elif member["section"] == "Comunidad De Caminantes":
            var5 += 1
        elif member["section"] == "Clan de Rovers":
            var6 += 1
        elif member["section"] == "Scouters o Dirigentes":
            var7 += 1

    countRegistered = {
        "papas": var1,
        "castores": var2,
        "manada": var3,
        "tropa": var4,
        "comunidad": var5,
        "clan": var6,
        "scouters": var7
    }

    print(countRegistered)

    return templates.TemplateResponse("info.html", {
        "request": request,
        "data": jsonStyle,
        "asistentes": countRegistered,
        "other": other
    })

@app.post("/addUsers")
async def addUsers(users: Request):
    print("Se Ejectua Await JSON - Other")
    data = await users.json()
    print(data)
    print("Se Ejectua DB CONNECT - Other")
    db.connect()
    for user in data:
        registeredscouts.create(name=user["name"], section=user["section"])
    db.close()
    return { "user_added": "Usuario Agregado" }


@app.post("/addOtherCuestions")
async def addOthers(other: Request):
    print("Se Ejectua Await JSON - Other")
    data = await other.json()
    print(data)
    print("Se Ejectua DB CONNECT - Other")
    db.connect()
    otherquestions.create(fechaCamp=data["fechaCamp"], tienda=data["tienda"])
    db.close()
    return { "other_cuestions": "Added" }
