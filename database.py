from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 🔑 Paste your Supabase connection string here
DATABASE_URL =  "postgresql://postgres:Loanzage%40*12@db.laezukqmsutahwmjcsyo.supabase.co:5432/postgres"

# Create engine (Supabase PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

# Session (used to talk to DB)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency helper (optional but good practice)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()