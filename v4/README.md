# CRISPR Short — v4 (gerçek görseller + müzik + profesyonel animasyon)

Çıktı: `CRISPR_short_v4.mp4` · 1080×1920 · 30 fps · 28,5 sn · -14 LUFS

## v3'e göre yenilikler

- **Gerçek görseller:**
  - Orak hücre sahnesinde gerçek bir hasta kan yayması var. Yavaş zoom yapılıyor ve tek bir orak hücre elle çizilmiş daireyle işaretleniyor.
  - İyileşme sahnesinde sağlıklı bir alyuvarın elektron mikroskobu fotoğrafı, polaroid kart olarak giriyor.
- **Müzik:** Kevin MacLeod'un "Lightless Dawn" parçasının 3:38'den başlayan bölümü kullanıldı. Konuşma yokken -27 LUFS, konuşma sırasında 7 dB daha kısılıyor (otomatik ducking). Sonda 0,45 sn yumuşak kısılma var.
- **Geçişler:** Sahneler arasında yatay kayma ve hareket bulanıklığıyla "whip-pan" geçişi yapılıyor.
- **Başlıklar:** Her başlık kelime kelime, maske içinden yukarı kayarak beliriyor (sıralı animasyon).
- **Derinlik:** Arka planda yavaş süzülen yumuşak renk lekeleri ve her karede kayan film greni var.

## Üretim

```bash
python3 audio.py <orijinal.mp4> audio.wav "Lightless Dawn.mp3"
node render.js video silent.mp4
ffmpeg -i silent.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart CRISPR_short_v4.mp4
```

Müzik bölümü ve seviyeleri `audio.py` içinde ayarlanır: `MUSIC_START`, `MUSIC_LUFS`, `DUCK_DB`.

## YouTube açıklamasına eklenmesi ZORUNLU kaynaklar (CC BY lisansı gereği)

```
Music: "Lightless Dawn" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

Sickle cell blood smear photo: Ed Uthman, CC BY 2.0, via Wikimedia Commons
https://commons.wikimedia.org/wiki/File:Sickle_Cell_Anemia_(5610746554).jpg

Red blood cell SEM image: NCI-Frederick Electron Microscopy Facility, public domain, via Wikimedia Commons
https://commons.wikimedia.org/wiki/File:Red_White_Blood_cells.jpg
```

## Görseller (`img/`)

| Dosya | Kaynak | Lisans |
|---|---|---|
| `sickle_smear.jpg` → `smear.jpg` (kırpılmış) | Ed Uthman, Wikimedia Commons | CC BY 2.0 |
| `rbc_sem.jpg` → `rbc.jpg` (kırpılmış, büyütülmüş) | NCI-Frederick, Wikimedia Commons | Public domain |

`candidates.json` incelenen diğer adayları ve lisanslarını içerir. CC BY-SA görseller, share-alike şartı
videoyu da bağlayabileceği için kullanılmadı.

## Bilinen sınırlar

- Anlatım orijinal kayıttır. Yeni metin ve doğal bir anlatıcı sesi için Higgsfield'da ~1,8 kredi gerekiyor
  (ElevenLabs motoru).
- NCI görselinin aslı 500 px genişliğinde, polaroid kartta 2 kat büyütüldü (hafif yumuşaklık olabilir).
