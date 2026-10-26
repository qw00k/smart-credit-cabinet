from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.core.database import dvigatel, BazoviiKlass, poluchit_bd, FabrikaSessii
from app.models import models
from app.schemas import schemas
from app.services import scoring, ocr_service, ai_service

BazoviiKlass.metadata.create_all(bind=dvigatel)

prilozhenie = FastAPI(title="Smart Credit Cabinet API")

prilozhenie.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@prilozhenie.on_event("startup")
def avtozapolnenie_pri_starte():
    bd = FabrikaSessii()
    try:
        if bd.query(models.KreditnyiProdukt).count() == 0:
            bd.add_all([
                models.KreditnyiProdukt(nazvanie="Oborotnyi kredit", stavka=18.0, min_summa=100000, max_summa=3000000),
                models.KreditnyiProdukt(nazvanie="Investicionnyi", stavka=15.5, min_summa=500000, max_summa=5000000),
                models.KreditnyiProdukt(nazvanie="Mikrokredit", stavka=22.0, min_summa=50000, max_summa=500000),
            ])
            bd.commit()
            print("=== База данных успешно заполнена при старте ===")
    finally:
        bd.close()


@prilozhenie.get("/")
def koren():
    return {"message": "Backend is running"}

@prilozhenie.post("/api/profiles/", response_model=schemas.ProfilOtv)
def sozdat_profil(profil: schemas.SozdatProfil, bd: Session = Depends(poluchit_bd)):
    obekt = models.ProfilBiznesa(**profil.model_dump())
    bd.add(obekt); bd.commit(); bd.refresh(obekt)
    return obekt

@prilozhenie.post("/api/applications/", response_model=schemas.ZayavkaOtv)
def sozdat_zayavku(dannye: schemas.SozdatZayavku, bd: Session = Depends(poluchit_bd)):
    zayavka = models.Zayavka(
        profil_id=dannye.profil_id, 
        produkt_id=dannye.produkt_id, 
        zaproshennaya_summa=dannye.zaproshennaya_summa, 
        srok_mesyacev=dannye.srok_mesyacev, 
        status="pending"
    )
    bd.add(zayavka); bd.commit(); bd.refresh(zayavka)
    bd.add(models.ZhurnalDeistvii(zayavka_id=zayavka.id, deistvie="created")); bd.commit()
    return zayavka

@prilozhenie.get("/api/applications/", response_model=List[schemas.ZayavkaOtv])
def spisok_zayavok(bd: Session = Depends(poluchit_bd)):
    return bd.query(models.Zayavka).order_by(models.Zayavka.id.desc()).all()

@prilozhenie.get("/api/applications/{zayavka_id}", response_model=schemas.ZayavkaOtv)
def poluchit_zayavku(zayavka_id: int, bd: Session = Depends(poluchit_bd)):
    obekt = bd.query(models.Zayavka).get(zayavka_id)
    if not obekt: raise HTTPException(404, "Not found")
    return obekt

@prilozhenie.post("/api/applications/{zayavka_id}/decision", response_model=schemas.ZayavkaOtv)
def prinyat_reshenie(zayavka_id: int, reshenie: schemas.ResheniePoZayavke, bd: Session = Depends(poluchit_bd)):
    obekt = bd.query(models.Zayavka).get(zayavka_id)
    if not obekt: raise HTTPException(404, "Not found")
    obekt.status = reshenie.reshenie
    bd.add(models.ZhurnalDeistvii(zayavka_id=zayavka_id, deistvie="decision", kommentarii=reshenie.kommentarii))
    bd.commit(); bd.refresh(obekt)
    return obekt

@prilozhenie.get("/api/recommendations/{profil_id}")
def rekomendacii(profil_id: int, bd: Session = Depends(poluchit_bd)):
    profil = bd.query(models.ProfilBiznesa).get(profil_id)
    if not profil: raise HTTPException(404, "Not found")
    produkty = bd.query(models.KreditnyiProdukt).all()
    bezopasnaya = scoring.poschitat_bezopasnuyu_summu(profil.vyruchka, profil.rashody, profil.dolgi)
    ball = scoring.poschitat_ball(profil)
    rekomendovannye = scoring.podobrat_produkty(profil, produkty)
    return {
        "bezopasnaya_summa": bezopasnaya, 
        "ball": ball, 
        "produkty": [{"id": p.id, "nazvanie": p.nazvanie, "stavka": p.stavka} for p in rekomendovannye]
    }

@prilozhenie.post("/api/ocr/")
async def zagruzit_dokument(fail: UploadFile = File(...)):
    soderzhimoe = await fail.read()
    return ocr_service.izvlech_dannye_kompanii(soderzhimoe)

@prilozhenie.post("/api/ai/ask")
async def sprosit_ii_endpoint(zapros: schemas.ZaprosII):
    podskazka = f"Ты — дружелюбный кот-финансист. Отвечай кратко, по-русски. Вопрос: {zapros.vopros}. Контекст: {zapros.kontekst}"
    otvet = await ai_service.sprosit_ii(podskazka)
    return {"otvet": otvet}

@prilozhenie.post("/api/seed/")
def zapolnit_spravochnik(bd: Session = Depends(poluchit_bd)):
    if bd.query(models.KreditnyiProdukt).count() == 0:
        bd.add_all([
            models.KreditnyiProdukt(nazvanie="Oborotnyi kredit", stavka=18.0, min_summa=100000, max_summa=3000000),
            models.KreditnyiProdukt(nazvanie="Investicionnyi", stavka=15.5, min_summa=500000, max_summa=5000000),
            models.KreditnyiProdukt(nazvanie="Mikrokredit", stavka=22.0, min_summa=50000, max_summa=500000),
        ])
        bd.commit()
    return {"status": "seeded"}