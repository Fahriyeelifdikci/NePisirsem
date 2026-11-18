# Deneyler

Projeyi geliştirirken veriyi anlamak ve kararları **ölçerek** vermek için yazılmış scriptler.
Uygulamanın bir parçası değiller; kök dizinden `python -m experiments.<ad>` ile çalışırlar.

| Script | Hangi soruyu cevaplıyor? | Hangi karara yol açtı? |
|---|---|---|
| `explore.py` | Veri seti neye benziyor? | Tariflerin ortak bir şablonla yazıldığı fark edildi |
| `check_structure.py` | Tariflerin yüzde kaçı bu şablona uyuyor? | Malzeme satırlarını şablondan çıkaran ayrıştırıcı |
| `regex_playground.py` | Miktar/birim ayrıştırma örneklerde doğru çalışıyor mu? | `parse_ingredient` kuralları |
| `embedding_playground.py` | Hangi dil modeli Türkçe malzeme adlarını daha iyi ayırt ediyor? | Türkçe BERT modeli seçildi |
| `check_gr.py` | "gr" birimi veride hangi biçimlerde geçiyor? | Noktasız "gr" desteği gereksiz bulundu (veride 0 örnek) |
| `top_ingredients.py` | En sık malzeme adları ve varyantları neler? | Eşanlamlı sözlüğü, yapışık "boy" hatasının bulunması |
| `compare_datasets.py` | Ayrıştırıcıdaki bir değişiklik veriyi nasıl etkiledi? | Düzeltmelerin etkisinin ölçülmesi (ör. "soğan" eşleşmesi +%75) |
| `inspect_other.py` | Hangi tarifler "Diğer" kategorisine düşüyor? | Yeni kategori kelimeleri ("Diğer" %20,1 → %14,5) |

Arama yöntemlerinin karşılaştırması ise bir deney değil, tekrar çalıştırılabilir bir değerlendirme olduğu için
`scripts/evaluate.py` ve `nepisirsem/evaluation.py` içinde.