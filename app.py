import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")

st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    # Excel dosyanın adı tam olarak plan.xlsx olmalı
    df = pd.read_excel("plan.xlsx")
    # Tarih sütununu GG.AA.YYYY formatına çevirelim
    df['Tarih'] = pd.to_datetime(df['Tarih']).dt.strftime('%d.%m.%Y')
    return df

try:
    df = veri_yukle()
    
    st.write("Bakmak istediğiniz günü seçin:")
    secilen_tarih = st.selectbox("Tarih Seçiniz:", df['Tarih'].unique())

    if secilen_tarih:
        # Seçilen tarihin satırındaki 'Not' sütununu gösterir
        not_metni = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
        
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Bilgi:")
        st.info(not_metni)

except Exception as e:
    st.warning("Lütfen 'plan.xlsx' dosyasını yüklemeyi unutmayın.")
