from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.database import engine, Base
from app.routers.auth import auth_router
from app.routers.news import news_router
from app.core.templates import templates

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS settings (optional, adjust according to your needs)
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})


# Include routers here in the future
app.include_router(auth_router)
app.include_router(news_router)