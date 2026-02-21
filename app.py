import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hatasız Planlayıcı", layout="centered")
st.title("📅 Günlük Plan Notlarım")

def veri_cek():
    try:
        # Excel'in içindeki TÜM sayfaları listele
        excel = pd.ExcelFile("plan.xlsx")
        # İlk sayfayı al
        df = excel.parse(excel.sheet_names[0], header=None)
        
        # Tamamen boş satır ve sütunları temizle
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Eğer ilk satır başlık (Tarih, Not vb.) ise onu temizle
        if "tarih" in str(df.iloc[0, 0]).lower():
            df = df.iloc[1:]
            
        # İlk iki sütunu al
        df = df.iloc[:, :2]
        df.columns = ['Tarih', 'Not']
        
        # Her şeyi metne çevir
        df['Tarih'] = df['Tarih'].astype(str).str.split(' ').str[0].str.strip()
        df['Not'] = df['Not'].astype(str).str.strip()
        
        # 'nan' (boş) olanları listeden at
        df = df[df['Tarih'] != 'nan']
        
        return df
    except Exception as e:
        return None

df = veri_cek()

if df is not None and not df.empty:
    tarih_listesi = df['Tarih'].unique().tolist()
    
    st.success(f"✅ Excel başarıyla okundu! {len(tarih_listesi)} tarih bulundu.")
    
    secilen = st.selectbox("Bir Tarih Seçin:", tarih_listesi)
    
    if secilen:
        not_metni = df[df['Tarih'] == secilen].iloc[0]['Not']
        st.divider()
        st.subheader(f"📌 {secilen} Notu:")
        st.info(not_metni)
else:
    st.error("⚠️ Excel'in içindeki veriye ulaşılamıyor.")
    st.info("İpucu: Excel'deki verilerinizin en üst sol köşeden (A1 hücresi) başladığından emin olun.")
