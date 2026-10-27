# CRISPR Short — v4 (gerçek görseller + profesyonel animasyon)

Çıktı: `CRISPR_short_v4.mp4` · 1080×1920 · 30 fps · 28,5 sn · -14 LUFS

## Lisans politikası

Videoda **CC BY lisanslı hiçbir içerik yok.** Sadece public domain ve CC0 görseller kullanıldı, YouTube
açıklamasında kaynak gösterme zorunluluğu yok.

| Görsel | Kaynak | Lisans |
|---|---|---|
| `sickle_smear_cc0.jpg` → `smear.jpg` (kırpılmış) | Prof. Osaro Erhabor, Wikimedia Commons (`File:Sickle_Cell_Disease.jpg`) | CC0 |
| `rbc_sem.jpg` → `rbc.jpg` (kırpılmış, 2× büyütülmüş) | NCI-Frederick, Wikimedia Commons (`File:Red_White_Blood_cells.jpg`) | Public domain |

Fontlar SIL Open Font License'lıdır. Çizimler ve SFX bu repodaki kodla üretilir. Anlatım orijinal videodan alınmıştır.

Daha önce kullanılan "Lightless Dawn" (Kevin MacLeod, CC BY 4.0) müziği ve Ed Uthman fotoğrafı (CC BY 2.0)
bu politika gereği çıkarıldı. `candidates.json` / `candidates2.json` incelenen tüm adayları ve lisanslarını listeler.

## v3'e göre yenilikler

- **Gerçek görseller:**
  - Orak hücre sahnesinde gerçek kan yayması var. Yavaş zoom yapılıyor ve tek bir orak hücre elle çizilmiş daireyle işaretleniyor.
  - İyileşme sahnesinde sağlıklı alyuvarın elektron mikroskobu fotoğrafı polaroid kart olarak giriyor.
- **Geçişler:** Sahneler arasında yatay kayma ve hareket bulanıklığıyla "whip-pan" geçişi var.
- **Başlıklar:** Her başlık kelime kelime, maske içinden yukarı kayarak beliriyor.
- **Derinlik:** Arka planda yavaş süzülen yumuşak renk lekeleri ve her karede kayan film greni var.
- **Ses:** True peak -2,5 dBTP hedefleniyor (AAC sıkıştırması sonrası taşma olmuyor).

## Üretim

```bash
python3 audio.py <orijinal.mp4> audio.wav [müzik.mp3]   # müzik isteğe bağlı, konuşma sırasında otomatik kısılır
node render.js video silent.mp4
ffmpeg -i silent.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart CRISPR_short_v4.mp4
```

Müzik eklenecekse CC0 / public domain ya da YouTube Ses Kitaplığı'nda "atıf gerekli değil" yazan bir parça
kullanın. Bölüm ve seviye ayarları `audio.py` içinde: `MUSIC_START`, `MUSIC_LUFS`, `DUCK_DB`.

## Bilinen sınırlar

- Anlatım orijinal kayıttır. Yeni metin ve doğal bir anlatıcı sesi için Higgsfield'da ~1,8 kredi gerekiyor (ElevenLabs motoru).
- Görsellerin aslı düşük çözünürlüklü. Mikroskop görüntüsü 640 px'lik bir bölgeden, alyuvar 270 px'ten büyütüldü;
  hafif yumuşaklık olabilir.
