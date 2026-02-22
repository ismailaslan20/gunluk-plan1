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

SINIFLAR = [5, 6, 7, 8, 9, 10, 11, 12]

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
    # Önce plan_yeni.xlsx, yoksa plan.xlsx dene
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
                # Tarih sütunu ilk sütun, sonrası sınıflar
                df = df.rename(columns={cols[0]: 'Tarih'})
                df['Tarih'] = df['Tarih'].astype(str).str.strip()
                df = df[df['Tarih'].isin(CALISMA_HAFTALAR)]
                return df
            except Exception as e:
                st.error(f"❌ Hata: {e}")
                import traceback
                st.code(traceback.format_exc())
    st.error("❌ 'plan_yeni.xlsx' veya 'plan.xlsx' bulunamadı.")
    return None

df = veri_yukle()

if df is not None and not df.empty:
    sinif_secenekleri = [f"{s}. Sınıf" for s in SINIFLAR]

    st.subheader("🏫 Sınıf Seçin:")
    secilen_sinif_label = st.selectbox("Sınıf:", sinif_secenekleri, label_visibility="collapsed")

    bu_hafta = aktif_pazartesi()
    if bu_hafta in CALISMA_HAFTALAR:
        default_index = CALISMA_HAFTALAR.index(bu_hafta)
    else:
        default_index = 0

    st.subheader("📆 Hafta Seçin:")
    secilen_tarih = st.selectbox(
        "Hafta:",
        CALISMA_HAFTALAR,
        index=default_index,
        label_visibility="collapsed"
    )

    if secilen_tarih == bu_hafta:
        st.caption("📍 Aktif hafta otomatik seçildi")

    satir = df[df['Tarih'] == secilen_tarih]
    st.divider()
    st.subheader("📌 Notunuz:")
    if not satir.empty and secilen_sinif_label in satir.columns:
        not_val = str(satir.iloc[0][secilen_sinif_label]).strip()
        if not_val and not_val.lower() != 'none' and not_val != '':
            st.info(not_val)
        else:
            st.info("Bu hafta için henüz not girilmemiş.")
    else:
        st.info("Bu hafta için henüz not girilmemiş.")
else:
    st.warning("⚠️ Excel verisi okunamadı veya dosya boş.")
