DATABASE_URL: str = "sqlite:///database.db"
DATABASE_ECHO: bool = True  # prints sql queries,

# how long should session last in seconds
# 30 days = 30 * 24 * 60 * 60 = 2592000 seconds
SESSION_DURATION: int = 2592000

# Disable /docs by setting it to None
DOCS_URL: str | None = "/docs"
