import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku (Başlıkları otomatik tanımaya çalışma, direkt ilk satırı veri al)
        df = pd.read_excel("plan.xlsx", header=None)
        
        # Eğer ilk satırda 'Tarih' veya 'TARİH' yazıyorsa o satırı atla
        if str(df.iloc[0, 0]).strip().lower() in ['tarih', 'tarıh']:
            df = df.iloc[1:]
            
        # İlk sütunu Tarih, ikinciyi Not yap
        df.columns = ['Tarih', 'Not'] + list(range(2, len(df.columns)))
        
        # Boş satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Her şeyi düz metne çevir ki format hatası vermesin
        df['Tarih'] = df['Tarih'].astype(str).str.strip().str.replace('.0', '', regex=False)
        df['Not'] = df['Not'].astype(str).str.strip()
        
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None and not df.empty:
    tarih_listesi = df['Tarih'].tolist()
    
    st.write("Bakmak istediğiniz günü seçin:")
    secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin yanındaki notu çek
        not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
        st.divider()
        st.subheader(f"📌 Notunuz:")
        if not_icerigi == "nan":
            st.warning("Bu tarih için bir not girilmemiş.")
        else:
            st.info(not_icerigi)
else:
    st.error("Excel dosyasında veri bulunamadı. Lütfen plan.xlsx dosyasının ilk sayfasında verileriniz olduğundan emin olun.")
