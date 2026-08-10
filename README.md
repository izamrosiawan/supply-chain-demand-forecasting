# Laporan Analisis Rantai Pasok & Optimasi Inventaris Ritel E-Commerce

Laporan ini menyajikan analisis peramalan permintaan (*demand forecasting*) dan strategi optimasi persediaan (*inventory optimization*) untuk produk `SKU_HIJAB_PREMIUM`. Analisis ini menggunakan data transaksi riil dari UCI Online Retail Dataset (541.909 baris transaksi) yang disaring khusus untuk produk terlaris (`StockCode 85123A`), disesuaikan ke dalam skala operasional regional Indonesia.

---

## 1. Latar Belakang & Masalah Bisnis

### Masalah Bisnis
Industri ritel e-commerce menghadapi tantangan dalam menyeimbangkan tingkat ketersediaan barang dengan efisiensi biaya penyimpanan:
1. **Risiko Kehilangan Penjualan (*Stockout*)**: Gangguan pasokan akibat banjir musiman dan kemacetan ekspedisi menjelang libur nasional memicu kegagalan pemenuhan pesanan konsumen.
2. **Biaya Penyimpanan Gudang (*Holding Cost*)**: Menyimpan persediaan berlebih sebagai stok pengaman membebani arus kas perusahaan karena tingginya biaya sewa gudang regional.

### Tujuan Proyek
Proyek ini bertujuan untuk membangun sistem peramalan permintaan harian pada data transaksi e-commerce serta menentukan parameter logistik optimal (**Safety Stock, Reorder Point, dan Economic Order Quantity**) guna meminimalkan biaya inventaris dengan target tingkat pelayanan (*Service Level*) sebesar **95%**.

---

## 2. Eksplorasi Tren & Pola Musiman

Dengan menyaring transaksi produk terpopuler dari data UCI dan memetakan koordinat logistiknya ke gudang regional (Jakarta, Surabaya, Medan, Makassar), diperoleh pola musiman harian berikut:
- **Musiman Mingguan**: Penjualan melonjak signifikan pada hari Jumat hingga Minggu, mencerminkan aktivitas belanja konsumen di akhir pekan.
- **Musiman Akhir Tahun**: Terjadi lonjakan permintaan yang tinggi pada bulan November–Desember, diikuti dengan fluktuasi harga akibat diskon promosi.

Visualisasi tren permintaan historis dan dekomposisi waktu mingguan:

![Tren Permintaan SKU_HIJAB_PREMIUM](./images/demand_trend.png)

![Dekomposisi Musiman](./images/seasonal_decomposition.png)

---

## 3. Prapemrosesan Data & Imputasi Stockout

Hari di mana terjadi kegagalan rantai pasok (*stockout*) mencatat penjualan aktual sebesar `0` meskipun permintaan pasar riil (*unconstrained demand*) sedang terjadi. Jika data penjualan bernilai nol ini langsung dimasukkan ke model peramalan tanpa pembersihan, model akan mengalami *bias under-forecasting*.

Untuk memulihkan permintaan pasar sesungguhnya, hari-hari terjadinya *stockout* diidentifikasi dan diimputasi menggunakan **rata-rata bergerak 7 hari sebelumnya (*7-day rolling mean*)**. Data bersih ini disimpan dalam [cleaned_demand.csv](file:///c:/Users/LENOVO/Documents/GitHub/supply-chain-demand-forecasting/data/cleaned_demand.csv) sebagai target pelatihan model.

---

## 4. Evaluasi Model Peramalan (*Demand Forecasting*)

Dataset dibagi menjadi dua periode:
- **Training Set**: Tanggal awal s/d 30 September 2025 (~10 bulan).
- **Testing Set (Holdout)**: 1 Oktober 2025 s/d 9 Desember 2025 (70 hari terakhir).

Tiga model diuji pada data holdout:
1. **Seasonal Naive (Baseline)**: Prediksi menggunakan penjualan harian 7 hari sebelumnya ($t-7$).
2. **SARIMAX (1,1,1)x(1,0,0,7)**: Model statistik linier dengan eksogen harga (`Price_IDR`) dan promosi (`Promotion`).
3. **Random Forest Regressor**: Algoritma *machine learning* berbasis lag ($t-1, t-7, t-14, t-30$), rolling mean, dan fitur kalender.

### Metrik Kinerja Evaluasi Model

| Nama Model | MAE (Unit) | RMSE (Unit) | MAPE (%) | WAPE (%) | Keterangan |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Seasonal Naive)** | 98.79 | 222.89 | 184.26% | 93.95% | Error tinggi saat fluktuasi tajam |
| **SARIMAX (Statistik)** | 100.61 | 180.52 | 1484.46% | 95.68% | Kurang adaptif pada data non-linear |
| **Random Forest (ML)** | **79.67** | **161.78** | **528.83%** | **75.77%** | **Performa terbaik dengan error terendah** |

**Evaluasi Metrik WAPE vs MAPE**:
Pada data ritel tingkat harian, hari-hari dengan volume penjualan kecil (misalnya 1–2 unit) dapat menyebabkan nilai persentase kesalahan relatif (MAPE) menggelembung hingga di atas 1000%. Oleh karena itu, **WAPE (Weighted Absolute Percentage Error)** digunakan sebagai metrik evaluasi utama karena menimbang kesalahan prediksi terhadap total volume permintaan aktual. Berdasarkan metrik WAPE, model **Random Forest** menghasilkan akurasi terbaik dengan kesalahan terendah yaitu **75,77%**.

![Perbandingan Peramalan vs Aktual](./images/forecast_vs_actual.png)

### Pentingnya Fitur (*Feature Importance*)
Model Random Forest mengidentifikasi bahwa harga produk (`Price_IDR`) dan rata-rata bergerak 30 hari (`rolling_mean_30`) merupakan dua fitur paling berpengaruh dalam memprediksi permintaan harian.

![Pentingnya Fitur](./images/feature_importance.png)

---

## 5. Optimasi Inventaris & Parameter Logistik

Dengan menggunakan deviasi standar error residual model peramalan terbaik (Random Forest) sebesar $\sigma_e = 162,94\text{ unit}$, parameter kebijakan persediaan gudang ritel dirumuskan sebagai berikut:
- **Service Level Target ($Z$)**: **95%** ($Z = 1,645$)
- **Lead Time Pengiriman ($L$)**: **5 hari** (pemenuhan dari pabrik ke gudang regional)
- **Biaya Pemesanan ($S$)**: **Rp750.000** per pesanan
- **Biaya Penyimpanan ($H$)**: **Rp12.000** per unit/tahun

### Perhitungan Manajemen Persediaan

#### 1. Safety Stock (SS)
Safety Stock disiapkan untuk mengantisipasi keterlambatan logistik dan lonjakan permintaan di atas rata-rata selama Lead Time:
$$SS = Z \times \sigma_e \times \sqrt{L}$$
$$SS = 1,645 \times 162,94 \times \sqrt{5} \approx 599\text{ unit}$$

#### 2. Reorder Point (ROP)
Reorder Point menentukan batas stok gudang yang memicu pemesanan kembali agar barang tiba sebelum stok pengaman terpakai:
$$ROP = (d \times L) + SS$$
Di mana $d$ adalah rata-rata permintaan harian ($105,14\text{ unit}$):
$$ROP = (105,14 \times 5) + 599 \approx 1.125\text{ unit}$$

#### 3. Economic Order Quantity (EOQ)
Economic Order Quantity menentukan kuantitas pemesanan paling efisien untuk meminimalkan gabungan biaya pemesanan dan penyimpanan:
$$EOQ = \sqrt{\frac{2DS}{H}}$$
Di mana $D$ adalah proyeksi permintaan tahunan ($D = d \times 365 = 38.376,1\text{ unit}$):
$$EOQ = \sqrt{\frac{2 \times 38.376,1 \times 750.000}{12.000}} \approx 2.190\text{ unit}$$

### Parameter Logistik Akhir
- Rata-rata Permintaan Harian ($d$): **105 unit**
- Stok Pengaman (*Safety Stock*): **599 unit**
- Titik Pemesanan Ulang (*Reorder Point*): **1.125 unit**
- Jumlah Pemesanan Optimal (*EOQ*): **2.190 unit**

---

## 6. Simulasi Siklus Persediaan Gudang

Grafik siklus persediaan harian (*sawtooth curve*) berikut mensimulasikan level stok fisik gudang selama Semester II tahun 2025. Kebijakan **ROP & EOQ** yang diterapkan berhasil menjaga stok gudang agar berada di atas zona risiko stockout:

![Simulasi Inventaris ROP EOQ](./images/safety_stock_rop.png)

---

## 7. Rekomendasi Strategis

1. **Otomatisasi ERP Berbasis ROP & EOQ**:
   Integrasikan nilai **ROP = 1.125 unit** dan **EOQ = 2.190 unit** ke dalam sistem *Warehouse Management System* (WMS). Ketika stok menyentuh ROP, sistem secara otomatis menerbitkan *Purchase Order* sebesar EOQ.
2. **Mitigasi Lonjakan Cuaca/Musiman**:
   Gudang regional perlu mempertahankan stok pengaman sebesar **599 unit** di awal bulan Januari untuk mengantisipasi hambatan pengiriman darat akibat curah hujan tinggi atau banjir musiman.
3. **Koordinasi Promosi dan Logistik**:
   Tim pemasaran disarankan membagikan jadwal kampanye promosi besar kepada tim operasional logistik minimal 30 hari sebelumnya untuk mengantisipasi lonjakan volume masuk di gudang.
