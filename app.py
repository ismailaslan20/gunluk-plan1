import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i en ham haliyle oku
        df = pd.read_excel("plan.xlsx", header=None)
        
        # Tamamen boş satırları ve sütunları temizle
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # İlk iki sütunu al, isimleri biz verelim
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Her şeyi metne çevir ve 'nan' (boş) yazanları temizle
        df = df.astype(str)
        df = df[df['Tarih'] != 'nan']
        
        # Eğer ilk satırda 'Tarih' kelimesi kalmışsa onu çıkar
        if "tarih" in df.iloc[0, 0].lower():
            df = df.iloc[1:]
            
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    
    # Tarihleri listele
    tarih_listesi = df['Tarih'].unique().tolist()
    secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin notunu göster
        not_icerigi = df[df['Tarih'] == secilen_tarih]['Not'].values[0]
        st.divider()
        st.subheader(f"📌 Notunuz:")
        st.info(not_icerigi)
else:
    st.error("Excel verisi hala okunamıyor. Lütfen plan.xlsx dosyasının İLK SAYFASINDA veri olduğundan emin olun.")
