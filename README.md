# Simulasi Penyebaran Berita Palsu (Fake News Spread Simulation)

Proyek ini adalah simulasi **Agent-Based Modelling (ABM)** untuk memodelkan bagaimana misinformasi (berita palsu) dan koreksinya menyebar di dalam jejaring sosial. Model ini dibangun menggunakan Python dan library **Mesa**.

link github: https://github.com/Lukman1085/Fake_News_Spread_Model

Proyek ini terinspirasi oleh paper: *"Can We Stop Fake News? Using Agent-Based Modelling to Evaluate Countermeasures for Misinformation on Social Media"*.

link paper: https://workshop-proceedings.icwsm.org/pdf/2021_63.pdf

## 📋 Deskripsi Model

Model yang di bangun adalah Agent-Based Model (ABM) yang bersifat heterogen. Artinya, setiap agen merepresentasikan satu individu unik dengan atribut/kepribadian yang tetap (fixed traits), terlepas dari apa status mereka saat ini

### Status Agen (States) 
Setiap agen dapat berada dalam salah satu status berikut:
1.  **SUSCEPTIBLE (Rentan):** Belum terpapar atau netral.
2.  **BELIEVE (Percaya):** Percaya berita palsu dan aktif menyebarkannya ("Infected").
3.  **DENY (Menolak):** Mengetahui kebenaran dan aktif melawan berita palsu ("Vaccinated").
4.  **CURED (Sembuh):** Mantan BELIEVE yang telah disadarkan, kini berhenti menyebar berita.

### Atribut Kepribadian (Personality Traits)
Setiap agen memiliki atribut probabilitas yang unik (ditetapkan di awal via CSV) yang menentukan perilaku mereka:
  
* **`prob_share`** *(dulunya `p_inf_personal`)*: Tingkat agresivitas agen dalam **membagikan** informasi yang ia percaya.(digunakan oleh agent BELIEVE untuk mengubah agent SUSPECTIBLE menjadi BELIEVE)

* **`prob_skeptic`** *(dulunya `p_deny_resist_personal`)*: Tingkat kemampuan kritis agen untuk **menolak** berita palsu saat dipaparkan (digunakan oleh agent SUSPECTIBLE untuk menolak berita dari BELIEVE). jika agent BELIEVE gagal memengaruhi agent SUSPECTIBLE, maka agent SUSPECTIBLE akan menjadi agent DENY.

* **`prob_educate`** *(dulunya `p_vace_personal`)*: Tingkat kepedulian agen untuk **mengedukasi**  orang lain yang masih rentan.(digunakan oleh agent DENY untuk mengubah agent SUSPECTIBLE menjadi agent DENY)

* **`prob_convince`** *(dulunya `p_deny_cure_personal`)*: Tingkat kemampuan persuasi agen untuk **menyadarkan** (menyembuhkan) orang yang sudah terlanjur percaya.(digunakan oleh agent DENY untuk mengubah agent BELIEVE menjadi CURED)

* **`is_influential`**: Penanda apakah agen adalah *Influencer*. [cite_start]Jika ya, semua probabilitas [prob_share, prob_educate, prob_convince] mendapat bonus kekuatan.

---

## 📂 Struktur File
* **`agent.py`**: Mendefinisikan class `PenggunaMediaSosial`. Berisi logika perilaku agen (`spread_fake_news`, `against_fake_news`).
* **`model.py`**: Mendefinisikan class `FakeNewsModel`. Mengatur lingkungan jaringan, memuat data dari CSV, dan penjadwalan.
* **`app.py`**: Script utama untuk menjalankan simulasi, mengumpulkan data, dan memvisualisasikan hasil (grafik).
* **`generate.py`**: Script utilitas untuk membuat data populasi (`data_pengguna.csv`) dan topologi jaringan (`hubungan.csv`) secara otomatis.

# Persiapan Menjalankan Model

## Membuat Python Virtual Environmet bernama venv-abm ## (opsional)
python -m venv venv-abm

## Mengaktifkan venv-abm ##
--Mac/Linux--
source venv-abm/bin/activate

--Windows--
venv-abm/Scripts/activate

## Install Library yang dibutuhkan ##
pip install -r requirements.txt

## Untuk menjalankan berbagai scenario 
modifikasi file model.py

### skenario 1: pengaruh influencer tinggi
ubah line 41 untuk data_pengguna_sc1.csv dan 72 untuk hubungan_sc1.csv
jalankan solara run app.py
setel nilai p_infl lebih tinggi

### skenario 2: agent dengah state BELIEVE memiliki relasi/tetangga yang paling banyak saat inisialisasi
ubah line 41 untuk data_pengguna_sc2.csv dan 72 untuk hubungan_sc2.csv

### skenario 3: setiap agent memiliki nilai p_educate rendah (agent deny cenderung tidak peduli untuk mengedukasi Agent rentan)
ubah line 41 untuk data_pengguna_sc2.csv dan 72 untuk hubungan_sc2.csv


## Untuk menjalakankan Model ABM ## 
solara run app.py
