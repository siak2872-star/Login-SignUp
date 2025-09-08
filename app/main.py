from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import users_collection, db  # make sure 'db' exists in database.py

app = FastAPI()

# Templates and static folders (root-level)
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Test database connection (optional route)
@app.get("/test-db")
async def test_db():
    try:
        await db.command("ping")
        return {"message": "✅ Connected to MongoDB Atlas successfully!"}
    except Exception as e:
        return {"error": str(e)}

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login form submission
@app.post("/login")
async def login_user(name: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"name": name, "password": password})
    if user:
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Invalid credentials"}

# Signup page
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Signup form submission
@app.post("/signup")
async def signup_user(name: str = Form(...), password: str = Form(...)):
    user = {"name": name, "password": password}
    await users_collection.insert_one(user)
    return RedirectResponse(url="/login", status_code=303)
