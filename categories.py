from recipe_parser import clean_name

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
    ("tavuk", "Tavuk", {"tavuk", "tavuklu", "kanat"}),
    ("et", "Et ve köfte", {"köfte", "köftesi", "kebap", "kebabı", "kıymalı", "dana", "kuzu"}),
    ("sebze", "Sebze ve zeytinyağlı", {"zeytinyağlı", "sebzeli", "sebze", "ıspanaklı", "dolma", "dolması",
                                       "sarma", "sarması", "mercimek", "nohut", "fasulye", "karnıyarık",
                                       "patlıcan", "graten", "mücver", "brokoli", "karnabahar", "pırasa",
                                       "patates", "kabak", "bamya", "biber"}),
]
DEFAULT = ("diger", "Diğer")


def categorize(title):
    """Tarif adından kategori bulur: 'Kekikli Tavuk' → ('tavuk', 'Tavuk')"""
    words = set(clean_name(title).split())
    for key, label, keywords in CATEGORIES:
        if words & keywords:
            return key, label
    return DEFAULT