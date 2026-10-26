from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SozdatProfil(BaseModel):
    nazvanie_kompanii: Optional[str] = None
    inn: Optional[str] = None
    vyruchka: float = 0
    rashody: float = 0
    dolgi: float = 0
    stazh_let: int = 1

class ProfilOtv(BaseModel):
    id: int
    nazvanie_kompanii: Optional[str] = None
    inn: Optional[str] = None
    vyruchka: float
    rashody: float
    dolgi: float
    stazh_let: int
    class Config:
        from_attributes = True

class SozdatZayavku(BaseModel):
    profil_id: Optional[int] = None
    produkt_id: Optional[int] = None
    zaproshennaya_summa: float
    srok_mesyacev: int

class ZayavkaOtv(BaseModel):
    id: int
    zaproshennaya_summa: float
    srok_mesyacev: int
    status: str
    ball: int
    sozdana: datetime
    class Config:
        from_attributes = True

class ResheniePoZayavke(BaseModel):
    reshenie: str
    kommentarii: Optional[str] = None

class ZaprosII(BaseModel):
    vopros: str
    kontekst: Optional[str] = ""
