from datasets import load_dataset

# Hugging Face'ten veri setini indir (ilk seferde biraz sürer, sonra önbellekten gelir)
ds = load_dataset("habanoz/yemek_tarif_24k_text")

print(ds)  # Kaç satır var, hangi bölümler (train/test) var?

df = ds["train"].to_pandas()  # İncelemesi kolay olsun diye pandas DataFrame'e çeviriyoruz
print(df.columns)  # Hangi sütunlar var?
print(df.iloc[0])  # İlk tarif nasıl görünüyor?
print("\n" + "=" * 60)
print("TAM METİN:")
print(df.iloc[0]["text"])  # Kırpmadan, olduğu gibi yazdır

print("\n" + "=" * 60)
print("METADATA:")
print(df.iloc[0]["metadata"])

print("\n" + "=" * 60)
print("İKİNCİ TARİF:")
print(df.iloc[1]["text"])  # Format her tarifte aynı mı, görmek için bir tane daha