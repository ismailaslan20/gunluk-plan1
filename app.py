import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i en saf haliyle oku (başlıkları biz belirleyeceğiz)
        df = pd.read_excel("plan.xlsx", header=None)
        
        # Tamamen boş satırları temizle
        df = df.dropna(how='all')
        
        # Eğer ilk satırda 'Tarih' veya 'Not' yazıyorsa o satırı atla
        if str(df.iloc[0, 0]).strip().lower() in ['tarih', 'tarıh', 'date']:
            df = df.iloc[1:]
            
        # Sadece ilk iki sütunu al ve isim ver
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Kritik Hamle: Her şeyi zorla metne çevir ve boşlukları sil
        df['Tarih'] = df['Tarih'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df['Not'] = df['Not'].astype(str).str.strip()
        
        # Boş olanları (nan) temizle
        df = df[df['Tarih'] != 'nan']
        
        return df
    except Exception as e:
        st.error(f"Dosya okuma hatası: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Notunu görmek istediğiniz günü seçin:")
    
    # Tarihleri bir listeye al
    tarih_listesi = df['Tarih'].tolist()
    
    secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin notunu göster
        not_icerigi = df[df['Tarih'] == secilen_tarih]['Not'].values[0]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Not:")
        
        if not_icerigi == 'nan' or not_icerigi == '':
            st.warning("Bu tarih için bir not girilmemiş.")
        else:
            st.info(not_icerigi)
else:
    st.warning("Excel dosyasında okunabilir veri bulunamadı. Lütfen plan.xlsx dosyasını kontrol edin.")
