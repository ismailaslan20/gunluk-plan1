import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku
        df = pd.read_excel("plan.xlsx")
        
        # Sütun isimleri ne olursa olsun onları 'Tarih' ve 'Not' olarak adlandırıyoruz
        # Bu sayede 'tarih', 'TARİH' veya 'Tarih' yazman fark etmez.
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # Boş satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarihleri her ihtimale karşı temiz bir formata sokalım
        df['Tarih'] = pd.to_datetime(df['Tarih'], errors='coerce').dt.strftime('%d.%m.%Y')
        
        # Dönüştürülemeyen (boş kalan) tarihleri de temizle
        df = df.dropna(subset=['Tarih'])
        
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    tarih_listesi = df['Tarih'].unique()
    
    secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin yanındaki notu bul
        not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Not:")
        st.info(not_icerigi)
else:
    st.error("Excel dosyası okunamadı. Lütfen GitHub'da 'plan.xlsx' adında bir dosya olduğundan emin olun.")
