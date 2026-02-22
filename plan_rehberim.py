import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.markdown("#### 📅 Günlük Plan Notlarım")

CALISMA_HAFTALAR = [
    "23.02.2026", "02.03.2026", "09.03.2026", "23.03.2026", "30.03.2026",
    "06.04.2026", "13.04.2026", "20.04.2026", "27.04.2026", "04.05.2026",
    "11.05.2026", "18.05.2026", "25.05.2026", "01.06.2026", "08.06.2026",
    "15.06.2026", "22.06.2026",
]

BEDEN_EGITIMI_SINIFLAR = ["5. Sınıf", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf"]
SPOR_EGITIMI_SINIFLAR  = ["11. Sınıf", "12. Sınıf"]

def aktif_pazartesi():
    bugun = date.today()
    hafta_gunu = bugun.weekday()
    if hafta_gunu >= 5:
        pazartesi = bugun + timedelta(days=(7 - hafta_gunu))
    else:
        pazartesi = bugun - timedelta(days=hafta_gunu)
    return pazartesi.strftime('%d.%m.%Y')

@st.cache_data(ttl=1)
def veri_yukle():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for dosya_adi in ["plan_yeni.xlsx", "plan.xlsx"]:
        dosya_yolu = os.path.join(base_dir, dosya_adi)
        if os.path.exists(dosya_yolu):
            try:
                import openpyxl
                wb = openpyxl.load_workbook(dosya_yolu)
                ws = wb.active
                data = list(ws.values)
                if not data:
                    continue
                cols = data[0]
                df = pd.DataFrame(data[1:], columns=cols)
                df = df.rename(columns={cols[0]: 'Tarih'})
                df['Tarih'] = df['Tarih'].astype(str).str.strip()
                df = df[df['Tarih'].isin(CALISMA_HAFTALAR)]
                return df
            except Exception as e:
                st.error(f"Hata: {e}")
                import traceback
                st.code(traceback.format_exc())
    st.error("'plan_yeni.xlsx' veya 'plan.xlsx' bulunamadi.")
    return None

df = veri_yukle()

if df is not None and not df.empty:

    # 1. Ders Secin
    st.subheader("📖 Ders Seçin:")
    secilen_ders = st.selectbox("Ders:", ["Beden Eğitimi", "Spor Eğitimi"], label_visibility="collapsed")

    # 2. Sinif Secin (derse gore)
    sinif_listesi = BEDEN_EGITIMI_SINIFLAR if secilen_ders == "Beden Eğitimi" else SPOR_EGITIMI_SINIFLAR
    st.subheader("🏫 Sınıf Seçin:")
    secilen_sinif = st.selectbox("Sınıf:", sinif_listesi, label_visibility="collapsed")

    # 3. Hafta Secin
    bu_hafta = aktif_pazartesi()
    default_index = CALISMA_HAFTALAR.index(bu_hafta) if bu_hafta in CALISMA_HAFTALAR else 0
    st.subheader("📆 Hafta Seçin:")
    secilen_tarih = st.selectbox("Hafta:", CALISMA_HAFTALAR, index=default_index, label_visibility="collapsed")
    if secilen_tarih == bu_hafta:
        st.caption("📍 Aktif hafta otomatik seçildi")

    # Excel sutun adini belirle
    if secilen_ders == "Spor Eğitimi":
        sinif_no = secilen_sinif.split(".")[0]
        sutun_adi = f"{sinif_no}. Sınıf Seçmeli"
    else:
        sutun_adi = secilen_sinif

    # 4. Ogrenme Ciktisi
    satir = df[df['Tarih'] == secilen_tarih]
    st.divider()
    st.subheader("📌 Öğrenme Çıktısı:")
    if not satir.empty and sutun_adi in satir.columns:
        deger = str(satir.iloc[0][sutun_adi]).strip()
        if deger and deger.lower() != 'none' and deger != '':
            st.info(deger)
        else:
            st.info("Bu hafta için öğrenme çıktısı girilmemiş.")
    else:
        st.info("Bu hafta için öğrenme çıktısı girilmemiş.")

else:
    st.warning("⚠️ Excel verisi okunamadı veya dosya boş.")
