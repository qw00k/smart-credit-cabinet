import pytesseract
from PIL import Image
import re
import io

def izvlech_dannye_kompanii(izobrazhenie_bytes: bytes) -> dict:
    izobrazhenie = Image.open(io.BytesIO(izobrazhenie_bytes))
    tekst = pytesseract.image_to_string(izobrazhenie, lang="rus")

    sovpadenie_inn = re.search(r'ИНН\s*(\d{10})', tekst)
    sovpadenie_ogrn = re.search(r'ОГРН\s*(\d{13})', tekst)
    sovpadenie_nazvaniya = re.search(r'(ООО|ИП)\s+[«"]?([^»"\n]+)', tekst)

    return {
        "inn": sovpadenie_inn.group(1) if sovpadenie_inn else None,
        "ogrn": sovpadenie_ogrn.group(1) if sovpadenie_ogrn else None,
        "nazvanie_kompanii": sovpadenie_nazvaniya.group(2).strip() if sovpadenie_nazvaniya else None,
        "syroi_tekst": tekst[:500],
    }
