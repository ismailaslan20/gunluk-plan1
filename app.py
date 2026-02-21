import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i en saf haliyle, her şeyi düz metin olarak açıyoruz
        df = pd.read_excel("plan.xlsx", dtype=str)
        
        # Sütun isimlerini zorla 1. Tarih, 2. Not yapıyoruz
        df.columns = [str(c) for c in df.columns]
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # Başlık satırı aşağıda tekrar ediyorsa (Tarih yazan satırlar) onları siliyoruz
        df = df[df['Tarih'].str.lower() != 'tarih']
        
        # Sadece dolu olan satırları alıyoruz
        df = df[df['Tarih'].notna() & (df['Tarih'] != 'nan')]
        
        # Excel'in arkada eklediği saat (00:00:00) yazılarını temizliyoruz
        df['Tarih'] = df['Tarih'].str.split(' ').str[0].str.strip()
        
        return df
    except Exception as e:
        st.error(f"Teknik bir sorun oluştu: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    # İşte kritik nokta: Listeyi zorla oluşturuyoruz
    tarih_listesi = df['Tarih'].tolist()
    
    st.write(f"Sistemde {len(tarih_listesi)} adet tarih bulundu. Lütfen birini seçin:")
    
    secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin tam olarak karşısındaki notu buluyoruz
        not_filtresi = df[df['Tarih'] == secilen_tarih]
        if not not_filtresi.empty:
            not_icerigi = not_filtresi.iloc[0]['Not']
            st.divider()
            st.subheader(f"📌 {secilen_tarih} Tarihli Not:")
            st.info(not_icerigi)
else:
    st.warning("Excel dosyasının içi boş veya düzgün okunmadı.")
