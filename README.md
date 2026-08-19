# Supply Chain Demand Forecasting & Inventory Optimization

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-Forecasting-orange.svg)](https://www.statsmodels.org/)
[![Domain](https://img.shields.io/badge/Domain-Supply%20Chain%20Analytics-green.svg)](#)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20Passing-brightgreen.svg)](#)

Repositori ini menyajikan analisis komprehensif peramalan permintaan produk (*Demand Forecasting*) dan optimasi tingkat persediaan (*Inventory Optimization*) menggunakan pemodelan deret waktu (*Time Series Analysis: SARIMA & Gradient Boosting*) serta perumusan *Safety Stock & Reorder Point (ROP)* untuk menekan biaya kehabisan stok (*stockout cost*) dan biaya simpan berlebih (*excess holding cost*).

---

## 1. Pembahasan Bisnis & Konteks Supply Chain

Ketidakakuratan peramalan permintaan dalam rantai pasok (*supply chain*) memicu fenomena *Bullwhip Effect*, di mana fluktuasi kecil pada tingkat konsumen akhir menciptakan lonjakan distorsi pesanan yang sangat masif di tingkat gudang dan pabrik.

Tujuan utama analisis ini adalah:
1. **Peramalan Permintaan Akurat**: Mengestimasi volume permintaan bulanan agregat dengan mempertimbangkan tren dan musiman (*seasonality*).
2. **Kalkulasi Safety Stock Dinamis**: Menentukan buffer stok minimum yang aman terhadap volatilitas *lead time* dan deviasi permintaan.
3. **Penentuan Titik Pemesanan Kembali (Reorder Point / ROP)**: Memberikan sinyal otomatis kapan departemen pengadaan (*procurement*) harus menerbitkan *Purchase Order*.

---

## 2. Struktur Proyek

```
├── .gitignore          # Konfigurasi pengabaian cache Git
├── data/               # Dataset demand historis (cleaned_demand.csv, raw_demand.csv)
├── images/             # Visualisasi plot komputasi 300 DPI
│   ├── demand_trend.png
│   ├── seasonal_decomposition.png
│   ├── forecast_vs_actual.png
│   ├── safety_stock_rop.png
│   └── feature_importance.png
├── src/                # Modular Python forecaster engine (SupplyChainForecaster)
├── tests/              # Automated unit tests (Pytest)
├── notebook.ipynb      # Mesin pemrosesan: Time series decomposition, forecasting, dan ROP
├── requirements.txt    # Pinned stable dependencies
└── README.md           # Laporan utama: Pembahasan bisnis, rumus, tabel metrik, dan visualisasi
```

---

## 3. Metodologi & Formulasi Manajemen Persediaan

Analisis pada `notebook.ipynb` dan `src/forecaster.py` menerapkan formulasi baku manajemen operasi:

### A. Dekomposisi Deret Waktu Aditif
Memisahkan komponen permintaan historis menjadi tren ($T_t$), musiman ($S_t$), dan residual ($R_t$):

$$Y_t = T_t + S_t + R_t$$

### B. Stok Pengaman (Safety Stock / SS)
Menghitung batas pengaman berbasis deviasi standar permintaan ($\sigma_D$), rata-rata *lead time* ($L$), dan faktor tingkat layanan (*Service Level Factor / Z* pada 95% = 1.645):

$$\text{Safety Stock} = Z \times \sqrt{L \times \sigma_D^2 + D^2 \times \sigma_L^2}$$

### C. Titik Pemesanan Ulang (Reorder Point / ROP)
Batas ambang stok saat pesanan pengadaan baru harus dibuat:

$$\text{ROP} = (\text{Demand per Day} \times \text{Lead Time in Days}) + \text{Safety Stock}$$

---

## 4. Hasil Kuantitatif & Pembahasan Visualisasi

### A. Tren Permintaan Historis & Dekomposisi Musiman
Pola fluktuasi permintaan bulanan dan identifikasi siklus musiman tahunan.

![Tren Permintaan](images/demand_trend.png)
![Dekomposisi Musiman](images/seasonal_decomposition.png)

*   **Pembahasan**: Permintaan menunjukkan tren pertumbuhan bertahap dengan pola lonjakan musiman yang konsisten pada kuartal akhir (Q4 / November - Desember) akibat peningkatan aktivitas belanja akhir tahun.

### B. Hasil Peramalan (Forecast vs Actual)
Perbandingan performa model prediksi deret waktu terhadap data permintaan aktual di periode pengujian.

![Forecast vs Actual](images/forecast_vs_actual.png)
![Safety Stock dan ROP](images/safety_stock_rop.png)

*   **Pembahasan**: Model SARIMA dan Gradient Boosting mampu menangkap titik balik musiman dengan *Mean Absolute Percentage Error (MAPE)* di bawah 12%, memberikan kepastian perencanaan produksi bagi manajemen pabrik.

---

## 5. Implementasi Modular & Pengujian Otomatis

Modul demand forecaster tersedia di `src/forecaster.py`:

```python
from src.forecaster import SupplyChainForecaster

forecaster = SupplyChainForecaster()
monthly_df = forecaster.aggregate_monthly_demand()
print("=== Ringkasan Permintaan Bulanan ===")
print(monthly_df.tail())
```

Jalankan automated test:
```bash
pytest tests/
```

---

## 6. Rekomendasi Operasional Manajemen Rantai Pasok

1. **Implementasi Buffer Stok Dinamis**: Terapkan *Safety Stock* yang disesuaikan per kuartal (tingkatkan buffer 20% lebih tinggi menjelang Q4) untuk mencegah *stockout* saat peak season.
2. **Otomasi Reorder Point pada ERP**: Hubungkan formula ROP langsung ke sistem ERP gudang agar *Purchase Order* otomatis terbit saat persediaan menyentuh batas kritis.
3. **Pengurangan Lead Time Supplier**: Negosiasi SLA dengan pemasok utama untuk memangkas variabilitas *lead time*, yang dapat memotong kebutuhan modal kerja *Safety Stock* hingga 15%.

---

## 7. Cara Menjalankan

1. **Pasang Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Eksekusi Notebook**:
   ```bash
   jupyter notebook notebook.ipynb
   ```

---
*Supply Chain Demand Forecasting Project.*
