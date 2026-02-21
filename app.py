import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku
        df = pd.read_excel("plan.xlsx")
        
        # Sütunları zorla isimle çağır (1. Sütun Tarih, 2. Sütun Not)
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # Boş satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarih sütununda ne varsa (sayı, metin, tarih) hepsini düz yazıya çevir
        df['Tarih'] = df['Tarih'].astype(str).str.replace('.0', '', regex=False)
        
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None:
    # Tarihleri listeye al
    tarih_listesi = df['Tarih'].tolist()
    
    if not tarih_listesi:
        st.warning("Excel dosyasının içi boş görünüyor. Lütfen A sütununa tarihleri ekleyin.")
    else:
        st.write("Bilgi notunu görmek istediğiniz günü seçin:")
        secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

        if secilen_tarih:
            # Seçilen tarihin karşısındaki notu göster
            not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
            st.divider()
            st.subheader(f"📌 Notunuz:")
            st.info(not_icerigi)
else:
    st.error("Excel dosyası bulunamadı. Lütfen GitHub'da dosya adının 'plan.xlsx' olduğundan emin olun.")
