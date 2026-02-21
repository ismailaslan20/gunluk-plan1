import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'i oku
        df = pd.read_excel("plan.xlsx")
        
        # İlk iki sütunu al ve isimlerini sabitle
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Kritik Hamle: Önce her şeyi metne çevir, sonra temizle (Hatanın çözümü burada)
        df['Tarih'] = df['Tarih'].astype(str).apply(lambda x: x.strip() if x != 'nan' else '')
        df['Not'] = df['Not'].astype(str).apply(lambda x: x.strip() if x != 'nan' else '')
        
        # Boş tarihli satırları temizle
        df = df[df['Tarih'] != '']
        
        # Excel'in eklediği gereksiz saat kısımlarını (00:00:00) temizle
        df['Tarih'] = df['Tarih'].str.replace(' 00:00:00', '', regex=False)
        
        return df
    except Exception as e:
        st.error(f"Veri yüklenirken bir sorun oldu: {e}")
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bilgi notunu görmek istediğiniz günü seçin:")
    
    tarih_listesi = df['Tarih'].unique().tolist()
    secilen_tarih = st.selectbox("Tarih Seçiniz:", tarih_listesi)

    if secilen_tarih:
        # Seçilen tarihin notunu güvenle getir
        not_icerigi = df[df['Tarih'] == secilen_tarih]['Not'].values[0]
        st.divider()
        st.subheader(f"📌 {secilen_tarih} Tarihli Notunuz:")
        if not_icerigi == "" or not_icerigi == "nan":
            st.warning("Bu tarih için bir not girilmemiş.")
        else:
            st.info(not_icerigi)
else:
    st.info("Henüz görüntülenecek bir veri bulunamadı. Lütfen Excel dosyanızı kontrol edin.")
