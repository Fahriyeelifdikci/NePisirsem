from datasets import load_dataset

df = load_dataset("habanoz/yemek_tarif_24k_text")["train"].to_pandas()

# Her işaretin kaç tarifte geçtiğini ölç
markers = {
    "Malzemeler başlığı": "İçin Malzemeler",
    "Yapılış başlığı": "Nasıl Yapılır?",
    "Reklam satırı": "Eksik malzemeleri indirimli",
}

for name, marker in markers.items():
    # str.contains her satır için True/False döner; .mean() True'ların oranını verir
    ratio = df["text"].str.contains(marker, regex=False).mean()
    print(f"{name}: %{ratio * 100:.1f}")

# Şablona uymayan tariflerden birine bakalım
missing = df[~df["text"].str.contains("İçin Malzemeler", regex=False)]
print(f"\n'İçin Malzemeler' olmayan tarif sayısı: {len(missing)}")

if len(missing) > 0:
    example = missing.iloc[0]
    print("URL:", example["metadata"]["url"])
    print(example["text"][:1500])  # İlk 1500 karakter yeter
has_marker = df["text"].str.contains("İçin Malzemeler", regex=False)

# Metin uzunluklarını karşılaştır: eksikler gerçekten kısa mı?
print("\nŞablonlu tariflerin uzunluğu (karakter):")
print(df[has_marker]["text"].str.len().describe().round(0))

print("\nŞablonsuz tariflerin uzunluğu (karakter):")
print(missing["text"].str.len().describe().round(0))

# Eksiklerde başka bir formatta malzeme listesi var mı? ("- " ile başlayan satır arıyoruz)
dash_ratio = missing["text"].str.contains("\n- ", regex=False).mean()
print(f"\nŞablonsuzların içinde '- ' satırı olan: %{dash_ratio * 100:.1f}")