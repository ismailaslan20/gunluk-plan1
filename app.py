import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku (Hangi sütun neyse ona bakmaksızın)
        df = pd.read_excel("plan.xlsx", dtype=str) # Her şeyi metin olarak oku ki hata çıkmasın
        
        # İlk iki sütunu al
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Boş satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarih formatını temizle (Excel'in eklediği saatleri vs. siler)
        df['Tarih'] = df['Tarih'].str.replace(' 00:00:00', '', regex=False).str.strip()
        
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    
    # Tüm tarihleri listele
    tarih_listesi = df['Tarih'].unique().tolist()
    
    secilen_tarih = st.selectbox("Tarih Seçiniz:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin notunu getir
        not_icerigi = df[df['Tarih'] == secilen_tarih]['Not'].values[0]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Notunuz:")
        st.info(not_icerigi)
else:
    st.error("Excel verisi hala okunamıyor. Lütfen GitHub'da 'plan.xlsx' dosyasının içeriğinden emin olun.")
