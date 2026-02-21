import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data(ttl=1) # Hafızayı her saniye tazeler
def veri_yukle():
    try:
        # Excel'i her şeyi metin (str) olarak oku
        df = pd.read_excel("plan.xlsx", dtype=str)
        
        # Sütunları zorla eşle
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # Boş olanları ve başlık satırını temizle
        df = df[df['Tarih'].notna()]
        df = df[df['Tarih'].str.lower() != 'tarih']
        
        # Excel'in arkada eklediği saat (00:00:00) yazılarını temizle
        df['Tarih'] = df['Tarih'].str.split(' ').str[0].str.strip()
        
        return df
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    # İşte burası önemli: Bütün tarihleri olduğu gibi listeye alıyoruz
    tarih_listesi = df['Tarih'].tolist()
    
    st.write(f"Sistemde toplam {len(tarih_listesi)} kayıt bulundu.")
    
    # Listeyi göster
    secilen_tarih = st.selectbox("Lütfen bir tarih seçin:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin tam karşısındaki notu göster
        not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0]['Not']
        st.divider()
        st.subheader(f"📌 Notunuz:")
        st.info(not_icerigi)
else:
    st.error("Excel verisi okunamadı.")
