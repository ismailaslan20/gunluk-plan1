import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.markdown("#### 📅 Günlük Plan Notlarım")

def aktif_pazartesi():
    bugun = date.today()
    hafta_gunu = bugun.weekday()  # 0=Pazartesi, 5=Cumartesi, 6=Pazar
    if hafta_gunu >= 5:  # Hafta sonu ise bir sonraki pazartesi
        pazartesi = bugun + timedelta(days=(7 - hafta_gunu))
    else:  # Hafta içi ise bu haftanın pazartesisi
        pazartesi = bugun - timedelta(days=hafta_gunu)
    return pazartesi.strftime('%d.%m.%Y')

@st.cache_data(ttl=1)
def veri_yukle():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dosya_yolu = os.path.join(base_dir, "plan.xlsx")

    if not os.path.exists(dosya_yolu):
        st.error("❌ 'plan.xlsx' bulunamadı.")
        return None

    try:
        import openpyxl
        wb = openpyxl.load_workbook(dosya_yolu)
        ws = wb.active

        merged_ranges = list(ws.merged_cells.ranges)
        for merged in merged_ranges:
            min_row, min_col, max_row, max_col = merged.min_row, merged.min_col, merged.max_row, merged.max_col
            top_left_value = ws.cell(min_row, min_col).value
            ws.unmerge_cells(str(merged))
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    ws.cell(row, col).value = top_left_value

        data = ws.values
        cols = next(data)
        df = pd.DataFrame(data, columns=cols)

        df.columns = ['Sinif', 'Tarih', 'Not'] + [f"Sutun_{i}" for i in range(3, df.shape[1])]
        df = df.dropna(how='all')
        df = df[df['Tarih'].notna()]
        df = df[df['Sinif'].notna()]

        def tarihe_cevir(t):
            try:
                return pd.to_datetime(t).strftime('%d.%m.%Y')
            except:
                return str(t).split(' ')[0].strip()

        df['Tarih'] = df['Tarih'].apply(tarihe_cevir)
        df['Sinif'] = df['Sinif'].apply(lambda x: str(int(float(str(x)))) if str(x).replace('.','').isdigit() else str(x))
        df = df[df['Tarih'].astype(str).str.lower().str.strip() != 'tarih']
        df['Not'] = df['Not'].fillna('').astype(str)
        df = df.reset_index(drop=True)
        return df

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None


df = veri_yukle()

if df is not None and not df.empty:
    sinif_listesi = sorted(df['Sinif'].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)

    st.subheader("🏫 Sınıf Seçin:")
    secilen_sinif = st.selectbox("Sınıf:", sinif_listesi, label_visibility="collapsed")

    if secilen_sinif:
        sinif_df = df[df['Sinif'] == secilen_sinif]
        tarih_listesi = sinif_df['Tarih'].tolist()

        bu_hafta = aktif_pazartesi()
        if bu_hafta in tarih_listesi:
            default_index = tarih_listesi.index(bu_hafta)
        else:
            default_index = 0

        st.subheader("📆 Hafta Seçin:")
        secilen_tarih = st.selectbox(
            "Hafta:",
            tarih_listesi,
            index=default_index,
            label_visibility="collapsed"
        )

        if secilen_tarih:
            if secilen_tarih == bu_hafta:
                st.caption("📍 Aktif hafta otomatik seçildi")

            eslesme = sinif_df[sinif_df['Tarih'] == secilen_tarih]
            if not eslesme.empty:
                not_icerigi = eslesme.iloc[0]['Not']
                st.divider()
                st.subheader("📌 Notunuz:")
                st.info(not_icerigi)
            else:
                st.warning("Seçilen haftaya ait not bulunamadı.")
else:
    st.warning("⚠️ Excel verisi okunamadı veya dosya boş.")
