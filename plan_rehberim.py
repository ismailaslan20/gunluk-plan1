import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Plan Rehberim", layout="centered")
st.title("📅 Günlük Plan Notlarım")

# Dosya yolunu göster
base_dir = os.path.dirname(os.path.abspath(__file__))
dosya_yolu = os.path.join(base_dir, "plan.xlsx")

st.write("📂 Aranan yol:", dosya_yolu)
st.write("📁 Klasördeki dosyalar:", os.listdir(base_dir))

if os.path.exists(dosya_yolu):
    st.success("✅ Dosya bulundu!")
    try:
        df = pd.read_excel(dosya_yolu)
        st.write("📊 Ham veri:", df)
    except Exception as e:
        st.error(f"Okuma hatası: {e}")
else:
    st.error("❌ Dosya bulunamadı!")
