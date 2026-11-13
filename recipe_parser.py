def extract_ingredient_lines(text: str) -> list[str]:
    """Tarif metninden ham malzeme satırlarını çıkarır.
    Örn: ['100gramtereyağı', '1adetyumurta', ...]
    """
    start = text.find("İçin Malzemeler")
    if start == -1:
        return []  # Şablonsuz tarif, malzeme yok

    # Başlıktan itibaren satırlara böl; ilk eleman başlığın kendisi, onu atla
    lines = text[start:].split("\n")[1:]

    ingredients = []
    for line in lines:
        line = line.strip()
        if not line:
            continue                         # Boş satırları geç
        if line.startswith("- "):
            ingredients.append(line[2:].strip())  # "- " ön ekini at
        elif line.endswith(":"):
            continue                         # "Üzeri için:" gibi ara başlık, atla
        else:
            break                            # Kurala uymayan ilk satır = bölüm bitti
    return ingredients