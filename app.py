import streamlit as st
import pandas as pd

# Sayfa tasarımı
st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku
        df = pd.read_excel("plan.xlsx")
        
        # İlk iki sütunu al ve isimlerini ne yazarsan yaz kabul et
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Boş olan satırları tamamen temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarih sütununu düz yazıya (metne) çevir (Format hatasını engeller)
        df['Tarih_Gosterim'] = df['Tarih'].astype(str).str.split(' ').str[0]
        
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    
    # Tüm tarihleri benzersiz bir liste olarak al
    tarih_listesi = df['Tarih_Gosterim'].unique().tolist()
    
    secilen_tarih = st.selectbox("Tarih Seçiniz:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin karşısındaki notu göster
        satir = df[df['Tarih_Gosterim'] == secilen_tarih].iloc[0]
        st.divider()
        st.subheader(f"📌 Notunuz:")
        st.info(satir['Not'])
else:
    st.error("Excel dosyası okunamadı veya içi boş. Lütfen 'plan.xlsx' dosyasını kontrol edin.")
