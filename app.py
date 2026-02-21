import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku
        df = pd.read_excel("plan.xlsx")
        
        # Sütun isimlerini ne olursa olsun 'Tarih' ve 'Not' yap
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # Boş satırları tamamen temizle
        df = df.dropna(subset=['Tarih', 'Not'], how='all')
        
        # Tarih sütununu zorla metne (string) çevir
        # Bu sayede Excel'deki format ne olursa olsun hata vermez
        df['Tarih'] = df['Tarih'].astype(str).str.split(' ').str[0]
        
        return df
    except Exception as e:
        st.error(f"Hata detayı: {e}")
        return None

df = veri_yukle()

if df is not None:
    # Boş olmayan tarihleri listele
    tarih_listesi = [t for t in df['Tarih'].unique() if str(t) != 'nan']
    
    if not tarih_listesi:
        st.warning("Excel'de okunabilir bir tarih bulunamadı. Lütfen A sütununda veri olduğundan emin olun.")
    else:
        secilen_tarih = st.selectbox("Bir gün seçin:", tarih_listesi)

        if secilen_tarih:
            # Seçilen tarihin notunu göster
            not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
            st.divider()
            st.subheader(f"📌 Notunuz:")
            st.info(not_icerigi)
else:
    st.error("Excel dosyası okunamadı.")
