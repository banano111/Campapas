from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["RegisteredPeople"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file)

def write_json2(new_data, filename='data2.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["OtherQuestion"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

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

    f = open('data.json')
    dataSend = json.load(f)
    data = dataSend["RegisteredPeople"]

    g = open('data2.json')
    data2 = json.load(g)
    data2 = data2["OtherQuestion"]

    for other in data2:
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
    
    for member in data:
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
        "data": dataSend,
        "asistentes": countRegistered,
        "other": other
    })

@app.post("/addUsers")
async def addUsers(users: Request):
    data = await users.json()

    for user in data:
        write_json(user)

    return { "user_added": "Usuario Agregado" }


@app.post("/addOtherCuestions")
async def addOthers(other: Request):
    data = await other.json()

    write_json2(data)

    return { "other_cuestions": "Added" }
