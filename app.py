import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

# ÖNEMLİ: Hafızaya alma (cache) özelliğini kaldırdık ki her seferinde dosyayı sıfırdan okusun
try:
    # Dosyayı her türlü hataya karşı en esnek modda okuyoruz
    df = pd.read_excel("plan.xlsx", dtype=str)
    
    # Sütunları zorla eşleştiriyoruz
    df = df.iloc[:, :2]
    df.columns = ['Tarih', 'Not']
    
    # Boş satırları filtrele
    df = df[df['Tarih'].notna() & (df['Tarih'] != 'nan')]
    
    # Excel'den gelen gereksiz saat bilgilerini temizle
    df['Tarih'] = df['Tarih'].str.split(' ').str[0].str.strip()

    if not df.empty:
        # Tüm tarihleri listeye döküyoruz
        tarih_listesi = df['Tarih'].unique().tolist()
        
        st.success(f"Bağlantı başarılı! {len(tarih_listesi)} adet tarih bulundu.")
        
        secilen_tarih = st.selectbox("Lütfen bir tarih seçin:", tarih_listesi)

        if secilen_tarih:
            not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0]['Not']
            st.divider()
            st.subheader(f"📌 {secilen_tarih} Tarihli Not:")
            st.info(not_icerigi)
    else:
        st.warning("Dosya bulundu ama içindeki 'Tarih' sütunu boş görünüyor.")

except Exception as e:
    st.error("Şu an 'plan.xlsx' dosyasına ulaşılamıyor veya dosya bozuk.")
    st.info("Lütfen GitHub ana sayfasında 'plan.xlsx' dosyasının var olduğundan emin olun.")
