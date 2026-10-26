import httpx
from app.core.config import nastroiki

ZAPASNYE_OTVETY = {
    "hello": "Привет! Я кот-финансист. Давай подберём тебе кредит!",
    "think": "Секунду, я считаю твои показатели...",
    "advice": "Твой профиль выглядит надёжно. Рекомендую этот кредит.",
    "warn": "Осторожно! Эта сумма может быть рискованной для твоего бизнеса.",
    "happy": "Ура! Твой кредит одобрен!",
}

async def sprosit_ii(zapros: str, klyuch_zapasa: str = "advice") -> str:
    try:
        async with httpx.AsyncClient(timeout=15.0) as klient:
            otvet = await klient.post(
                f"{nastroiki.OLLAMA_URL}/api/generate",
                json={"model": nastroiki.OLLAMA_MODEL, "prompt": zapros, "stream": False},
            )
            if otvet.status_code == 200:
                tekst = otvet.json().get("response", "").strip()
                if tekst: return tekst
    except Exception as oshibka:
        print(f"Ollama error: {oshibka}")
    return ZAPASNYE_OTVETY.get(klyuch_zapasa, "Я рядом и готов помочь!")
