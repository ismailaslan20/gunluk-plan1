import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i her şeyi metin (string) olarak oku ki tarih formatı bozulmasın
        df = pd.read_excel("plan.xlsx", dtype=str)
        
        # Sütun isimlerini sabitle
        df.columns = ['Tarih', 'Not'] + list(df.columns[2:])
        
        # Başlık satırı tekrar ediyorsa onu çıkar
        df = df[~df['Tarih'].str.contains("Tarih", case=False, na=False)]
        
        # Boş satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarih formatındaki gereksiz '.0' veya saat kısımlarını temizle
        df['Tarih'] = df['Tarih'].str.replace(' 00:00:00', '', regex=False).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Hata: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    
    # Excel'deki TÜM benzersiz tarihleri listeye al
    tarih_listesi = df['Tarih'].unique().tolist()
    
    # Listede kaç tarih olduğunu kontrol için alta küçük bir not yazalım
    st.caption(f"Toplam {len(tarih_listesi)} farklı tarih bulundu.")
    
    secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin karşısındaki NOTU getir
        not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Not:")
        st.info(not_icerigi)
else:
    st.error("Excel dosyasında veri bulunamadı.")
