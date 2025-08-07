from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from datetime import datetime
from time import time
import logging
import traceback

from app.config import settings
from app.database import get_db
from app.router_registry import ROUTERS

# ========================================
# 🔧 Logging Setup
# ========================================
logging.basicConfig(
    level=logging.INFO if settings.APP_ENV == "production" else logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ========================================
# 📚 OpenAPI Metadata
# ========================================
tags_metadata = [
    {"name": "🔐 Auth", "description": "Endpoints for registration, login, logout, password reset, and JWT management."},
    {"name": "👤 Users", "description": "Manage user profiles, roles, and customer-related data."},
    {"name": "🏦 Accounts", "description": "Create, update, and manage bank accounts."},
    {"name": "💸 Transactions", "description": "Money transfers, deposits, withdrawals, and history."},
    {"name": "💰 Loans", "description": "Loan applications, approvals, rejections, and repayments."},
    {"name": "📈 Investments", "description": "Planned investment options like stocks and savings."},
    {"name": "🛠️ Admin", "description": "Admin-level operations and dashboards."},
    {"name": "📋 Audit Logs", "description": "Track system and user activity for compliance."},
    {"name": "🧾 Bill Payments", "description": "Pay utilities, subscriptions, and other services."},
    {"name": "⚙️ Profile", "description": "User preferences, security settings, and personal info."},
    {"name": "💳 Card Services", "description": "Issue and manage debit, credit, and virtual cards."},
    {"name": "📡 System", "description": "Health checks, version info, and root documentation."},
]

# ========================================
# 🚀 FastAPI App Initialization
# ========================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A secure digital banking and investment backend platform.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata,
)

# ========================================
# 🗂️ Static File Mount
# ========================================
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# ========================================
# 🌐 CORS Middleware
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# 🛡️ Security Headers Middleware
# ========================================
@app.middleware("http")
async def set_secure_headers(request: Request, call_next):
    """Attach basic security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# ========================================
# 📊 Request Logging Middleware
# ========================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log method, path, and duration of each HTTP request."""
    start_time = time()
    response = await call_next(request)
    duration = round(time() - start_time, 3)
    logger.info(f"{request.method} {request.url.path} - {duration}s")
    return response

# ========================================
# 🧊 Rate Limiting Setup
# ========================================
def get_user_id_or_ip(request: Request):
    """Use authenticated user ID if available, fallback to IP address."""
    user = getattr(request.state, "user", None)
    return str(user.id) if user and hasattr(user, "id") else get_remote_address(request)

limiter = Limiter(key_func=get_user_id_or_ip)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle 429 Too Many Requests errors gracefully."""
    retry_after = exc.detail.get("remaining", 60)
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": "Rate limit exceeded. Please wait before retrying.",
            "retry_after_seconds": retry_after,
            "limit": exc.detail.get("limit", "unknown"),
        },
        headers={"Retry-After": str(retry_after)}
    )

# ========================================
# 🚨 Global Exception Handler
# ========================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled server-side exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    traceback.print_exc()
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": request.url.path
        },
    )

# ========================================
# 🧪 Health Check Endpoint
# ========================================
@app.get("/health", tags=["📡 System"])
@limiter.limit("5/minute")
async def health_check(request: Request, db: Session = Depends(get_db)):
    """Confirm database and server status."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "time": datetime.utcnow().isoformat()
        }
    except Exception:
        return {
            "status": "error",
            "database": "unavailable"
        }

# ========================================
# 👋 Root Welcome Endpoint
# ========================================
@app.get("/", tags=["📡 System"])
def welcome():
    """Basic greeting for root path."""
    return {"message": "👋 Welcome to ORiem Capital Backend API"}

# ========================================
# 🔢 Version Info Endpoint
# ========================================
@app.get("/version", tags=["📡 System"])
def get_version():
    """Get current version and environment context."""
    return {
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.utcnow().isoformat()
    }

# ========================================
# 🔌 Register All Routers
# ========================================
for router, prefix, tag in ROUTERS:
    app.include_router(router, prefix=prefix, tags=[tag])
