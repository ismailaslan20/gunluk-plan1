import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Rehberi", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data
def veri_yukle():
    try:
        # Excel'in içindeki TÜM sayfaları kontrol et ve ilk dolu olanı al
        excel_file = pd.ExcelFile("plan.xlsx")
        df = excel_file.parse(excel_file.sheet_names[0], header=None)
        
        # Tamamen boş satırları ve sütunları temizle
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Eğer ilk satır başlık (Tarih, Not vb.) ise onu atla
        first_cell = str(df.iloc[0, 0]).lower()
        if "tarih" in first_cell or "tarıh" in first_cell or "date" in first_cell:
            df = df.iloc[1:]

        # İlk iki sütunu al (Tarih ve Not)
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Tarih sütununu metne çevir ve temizle
        df['Tarih'] = df['Tarih'].astype(str).str.strip().str.replace('.0', '', regex=False)
        df['Not'] = df['Not'].astype(str).str.strip()
        
        return df
    except Exception as e:
        return None

df = veri_yukle()

if df is not None and not df.empty:
    st.write("Bakmak istediğiniz günü seçin:")
    
    # Tarihleri listeye al (Boş olmayanları)
    tarih_listesi = [t for t in df['Tarih'].tolist() if t != 'nan']
    
    if tarih_listesi:
        secilen_tarih = st.selectbox("Tarih Listesi:", tarih_listesi)

        if secilen_tarih:
            # Seçilen tarihin yanındaki notu göster
            not_icerigi = df[df['Tarih'] == secilen_tarih].iloc[0, 1]
            st.divider()
            st.subheader(f"📌 Notunuz:")
            if not_icerigi == "nan" or not_icerigi == "":
                st.warning("Bu tarih için bir not girilmemiş.")
            else:
                st.info(not_icerigi)
    else:
        st.warning("Excel'de tarih sütunu boş görünüyor.")
else:
    st.error("Excel dosyası okunamadı veya içi tamamen boş. Lütfen 'plan.xlsx' dosyasını ve içeriğini kontrol edin.")
