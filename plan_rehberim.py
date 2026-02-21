import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

@st.cache_data(ttl=1)
def veri_yukle():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dosya_yolu = os.path.join(base_dir, "plan.xlsx")

    if not os.path.exists(dosya_yolu):
        st.error(f"❌ 'plan.xlsx' bulunamadı: {dosya_yolu}")
        return None

    try:
        df = pd.read_excel(dosya_yolu)

        if df.shape[1] < 2:
            st.error("❌ Excel dosyasında en az 2 sütun olmalıdır.")
            return None

        sutunlar = ['Tarih', 'Not'] + [f"Sutun_{i}" for i in range(2, df.shape[1])]
        df.columns = sutunlar

        df = df.dropna(how='all')
        df = df[df['Tarih'].notna()]

        # Tarihi stringe çevir
        def tarihe_cevir(t):
            try:
                return pd.to_datetime(t).strftime('%d.%m.%Y')
            except:
                return str(t).split(' ')[0].strip()

        df['Tarih'] = df['Tarih'].apply(tarihe_cevir)

        # Artık string olduğu garantili, filtrele
        df['Tarih'] = df['Tarih'].astype(str)
        df = df[df['Tarih'].str.strip() != '']
        df = df[df['Tarih'].str.strip() != 'nan']
        df = df[df['Tarih'].str.lower().str.strip() != 'tarih']

        df['Not'] = df['Not'].fillna('(Not girilmemiş)').astype(str)
        df = df.reset_index(drop=True)
        return df

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None


df = veri_yukle()

if df is not None and not df.empty:
    tarih_listesi = df['Tarih'].tolist()
    st.success(f"✅ Sistemde toplam {len(tarih_listesi)} kayıt bulundu.")

    secilen_tarih = st.selectbox("Lütfen bir tarih seçin:", tarih_listesi)

    if secilen_tarih:
        eslesme = df[df['Tarih'] == secilen_tarih]
        if not eslesme.empty:
            not_icerigi = eslesme.iloc[0]['Not']
            st.divider()
            st.subheader("📌 Notunuz:")
            st.info(not_icerigi)
        else:
            st.warning("Seçilen tarihe ait not bulunamadı.")
else:
    st.warning("⚠️ Excel verisi okunamadı veya dosya boş.")
