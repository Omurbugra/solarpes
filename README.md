# SolarPES · Enerji renovasyon senaryoları

Ankara'daki bir devlet okulunun 3B modeli üzerinde dokuz enerji renovasyon önlemini (yalıtım, pencere,
gölgeleme, ısı pompası, güneş panelleri) keşfetmeye yarayan etkileşimli sayfa. Türkçe / İngilizce.

## Yapı

- `site/` — yayınlanan sayfa (three.js, derleme adımı yok)
  - `js/data.js` sistem metinleri ve kamera açıları, `js/i18n.js` İngilizce metinler
  - `assets/school.glb` ana model, `assets/details/` teknik detay modelleri
- `rhino/` — Rhino 8 betikleri: detay modellerini kurar, ana modeli ve detayları siteye export eder
- `serve.py` — yerel geliştirme sunucusu (önbelleksiz)

## Yerelde çalıştırma

```bash
py serve.py 5173
```

Ardından `http://localhost:5173` adresini açın.

## Yayın

`main` dalına gönderilen her değişiklik `.github/workflows/pages.yml` ile GitHub Pages'a yayınlanır.
