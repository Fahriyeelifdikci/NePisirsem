import re

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


# --- Miktar ayrıştırma ---

# Satırın başındaki miktarı yakalayan kalıp:
# ya rakam/virgül/eğik çizgi/tire grubu, ya "Yarım" kelimesi, ya da ¾ karakteri
NUMBER = re.compile(r"^([\d.,/-]+|Yarım|¾)")

WORD_NUMBERS = {"Yarım": 0.5, "¾": 0.75}


def to_number(text):
    """Yakalanan miktar metnini sayıya çevirir: "1,5" → 1.5
    Çeviremezse None döndürür (miktar bilinmiyor).
    """
    text = text.strip("-/")                  # YENİ: baştaki/sondaki tire ve eğik çizgiyi sil

    if text in WORD_NUMBERS:
        return WORD_NUMBERS[text]

    if "-" in text:
        parts = text.split("-")
        if len(parts) != 2:                  # YENİ: tam 2 parça değilse
            return None                      #   "bilmiyorum" de, uydurma
        low, high = parts
        return (to_number(low) + to_number(high)) / 2

    if "/" in text:
        top, bottom = text.split("/")
        return float(top) / float(bottom)

    return float(text.replace(",", "."))
# --- Birim ayrıştırma ---

UNITS = sorted((
    "gram", "kilogram", "gr.","kg.", "kg", "mililitre", "litre", "ml.", "ml",
    "adet", "paket", "kutu", "kase", "çorba kasesi", "poşet", "şişe",
    "su bardağı", "çay bardağı", "bardak", "kahve fincanı", "fincan",
    "yemek kaşığı", "tatlı kaşığı", "çay kaşığı", "çorba kaşığı",
    "tutam", "çimdik", "avuç", "damla",
    "demet", "bağ", "dal", "sap", "yaprak", "diş", "dilim",
    "baş", "kare", "parça",
), key=len, reverse=True)

MODIFIERS = ("tepeleme ", "silme ", "büyük ")


def parse_ingredient(line):
    """Bir malzeme satırını üç parçaya böler.
    "100gramtereyağı" → (100.0, "gram", "tereyağı")
    Bulunamayan parça None olur.
    """
    match = NUMBER.match(line)
    if not match:                                # miktar yoksa
        return None, None, line                  #   satırın tamamı ad sayılır

    amount = to_number(match.group())
    rest = line[match.end():].strip()
    for modifier in MODIFIERS:
        rest = rest.removeprefix(modifier)

    for unit in UNITS:                           # uzundan kısaya her birimi dene
        if rest.startswith(unit):
            name = rest[len(unit):].strip()      #   birimden sonrası = ad
            return amount, unit, name

    return amount, None, rest       

# --- Ad temizleme ---
PARENS = re.compile(r"\(.*?\)")
PREP_WORDS = (
    "orta boy", "küçük boy", "büyük boy",   # uzunlar önce!
    "orta", "küçük", "büyük",
    "ılık", "sıcak", "soğuk",
    "rendelenmiş", "haşlanmış","eritilmiş","olgun",
)


def strip_prep_words(name):
    """Baştaki hal sıfatlarını siler.
    "küçük boy haşlanmış patates" → "patates"
    """
    found = True
    while found:                                 # silinecek bir şey kaldığı sürece tekrarla
        found = False
        for word in PREP_WORDS:
            if name.startswith(word + " "):      # sıfat + boşluk ile başlıyorsa
                name = name[len(word) + 1:]      #   sıfatı ve boşluğu kes
                found = True
    return name

def clean_name(name):
    """Malzeme adını aramaya uygun hale getirir.
    "İzmir tulum peyniri(rendelenmiş)" → "izmir tulum peyniri"
    "(10 gram) kabartma tozu"          → "kabartma tozu"
    """
    name = PARENS.sub("", name)                               # kapanmış (...) parçalarını sil
    name = name.split("(")[0]                                 # kapanmamış parantez kaldıysa sonrasını at
    name = name.replace("İ", "i").replace("I", "ı").lower()   # Türkçe küçük harf
    return strip_prep_words(name.strip())