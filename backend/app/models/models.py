from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import BazoviiKlass

class ProfilBiznesa(BazoviiKlass):
    __tablename__ = "profili_biznesa"
    id = Column(Integer, primary_key=True, index=True)
    nazvanie_kompanii = Column(String, nullable=True)
    inn = Column(String, nullable=True)
    vyruchka = Column(Float, default=0)
    rashody = Column(Float, default=0)
    dolgi = Column(Float, default=0)
    stazh_let = Column(Integer, default=1)

class KreditnyiProdukt(BazoviiKlass):
    __tablename__ = "kreditnye_produkty"
    id = Column(Integer, primary_key=True, index=True)
    nazvanie = Column(String)
    stavka = Column(Float)
    min_summa = Column(Float)
    max_summa = Column(Float)

class Zayavka(BazoviiKlass):
    __tablename__ = "zayavki"
    id = Column(Integer, primary_key=True, index=True)
    profil_id = Column(Integer, ForeignKey("profili_biznesa.id"), nullable=True)
    produkt_id = Column(Integer, ForeignKey("kreditnye_produkty.id"), nullable=True)
    zaproshennaya_summa = Column(Float, nullable=False)
    srok_mesyacev = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    ball = Column(Integer, default=0)
    sozdana = Column(DateTime, default=datetime.utcnow)

    profil = relationship("ProfilBiznesa")
    produkt = relationship("KreditnyiProdukt")

class ZhurnalDeistvii(BazoviiKlass):
    __tablename__ = "zhurnal_deistvii"
    id = Column(Integer, primary_key=True, index=True)
    zayavka_id = Column(Integer, ForeignKey("zayavki.id"))
    deistvie = Column(String)
    kommentarii = Column(String, nullable=True)
    sozdano = Column(DateTime, default=datetime.utcnow)
