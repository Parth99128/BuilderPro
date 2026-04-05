import os

# ── Security ──
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION_use_openssl_rand_hex_32")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# ── Database ──
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./buildpro.db")

# ── AI Provider (leave blank, user fills in later) ──
AI_PROVIDER = os.getenv("AI_PROVIDER", "")        # "openai" | "gemini" | "custom" | ""
AI_API_KEY = os.getenv("AI_API_KEY", "")           # user's API key
AI_ENDPOINT = os.getenv("AI_ENDPOINT", "")         # custom endpoint URL

# ── App ──
APP_NAME = "BuildPro API"
APP_VERSION = "2.0.0"
