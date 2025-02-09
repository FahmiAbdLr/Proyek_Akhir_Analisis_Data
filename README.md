# Proyek Akhir - Analisis Data E-Commerce

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data transaksi dari platform e-commerce dan menyajikannya dalam bentuk dashboard interaktif menggunakan Streamlit. Analisis yang dilakukan mencakup tren penjualan, distribusi rating pelanggan, serta sebaran pelanggan berdasarkan lokasi.

---

## 📂 Struktur Folder

Berikut adalah struktur folder proyek ini:

```
proyek-akhir/
│── dashboard/
│   ├── dashboard.py   # Kode utama dashboard Streamlit
│── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
│── notebook.ipynb    # Jupyter Notebook untuk eksplorasi awal data
│── requirements.txt   # Daftar dependensi yang dibutuhkan
│── README.md         # Dokumentasi proyek ini
│── url.txt           # Referensi sumber data
```

---

## 📊 Analisis yang Dilakukan

### 1️⃣ Bagaimana Performa Penjualan dan Revenue Perusahaan Dalam Beberapa Bulan Terakhir?

- Menghitung jumlah order per bulan dan revenue bulanan.
- Mengidentifikasi produk yang paling laris.
- **Visualisasi:**
  - Grafik tren jumlah penjualan per bulan.
  - Grafik tren revenue per bulan.
  - Grafik kategori produk dengan penjualan terbanyak.

### 2️⃣ Bagaimana Tingkat Kepuasan Pelanggan Terhadap Produk dan Layanan Dalam Beberapa Bulan Terakhir?

- Melihat distribusi skor rating dari pelanggan.
- Menganalisis rata-rata rating per bulan.
- **Visualisasi:**
  - Grafik distribusi rating pelanggan.
  - Grafik tren rata-rata rating per bulan.

### 3️⃣ Bagaimana demografi pelanggan perusahaan, seperti lokasi state dan lokasi kota?

- Menghitung jumlah pelanggan per state dan kota.
- Menghitung total revenue berdasarkan lokasi pelanggan.
- **Visualisasi:**
  - Grafik jumlah pelanggan per state.
  - Grafik total pendapatan per state.
  - Grafik kota dengan jumlah pelanggan terbanyak.

---

## 🚀 Cara Menjalankan Dashboard

1. **Pastikan Python sudah terinstal** di sistem Anda.
2. **Install dependensi yang diperlukan** dengan menjalankan perintah berikut:
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Streamlit untuk membuka dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
4. **Buka browser** dan akses URL yang ditampilkan oleh Streamlit.

---
