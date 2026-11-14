"""Malzeme eşleştirme: elimizdekiler tarifin malzemelerini karşılıyor mu?

Modelden bağımsız, saf mantık. Bu yüzden testleri modeli yüklemeden saniyeler içinde çalışır.
"""

# Kullanıcının "evde hep var" diye işaretleyebileceği temel malzemeler
PANTRY_OPTIONS = ("tuz", "su", "sıvı yağ", "zeytinyağı", "karabiber", "pul biber", "şeker")
DEFAULT_PANTRY = ("tuz", "su", "sıvı yağ")

# "X varsa bunlar da vardır": bir malzemenin parçaları ya da ondan hemen elde edilenler
DERIVED = {
    "yumurta": ["yumurta akı", "yumurta sarısı"],
    "limon": ["limon suyu", "limon kabuğu rendesi"],
    "portakal": ["portakal suyu", "portakal kabuğu rendesi"],
}


def expand(have):
    """Elimizdekilere onlardan elde edilenleri de ekler.
    {"yumurta"} → {"yumurta", "yumurta akı", "yumurta sarısı"}
    """
    result = set(have)
    for item in have:
        result.update(DERIVED.get(item, []))
    return result


def has(ingredient, available):
    """Elimizdekiler bu malzemeyi karşılıyor mu?
    "yağlı kıyma", {"kıyma"} → True
    "limon suyu",  {"su"}    → False
    """
    for item in available:
        if ingredient == item or ingredient.endswith(" " + item):
            return True
    return False


def missing(ingredients, have, pantry=()):
    """Tarifin, kullanıcıda olmayan malzemelerini döndürür.
    pantry: kullanıcının "evde hep var" diye işaretledikleri
    """
    available = expand(have) | set(pantry)
    return [i for i in ingredients if not has(i, available)]


def uses_all(ingredients, have):
    """Tarif, kullanıcının seçtiği HER malzemeyi kullanıyor mu?"""
    return all(
        any(has(ingredient, expand({item})) for ingredient in ingredients)
        for item in have
    )