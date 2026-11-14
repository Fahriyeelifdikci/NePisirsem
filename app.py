from collections import Counter

import streamlit as st
from nepisirsem.search import RecipeSearch
from nepisirsem.categories import categorize
from nepisirsem.matching import PANTRY_OPTIONS, DEFAULT_PANTRY
from nepisirsem.paths import ASSETS_DIR

st.set_page_config(page_title="NePişirsem", page_icon="🍳", layout="wide")
st.markdown(f"<style>{(ASSETS_DIR / 'style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Tarif motoru hazırlanıyor...")
def get_engine():
    """Modeli ve veriyi bir kez yükler; sonraki her etkileşimde aynı nesne kullanılır."""
    return RecipeSearch.from_files()


engine = get_engine()
df = engine.df


@st.cache_data
def ingredient_options():
    """Bütün malzeme adlarını sıklık sırasıyla ve en popüler 20'yi döndürür.
    Pantry malzemeleri (tuz, su...) ayrı bir yerde seçildiği için listeye girmez.
    """
    counts = Counter(i for ings in df["ingredients"] for i in ings)
    names = [name for name, _ in counts.most_common() if name not in PANTRY_OPTIONS]
    return names, names[:20]


def category_image(key):
    """Kategori görselinin yolunu döndürür, yoksa None."""
    path = ASSETS_DIR / f"{key}.jpg"
    return str(path) if path.exists() else None


all_names, popular = ingredient_options()

if "category" not in st.session_state:
    st.session_state.category = None

# ---------- Kenar çubuğu ----------
with st.sidebar:
    st.title("🍳 NePişirsem")
    picked_popular = st.pills("Popüler malzemeler", popular, selection_mode="multi") or []
    picked_search = st.multiselect("Diğer malzemeler", all_names, placeholder="Ara: kabak, nohut...")
    st.divider()
    max_missing = st.slider("En fazla eksik malzeme", 0, 5, 2)
    pantry_common = st.pills("Evde hep olanlar", PANTRY_OPTIONS, selection_mode="multi",
                             default=list(DEFAULT_PANTRY)) or []
    pantry_extra = st.multiselect("Evde hep olan başka bir şey", all_names,
                                  placeholder="Ara: un, salça...")
    pantry = set(pantry_common) | set(pantry_extra)
    require_all = st.checkbox("Seçtiklerimin hepsini kullansın")

have = set(picked_popular) | set(picked_search)

if not have:
    st.info("👈 Soldan elindeki malzemeleri seç, sana yapabileceğin tarifleri bulayım.")
    st.stop()

# ---------- Arama ----------
results = engine.search(
    have,
    top_k=300,
    candidates=3000,
    max_missing=max_missing,
    pantry=pantry,
    require_all=require_all,
)

if results.empty:
    st.warning("Bu ayarlarla tarif bulunamadı. Eksik malzeme sınırını artırmayı dene.")
    st.stop()

cats = results.apply(lambda row: categorize(row["title"], row["ingredients"]), axis=1)
results["cat_key"] = cats.str[0]
results["cat_label"] = cats.str[1]

summary = (
    results.groupby(["cat_key", "cat_label"], sort=False)
    .size()
    .reset_index(name="n")
)

# Seçili kategori artık sonuçlarda yoksa (malzemeler değiştiyse) kategori ekranına dön
if st.session_state.category not in set(summary["cat_key"]):
    st.session_state.category = None

# ---------- 1. ekran: kategoriler ----------
if st.session_state.category is None:
    st.subheader("Ne pişirmek istersin?")
    st.caption(f"{len(results)} tarif, {len(summary)} kategoride")

    cols = st.columns(3)
    for i, row in enumerate(summary.itertuples()):
        with cols[i % 3]:
            with st.container(border=True, key=f"card_cat_{row.cat_key}"):
                image = category_image(row.cat_key)
                if image:
                    st.image(image, use_container_width=True)
                st.markdown(f"**{row.cat_label}**")
                st.caption(f"{row.n} tarif")
                if st.button("Tarifleri gör", key=f"btn_{row.cat_key}", use_container_width=True):
                    st.session_state.category = row.cat_key
                    st.rerun()

# ---------- 2. ekran: seçili kategorinin tarifleri ----------
else:
    selected = results[results["cat_key"] == st.session_state.category]
    label = selected["cat_label"].iloc[0]

    if st.button("← Kategorilere dön"):
        st.session_state.category = None
        st.rerun()

    st.subheader(f"{label} · {len(selected)} tarif")

    cols = st.columns(2)
    for i, (_, row) in enumerate(selected.iterrows()):
        n_have = row["n_total"] - row["n_missing"]
        with cols[i % 2]:
            with st.container(border=True, key=f"card_{i}"):
                st.subheader(row["title"])
                st.caption(f"{n_have}/{row['n_total']} malzeme sende")
                st.progress(n_have / row["n_total"])
                if row["n_missing"] == 0:
                    st.markdown(":green-background[✅ Hemen yapabilirsin]")
                else:
                    st.markdown(" ".join(f":red-background[{m}]" for m in row["missing"]))
                st.link_button("Tarife git →", row["url"])