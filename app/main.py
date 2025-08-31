from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import users_collection
from .models import User
app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(name: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"name": name, "password": password})
    if user:
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Invalid credentials"}

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_user(name: str = Form(...), password: str = Form(...)):
    user = {"name": name, "password": password}
    await users_collection.insert_one(user)
    return RedirectResponse(url="/login", status_code=303)
