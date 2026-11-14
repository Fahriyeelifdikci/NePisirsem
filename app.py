from collections import Counter
from pathlib import Path

import streamlit as st
from search import search, df

st.set_page_config(page_title="NePişirsem", page_icon="🍳", layout="wide")
st.markdown(f"<style>{Path('style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

@st.cache_data
def ingredient_options():
    """Bütün malzeme adlarını sıklık sırasıyla ve en popüler 20'yi döndürür."""
    counts = Counter(i for ings in df["ingredients"] for i in ings)
    names = [name for name, _ in counts.most_common()]
    return names, names[:20]


all_names, popular = ingredient_options()

if "top_k" not in st.session_state:
    st.session_state.top_k = 24

# ---------- Kenar çubuğu: malzeme seçimi ve ayarlar ----------
with st.sidebar:
    st.title("🍳 NePişirsem")

    picked_popular = st.pills("Popüler malzemeler", popular, selection_mode="multi") or []
    picked_search = st.multiselect("Diğer malzemeler", all_names, placeholder="Ara: kabak, nohut...")

    st.divider()
    max_missing = st.slider("En fazla eksik malzeme", 0, 5, 2)
    use_pantry = st.checkbox("Tuz, su, yağ evde var", value=True)
    require_all = st.checkbox("Seçtiklerimin hepsini kullansın")

have = set(picked_popular) | set(picked_search)

# ---------- Boş ekran ----------
if not have:
    st.info("👈 Soldan elindeki malzemeleri seç, sana yapabileceğin tarifleri bulayım.")
    st.stop()

# ---------- Arama ----------
results = search(
    have,
    top_k=st.session_state.top_k,
    candidates=st.session_state.top_k * 12,
    max_missing=max_missing,
    use_pantry=use_pantry,
    require_all=require_all,
)

if results.empty:
    st.warning("Bu ayarlarla tarif bulunamadı. Eksik malzeme sınırını artırmayı dene.")
    st.stop()

st.caption(f"{len(results)} tarif gösteriliyor")

# ---------- Kartlar ----------
cols = st.columns(2)
for i, (_, row) in enumerate(results.iterrows()):
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

# ---------- Daha fazla göster ----------
if len(results) == st.session_state.top_k:
    if st.button("Daha fazla göster", use_container_width=True):
        st.session_state.top_k += 24
        st.rerun()