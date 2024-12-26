# Analisis Data E-Commerce Public

Proyek ini bertujuan untuk menganalisis data e-commerce public menggunakan Python. Aplikasi ini telah di-deploy menggunakan Streamlit untuk mempermudah eksplorasi data secara interaktif.

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama untuk analisis data.
- **Pandas & NumPy**: Untuk manipulasi dan analisis data.
- **Matplotlib & Seaborn**: Untuk membuat visualisasi data.
- **Streamlit**: Untuk membangun aplikasi web interaktif.

## Cara Menjalankan Aplikasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/danendrafau/ecommerce-dataset.git
   ```
2. Masuk ke direktori proyek:
   ```bash
   cd ecommerce-dataset
   ```
3. Install dependencies menggunakan `pip`:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run dashboard.py
   ```

## Struktur Proyek

```
repo-name/
├── dashboard/
│   └── dashboard_main_data.csv                 # Dataset dashboard
│   └── dashboard.py                            # File aplikasi dashboard streamlit
│   └── logo-dan.png                            # Logo dashboard
├── data/...                                    # Dataset raw
├── Proyek_Analisis_Data_ID_Camp_2024.ipynb     # Notebook untuk eksplorasi awal
├── requirements.txt                            # Daftar dependencies
└── README.md                                   # Dokumentasi proyek
```

## Demo

Aplikasi ini telah di-deploy secara online. Anda dapat mencobanya di [Streamlit Cloud](https://ecommerce-public-danendrafau.streamlit.app/).

## Kontribusi

Kontribusi terbuka untuk siapa saja yang ingin meningkatkan proyek ini. Silakan fork repositori ini, buat branch baru, dan kirimkan pull request.
