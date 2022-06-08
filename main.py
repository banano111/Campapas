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

    f = open('data.json')

    data = json.load(f)

    print(data)

    return templates.TemplateResponse("info.html", {
        "request": request,
        "data": data
    })

@app.post("/addUsers")
async def addUsers(users: Request):
    data = await users.json()

    for user in data:
        write_json(user)

    return { "user_added": "Usuario Agregado" }