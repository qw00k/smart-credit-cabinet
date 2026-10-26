def poschitat_bezopasnuyu_summu(vyruchka: float, rashody: float, dolgi: float) -> float:
    svobodnyi_dengopotok = max(vyruchka - rashody - dolgi, 0)
    return round(svobodnyi_dengopotok * 0.4, 2)

def poschitat_ball(profil) -> int:
    ball = 50
    if profil.vyruchka > 0:
        dolgovaya_nagruzka = profil.dolgi / profil.vyruchka
        if dolgovaya_nagruzka < 0.3:
            ball += 30
        elif dolgovaya_nagruzka < 0.5:
            ball += 15
        else:
            ball -= 10
    if profil.stazh_let >= 3:
        ball += 20
    elif profil.stazh_let >= 1:
        ball += 10
    return max(0, min(ball, 100))

def podobrat_produkty(profil, produkty):
    bezopasnaya = poschitat_bezopasnuyu_summu(profil.vyruchka, profil.rashody, profil.dolgi)
    podhodyashie = [p for p in produkty if p.min_summa <= bezopasnaya <= p.max_summa]
    return sorted(podhodyashie, key=lambda x: x.stavka)[:3]
