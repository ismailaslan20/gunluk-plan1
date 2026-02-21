import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data(ttl=1)
def veri_yukle():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dosya_yolu = os.path.join(base_dir, "plan.xlsx")

    st.write(f"Aranan yol: {dosya_yolu}")  # debug için

    if not os.path.exists(dosya_yolu):
        st.error("❌ 'plan.xlsx' dosyası bulunamadı. Dosyanın bu script ile aynı klasörde olduğundan emin olun.")
        return None

    try:
        df = pd.read_excel(dosya_yolu, dtype=str)

        # Sütun sayısı kontrolü
        if df.shape[1] < 2:
            st.error("❌ Excel dosyasında en az 2 sütun (Tarih, Not) olmalıdır.")
            return None

        # İlk iki sütunu zorla adlandır
        sutunlar = ['Tarih', 'Not'] + [f"Sütun_{i}" for i in range(2, df.shape[1])]
        df.columns = sutunlar

        # Tamamen boş satırları at
        df = df.dropna(how='all')

        # Tarih sütunu boş olanları at
        df = df[df['Tarih'].notna()]
        df = df[df['Tarih'].str.strip() != '']

        # Başlık satırı tekrar geldiyse temizle
        df = df[df['Tarih'].str.lower().str.strip() != 'tarih']

        # Excel'in eklediği saat bilgisini temizle (ör: "2024-01-01 00:00:00")
        df['Tarih'] = df['Tarih'].str.split(' ').str[0].str.strip()

        # Not sütunundaki NaN'leri boş string yap
        df['Not'] = df['Not'].fillna('(Not girilmemiş)')

        df = df.reset_index(drop=True)
        return df

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
        return None


df = veri_yukle()

if df is not None and not df.empty:
    tarih_listesi = df['Tarih'].tolist()

    st.success(f"✅ Sistemde toplam {len(tarih_listesi)} kayıt bulundu.")

    secilen_tarih = st.selectbox("Lütfen bir tarih seçin:", tarih_listesi)

    if secilen_tarih:
        eslesme = df[df['Tarih'] == secilen_tarih]
        if not eslesme.empty:
            not_icerigi = eslesme.iloc[0]['Not']
            st.divider()
            st.subheader("📌 Notunuz:")
            st.info(not_icerigi)
        else:
            st.warning("Seçilen tarihe ait not bulunamadı.")
else:
    st.warning("⚠️ Excel verisi okunamadı veya dosya boş.")
