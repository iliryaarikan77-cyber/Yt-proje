# CRISPR Short — v3 (sıfırdan animasyon)

Çıktı: `CRISPR_short_v3.mp4` · 1080×1920 · 30 fps · 28,5 sn · -14 LUFS

## Nasıl üretilir

```bash
python3 audio.py <orijinal.mp4> audio.wav     # anlatım + SFX, -14 LUFS
node render.js video silent.mp4                # index.html -> kare kare video (Playwright)
ffmpeg -i silent.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart CRISPR_short_v3.mp4
```

Tek kare önizleme: `node render.js frames <klasör> 0 2.6 9.6 ...`

## Yapı

- **Ses:** Orijinal anlatım korunur. 0,15 sn baştan kırpılır (konuşma ilk karede başlar), "Approved in the UK and
  the US…" cümlesi çıkarılır. Sona 0,5 sn sessizlik eklenir, video başa döner. 34 senkron SFX vardır (makas,
  kalem, klavye, impact, chime, yükselen ton).
- **Görsel:** `index.html` içindeki `draw(t)` saf bir zaman fonksiyonudur, her kare deterministik üretilir.
  Doodle çizgileri saniyede 8 kez "titreşir" (boiling line), böylece el çizimi animasyon hissi verir ve
  steril yapay zekâ/vektör görünümünden uzaklaşır.
- **Altyazı:** Orijinal altyazı zamanlarından çıkarılan 31 parça kullanılır, kelime kelime vurgulanır. Açılışta
  ve "It doesn't." anında başlığın kendisi altyazı işlevi gördüğü için ayrıca altyazı gösterilmez.
- **Döngü:** Son 0,5 sn'de açılış ekranı geri gelir. Son kare ilk kareyle aynıdır.

| Sahne | Zaman | İçerik |
|---|---|---|
| Hook | 0–2,8 | Başlık kelime kelime işaretlenir, T etrafına el çizimi daire, "one wrong letter" notu |
| Orak hücre | 2,8–6,55 | Mikroskop görünümü (çizim), GAG→GTG harf dönüşü, "HBB gene" etiketi |
| Beklenen çözüm | 6,55–8,95 | Makas T'yi keser, A düşer (yeşil) |
| "It doesn't." | 8,95–9,9 | Kırmızı X, ekran sarsıntısı |
| BCL11A | 9,9–13,65 | Casgevy etiketi, anahtar, BCL11A yazılır, makas anahtarı kırar |
| Kök hücre | 13,65–16,85 | 3 adım: al → düzenle → geri ver · "no donor needed" |
| Fetal hemoglobin | 16,85–20,1 | Doğum zaman çizelgesi, ON→OFF, bebek ikonu |
| Yedek açılıyor | 20,1–24,3 | Kırık anahtar, HbF göstergesi dolar, hücreler oraklaşmayı bırakır |
| Kod metaforu | 24,3–28,0 | `fix(bug)` çizilir, `backup.enable()` yazılır |
| Döngü | 28,0–28,5 | Açılış ekranı |

## Bilimsel doğruluk notları

- Orak hücre: HBB genindeki tek nükleotid değişimi (GAG→GTG, kodon 6). İnsan genomu ~3 milyar baz çifti.
- Casgevy (exagamglogene autotemcel, exa-cel), hastanın kendi kök hücrelerinde vücut dışında (ex vivo)
  BCL11A'nın eritroid güçlendiricisini (enhancer) keser. BCL11A fetal hemoglobini baskılar. Donör gerekmez.

## Gerçek görseller (bekliyor)

Lisansı uygun gerçek görseller (Wikimedia Commons / CDC PHIL / NIH, public domain veya CC0) eklenecekti.
Ancak ortamın ağ politikası `upload.wikimedia.org`, `commons.wikimedia.org`, `phil.cdc.gov` ve
`images.pexels.com` adreslerini engelliyor. Erişim açılırsa ya da görseller yüklenirse eklenecek yerler:

1. Orak hücre sahnesi: mikroskop çizimi yerine gerçek kan yayması fotoğrafı (CDC PHIL, public domain)
2. Yedek açılıyor sahnesi: normal alyuvar SEM görüntüsü (NCI, public domain)
3. Fetal sahnesi: yenidoğan fotoğrafı (CC0)

## Lisanslar

Fontlar: Inter, JetBrains Mono, Instrument Serif, Caveat — hepsi SIL Open Font License.
Tüm çizimler ve SFX bu repodaki kodla üretildi.
