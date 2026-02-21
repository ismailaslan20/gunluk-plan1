import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    # Excel dosyasını oku
    df = pd.read_excel("plan.xlsx")
    
    # Sütun isimlerini ne yazarsan yaz otomatik 'Tarih' ve 'Not' olarak kabul et diyoruz
    df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
    
    # Tarihleri düzgünce metne çevir
    df['Tarih'] = pd.to_datetime(df['Tarih'], dayfirst=True).dt.strftime('%d.%m.%Y')
    return df

try:
    df = veri_yukle()
    
    # Seçim kutusu
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    secilen_tarih = st.selectbox("Tarih Listesi:", df['Tarih'].unique())

    if secilen_tarih:
        # Seçilen tarihin yanındaki notu göster
        not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Notunuz:")
        st.info(not_icerigi)

except Exception as e:
    st.warning("Excel dosyası okunurken bir hata oluştu. Lütfen dosyanın ilk sütununda Tarih, ikinci sütununda Not olduğundan emin olun.")
