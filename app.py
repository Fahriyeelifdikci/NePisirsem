import streamlit as st
from search import search

st.set_page_config(page_title="NePişirsem", page_icon="🍳")

st.title("🍳 NePişirsem")
st.write("Elindeki malzemeleri yaz, sana yapabileceğin tarifleri bulayım.")

query = st.text_input("Malzemeler (virgülle ayır)", placeholder="yumurta, un, süt")

if query:
    results = search(query)
    for _, row in results.iterrows():
        title = row["url"].rstrip("/").split("/")[-1].replace("-", " ").capitalize()
        st.subheader(title)
        st.caption(f"Benzerlik: {row['score']:.2f}")

        if row["n_missing"] == 0:
            st.success("✅ Bütün malzemeler var!")
        else:
            st.warning("Eksik: " + ", ".join(row["missing"]))

        st.markdown(f"[Tarife git →]({row['url']})")
        st.divider()