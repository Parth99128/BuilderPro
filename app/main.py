"""
BuildPro Backend API — Construction Management Platform
========================================================
FastAPI + SQLAlchemy (async) + SQLite + scikit-learn

Features:
  • JWT Authentication (register/login)
  • Projects CRUD with phases
  • Inventory CRUD + QR code generation + material usage logging
  • Payments & Payroll CRUD
  • Invoice generation with auto GST + auto numbering
  • Geo-tagged delivery tracking
  • AI demand forecasting (scikit-learn linear regression)
  • Automated invoice reconciliation
  • Smart alert engine
  • Analytics dashboard

API Key section left blank — configure via environment variables:
  AI_PROVIDER, AI_API_KEY, AI_ENDPOINT
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .config import APP_NAME, APP_VERSION
from .routers import auth, projects, inventory, payments, invoices, deliveries, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="High-end construction management backend with AI forecasting, invoice reconciliation, and smart alerts.",
    lifespan=lifespan,
)

# CORS — allow all origins for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(inventory.router)
app.include_router(payments.router)
app.include_router(invoices.router)
app.include_router(deliveries.router)
app.include_router(analytics.router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/auth/register, /api/auth/login, /api/auth/me",
            "projects": "/api/projects (CRUD + phases)",
            "inventory": "/api/materials (CRUD + /log + /qr/{code})",
            "payments": "/api/transactions (CRUD), /api/workers (CRUD)",
            "invoices": "/api/invoices (CRUD + auto GST + numbering)",
            "deliveries": "/api/deliveries (CRUD + geo-tagging)",
            "analytics": "/api/analytics/dashboard, /forecast, /reconciliation, /alerts",
        },
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
