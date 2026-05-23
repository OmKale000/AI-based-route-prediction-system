from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from prometheus_client import make_asgi_app

from api.routes import predict, manage
from api.routes.dashboard import router as dashboard_router

# =========================================================
# CREATE FASTAPI APP FIRST
# =========================================================

app = FastAPI(
    title="AI Route Prediction Engine",
    description="Production-grade AI-powered route optimization and prediction API.",
    version="1.0.0"
)

# =========================================================
# STATIC FILES + TEMPLATES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="frontend/templates"
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# PROMETHEUS METRICS
# =========================================================

metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)

# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    dashboard_router
)

app.include_router(
    predict.router,
    prefix="/predict",
    tags=["Prediction"]
)

app.include_router(
    manage.router,
    tags=["Management"]
)

# =========================================================
# ROOT
# =========================================================

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the AI Route Prediction Engine API.",
        "docs": "/docs",
        "dashboard": "/"
    }

# =========================================================
# HEALTH
# =========================================================

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy"
    }