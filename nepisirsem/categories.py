from nepisirsem.recipe_parser import clean_name

# (dosya adı, görünen ad, anahtar kelimeler) — sıra önemli: ilk eşleşen kazanır
CATEGORIES = [
    ("kurabiye", "Kurabiye", {"kurabiye", "kurabiyesi", "kurabiyeler", "cookie", "kömbe"}),
    ("kek", "Kek", {"kek", "keki", "kekler", "muffin", "cupcake", "kapkek"}),
    ("pasta", "Pasta ve cheesecake", {"pasta", "pastası", "cheesecake", "tart", "turta", "rulo",
                                      "galette", "tartolet"}),
    ("tatli", "Tatlı", {"tatlı", "tatlısı", "tatlıları", "muhallebi", "brownie", "sütlaç", "helva",
                        "helvası", "puding", "dondurma", "baklava", "tiramisu", "supangle", "şekerpare",
                        "lokma", "manolya", "crumble", "revani", "kazandibi", "profiterol", "trileçe",
                        "sufle", "güllaç", "mus"}),
    ("corba", "Çorba", {"çorba", "çorbası"}),
    ("salata", "Salata", {"salata", "salatası"}),
    ("icecek", "İçecek", {"limonata", "smoothie", "milkshake", "ayran", "şerbet", "şerbeti",       # YENİ
                          "kahve", "kahvesi", "çay", "çayı", "kokteyl", "latte", "frappe"}),
    ("meze", "Meze ve kahvaltılık", {"meze", "mezesi", "ezme", "ezmesi", "humus", "haydari",
                                     "omlet", "menemen", "kahvaltılık", "kısır", "cacık", "muhlama",
                                     "pankek", "krep", "reçel", "reçeli", "granola"}),
    ("makarna", "Makarna", {"makarna", "makarnası", "erişte", "spagetti", "mantı", "mantısı"}),
    ("pilav", "Pilav", {"pilav", "pilavı", "bulgur", "risotto"}),
    ("borek", "Börek ve poğaça", {"börek", "böreği", "poğaça", "poğaçası", "çörek", "açma", "simit",
                                  "çibörek", "gözleme", "gözlemesi", "katmer", "pişi", "milföy"}),
    ("ekmek", "Ekmek, pizza ve sandviç", {"ekmek", "ekmeği", "pizza", "pizzası", "pide", "pidesi",
                                          "lahmacun", "bazlama", "bazlaması", "focaccia", "tost",
                                          "tostu", "burger", "sandviç", "kanepe", "dürüm", "wrap"}),
    ("balik", "Balık ve deniz ürünleri", {"balık", "balığı", "somon", "levrek", "çupra", "hamsi",
                                          "karides", "midye", "ton", "alabalık"}),
    ("tavuk", "Tavuk", {"tavuk", "tavuklu", "kanat", "hindi"}),
    ("et", "Et ve köfte", {"köfte", "köftesi", "kebap", "kebabı", "kıymalı", "dana", "kuzu", "etli"}),
    ("sebze", "Sebze ve zeytinyağlı", {"zeytinyağlı", "sebzeli", "sebze", "ıspanaklı", "dolma", "dolması",
                                       "sarma", "sarması", "mercimek", "nohut", "fasulye", "karnıyarık",
                                       "patlıcan", "graten", "mücver", "brokoli", "karnabahar", "pırasa",
                                       "patates", "kabak", "bamya", "biber"}),
]

DEFAULT = ("diger", "Diğer")

# Başlıkta kelime kelime bakınca yanılan yemekler: önce bunlar kontrol edilir.
# (kalıp, kategori, şart koşulan malzeme ya da None)
PHRASES = [
    ("tavuk göğsü", "tatli", "şeker"),   # tatlı olan şekerlidir; "Fırında Tavuk Göğsü" tavuk kalır
    ("çiğ köfte", "meze", None),
    ("mercimek köftesi", "meze", None),
]

# "Et ve köfte" kategorisi için tarifte gerçekten et olmalı
MEAT_WORDS = {"et", "eti", "kıyma", "kıyması", "dana", "kuzu", "kuşbaşı", "bonfile", "biftek", "antrikot"}

LABELS = {key: label for key, label, _ in CATEGORIES}


def has_meat(ingredients):
    """Malzemelerden en az biri et mi? ["kuşbaşı dana eti", "soğan"] → True"""
    return any(word in MEAT_WORDS for ing in ingredients for word in ing.split())


def categorize(title, ingredients=None):
    """Tarif adından (ve varsa malzemelerden) kategori bulur.
    'Kekikli Tavuk'               → ('tavuk', 'Tavuk')
    'Patates Köftesi', [patates…] → et yok, 'Et ve köfte' atlanır → ('sebze', ...)
    ingredients=None: malzemeler bilinmiyor, et kontrolü yapılmaz
    """
    if ingredients is not None:
        ingredients = list(ingredients)                # parquet'ten numpy dizisi gelir, listeye çevir
    name = clean_name(title)
    for phrase, key, required in PHRASES:
        if phrase in name and (required is None or (ingredients and required in ingredients)):
            return key, LABELS[key]

    words = set(name.split())
    for key, label, keywords in CATEGORIES:
        if key == "et" and ingredients is not None and not has_meat(ingredients):
            continue                                  # "köfte" diyor ama et yok
        if words & keywords:
            return key, label
    return DEFAULT