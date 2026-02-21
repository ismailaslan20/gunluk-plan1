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
        st.error("❌ 'plan.xlsx' bulunamadı.")
        return None

    try:
        # Birleştirilmiş hücreleri doldurmak için openpyxl kullan
        import openpyxl
        wb = openpyxl.load_workbook(dosya_yolu)
        ws = wb.active

        # Birleştirilmiş hücre aralıklarını önce düz hücrelere dönüştür
        merged_ranges = list(ws.merged_cells.ranges)
        for merged in merged_ranges:
            min_row, min_col, max_row, max_col = merged.min_row, merged.min_col, merged.max_row, merged.max_col
            top_left_value = ws.cell(min_row, min_col).value
            ws.unmerge_cells(str(merged))
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    ws.cell(row, col).value = top_left_value

        # Şimdi pandas ile oku
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
    sinif_listesi = sorted(df['Sinif'].unique().tolist(), key=lambda x: int(x) if x.isdigit() else x)

    st.subheader("🏫 Sınıf Seçin:")
    secilen_sinif = st.selectbox("Sınıf:", sinif_listesi, label_visibility="collapsed")

    if secilen_sinif:
        sinif_df = df[df['Sinif'] == secilen_sinif]
        tarih_listesi = sinif_df['Tarih'].tolist()

        st.subheader("📆 Tarih Seçin:")
        secilen_tarih = st.selectbox("Tarih:", tarih_listesi, label_visibility="collapsed")

        if secilen_tarih:
            eslesme = sinif_df[sinif_df['Tarih'] == secilen_tarih]
            if not eslesme.empty:
                not_icerigi = eslesme.iloc[0]['Not']
                st.divider()
                st.subheader("📌 Notunuz:")
                st.info(not_icerigi)
            else:
                st.warning("Seçilen tarihe ait not bulunamadı.")
else:
    st.warning("⚠️ Excel verisi okunamadı veya dosya boş.")
