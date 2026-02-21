import streamlit as st
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Yıllık Planım", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku (plan.xlsx dosyasını arar)
        df = pd.read_excel("plan.xlsx")
        
        # İlk iki sütunu al ve isimlerini sabitle
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Boş olan satırları temizle
        df = df.dropna(subset=['Tarih'])
        
        # Tarih formatını Excel'den geldiği gibi koru veya güzelleştir
        df['Tarih_Gosterim'] = pd.to_datetime(df['Tarih'], dayfirst=True, errors='coerce').dt.strftime('%d.%m.%Y')
        
        # Eğer tarih dönüşümü başarısız olursa orijinal metni kullan
        df['Tarih_Gosterim'] = df['Tarih_Gosterim'].fillna(df['Tarih'].astype(str))
        
        return df
    except Exception as e:
        st.error(f"Dosya okuma hatası: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Notunu görmek istediğiniz günü seçin:")
    
    # Excel'deki TÜM tarihleri listeye koy
    secenekler = df['Tarih_Gosterim'].unique().tolist()
    
    secilen_tarih = st.selectbox("Tarih Listesi:", secenekler)

    if secilen_tarih:
        # Seçilen tarihin satırını bul ve Not sütununu getir
        not_metni = df[df['Tarih_Gosterim'] == secilen_tarih]['Not'].values[0]
        
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Bilgi:")
        st.info(not_metni)
else:
    st.warning("Excel dosyasında veri bulunamadı.")
