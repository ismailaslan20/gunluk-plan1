import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i her şeyi metin (string) olarak oku
        df = pd.read_excel("plan.xlsx", dtype=str)
        
        # Sütun isimleri ne olursa olsun, ilk sütunu 'Tarih', ikinciyi 'Not' yap
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # İlk satırda yanlışlıkla 'Tarih' veya 'Not' yazıyorsa o satırı atla
        if df.iloc[0, 0].strip().lower() in ['tarih', 'tarıh', 'date']:
            df = df.iloc[1:]
        
        # Boş olan satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarih formatındaki gereksiz saat kısımlarını temizle
        df['Tarih'] = df['Tarih'].str.replace(' 00:00:00', '', regex=False).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Teknik bir hata oluştu: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    
    # Tüm tarihleri listele
    tarih_listesi = df['Tarih'].unique().tolist()
    
    secilen_tarih = st.selectbox("Tarih Seçiniz:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin notunu getir
        satir = df[df['Tarih'] == secilen_tarih].iloc[0]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Notunuz:")
        st.info(satir['Not'])
else:
    st.error("Excel verisi okunurken bir sorun oluştu. Lütfen GitHub'daki 'plan.xlsx' dosyasının doğru yüklendiğinden emin olun.")
