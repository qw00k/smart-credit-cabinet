from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import nastroiki

dvigatel = create_engine(nastroiki.DATABASE_URL)

FabrikaSessii = sessionmaker(autocommit=False, autoflush=False, bind=dvigatel)

BazoviiKlass = declarative_base()

def poluchit_bd():
    bd = FabrikaSessii()
    try:
        yield bd
    finally:
        bd.close()
