STOP_MARKERS = (
    "Eksik malzemeleri",
    "Nasıl Yapılır?",
    "Besin Değerlerini",
    "Görmek İçin",
    "Püf Noktası",
    "Pişirme Önerisi",
    "KALORİ",
)

def extract_ingredient_lines(text: str) -> list[str]:
    """Tarif metninden ham malzeme satırlarını çıkarır.
    Örn: ['100gramtereyağı', '1adetyumurta', ...]
    """
    start = text.find("İçin Malzemeler")
    if start == -1:
        return []

    lines = text[start:].split("\n")[1:]

    ingredients = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(marker in line for marker in STOP_MARKERS):
            break
        if line.endswith((":", ";")) or line.rstrip(".").endswith(("için", "İçin")):
            continue
        ingredients.append(line.removeprefix("- "))
    return ingredients