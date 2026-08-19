# Supply Chain Demand Forecasting & Inventory Optimization

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-Forecasting-orange.svg)](https://www.statsmodels.org/)
[![Domain](https://img.shields.io/badge/Domain-Supply%20Chain%20Analytics-green.svg)](#)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20Passing-brightgreen.svg)](#)

Repositori ini menyajikan analisis peramalan permintaan produk (*Demand Forecasting*) dan optimasi persediaan (*Inventory Optimization*) menggunakan pemodelan deret waktu (*Time Series Analysis*) untuk meminimalisir *stockout* dan *excess holding cost*.

---

## Struktur Proyek

```
├── .gitignore          # Konfigurasi pengabaian cache Git
├── data/               # Dataset historis demand mentah & bersih (CSV)
├── images/             # Visualisasi plot komputasi 300 DPI
├── src/                # Modular Python forecaster engine (SupplyChainForecaster)
├── tests/              # Automated unit tests (Pytest: validasi aggregasi bulanan)
├── notebook.ipynb      # Jupyter Notebook: Time series decomposition, forecasting, dan metrik
├── requirements.txt    # Pinned stable dependencies
└── README.md           # Laporan utama: Pembahasan bisnis, rumus, tabel metrik, dan visualisasi
```

---

## Implementasi Modular & Pengujian Otomatis

Modul demand forecaster tersedia di `src/forecaster.py`:

```python
from src.forecaster import SupplyChainForecaster

forecaster = SupplyChainForecaster()
monthly_df = forecaster.aggregate_monthly_demand()
print(monthly_df.head())
```

Jalankan automated test:
```bash
pytest tests/
```

---

## Cara Menjalankan

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

