# CRISPR Shorts — Revizyon (v2)

Kaynak: `The_First_CRISPR_Medicine_Doesnt_Fix_the_Typo.mp4` (35,1 sn)
Çıktı: `CRISPR_short_v2.mp4` (28,9 sn) — `revise_short.py` ile üretildi.

## v2'de yapılanlar (montaj)

| Sorun (v1) | Çözüm (v2) |
|---|---|
| 25–29 sn "Approved in the UK and the US at the end of 2023" hikâyeye bir şey katmıyor | Cümle ve ekranı tamamen çıkarıldı (−4,7 sn). "First CRISPR medicine" zaten onaylı olduğunu ima ediyor. |
| 33–35 sn konuşma bitti, 2 sn ölü kuyruk | Başlık kartı 0,5 sn gösterilip kesiliyor → video kendi başına döner gibi akıyor (son kare ≈ ilk kare) |
| 10–17 sn "different switch" ekranı ~7 sn neredeyse donuk | Her sahnede yavaş push-in (1.00→1.06) + 14,27 sn'de sıfırlanan ikinci zoom |
| Görsel hareket düşük | Vurgu anlarında punch-in: 0 sn (zoom-out açılış), 9,1 sn "It doesn't.", 20,3 sn "Break the switch", 26,8 sn "…the backup" |
| Ses tasarımı yok | 13 senkron SFX: sahne geçişlerinde whoosh, T'nin daire içine alınmasında / etiketlerde pop, "It doesn't" ve "Break the switch"te impact, kapanış cümlesinde chime |
| — | Ses yeniden -14 LUFS / -1,6 dBTP'ye normalize edildi (iki geçişli loudnorm) |

### Ölçümler

| | v1 | v2 |
|---|---|---|
| Süre | 35,1 sn | **28,9 sn** |
| Hareket olan karelerin oranı (fark > 0,3) | %20 | **%51** |
| En uzun donuk an | 1,63 sn | **0,93 sn** |
| Ölü kuyruk | ~2,4 sn | ~0,8 sn (döngüye bağlanan başlık kartı) |
| Loudness | -14,0 LUFS | -14,0 LUFS |

Altyazı konumu ölçüldü: y = 1376–1442 px (%72–75). Shorts arayüzünün kapattığı alt bandın (~1500 px sonrası)
üstünde kalıyor, taşımaya gerek yok.

## Tahmini puanlar (sezgisel, YouTube verisi değil)

| Kriter | v1 | v2 | v3 hedefi (aşağıdaki yeniden render ile) |
|---|---|---|---|
| Hook | 8,5 | 9 | 10 |
| Tempo | 7 | 8,5 | 9,5 |
| Ses | 8,5 | 9,5 | 10 |
| Görsel | 7 | 8 | 9,5 |
| Ekranda tutma | 7 | 8,5 | 9,5 |
| Viralite | 6,5 | 7,5 | 8,5–9 |

Dürüst not: Viraliteyi tek başına montaj belirlemez. Konunun dar bir kitleye hitap etmesi, yayın saati ve
kanalın büyüklüğü de etkili. Hiçbir revizyon 10/10'u garanti edemez, gerçek sonuç yayından sonraki
izlenme oranı ve kaydırma oranı verisinde görülür.

## v3 — Kaynak projede yeniden render için senaryo

Montajla düzeltilemeyen kısımlar (yeni animasyon / yeni seslendirme gerektiriyor):

**1. Hook (0–2 sn): konuşma 1. karede başlasın** (şu an ~0,2 sn geç başlıyor). A/B için iki seçenek:
- A (mevcut, daha sıkı): "The first CRISPR cure doesn't fix the broken gene."
- B (sonuçla açılış): "They cured sickle cell — without fixing the typo that causes it."

**2. 2–6 sn:** Orak hücre animasyonu: yuvarlak hücre → orak şekline "bükülme" hareketi (şu an iki statik hücre var).

**3. 10–17 sn (en zayıf bölüm):** Metni kısalt ve görselleştir:
> "Instead, it cuts a switch called BCL11A — in your own stem cells."

Görselde makas/CRISPR kesimi düğmeye "klik" diye vurur, düğme kırılır. Kök hücre için tek ikon yeterli,
küçük etiket kutusunu kaldır.

**4. 17–20 sn:** Doğum zaman çizelgesinde ON→OFF geçişini düğmenin kendisi yapsın (ok animasyonu).

**5. 20–24 sn:** "Baby version" için bebek ikonu, hücreler tek tek "pop" ederek dolsun (SFX hazır).

**6. Kapanış (24–28 sn):** Mevcut punchline çok iyi, aynen kalsın:
> "Sometimes the fix isn't fixing the bug. It's turning on the backup."

Ardından konuşmasız 0,3 sn sonra doğrudan açılış karesi gelsin (kusursuz döngü).

**7. Etkileşim:** Videoya CTA ekleme (döngüyü bozar). Bunun yerine sabitlenmiş yorum:
"Would you rather fix the typo or flip the switch? 🧬"

### Başlık / açıklama
- Başlık: `CRISPR didn't fix the typo — it flipped a switch 🧬`
- Alternatif: `The first CRISPR cure doesn't fix the broken gene`
- Hashtag: `#CRISPR #Science #Biology #SickleCell #Shorts`
