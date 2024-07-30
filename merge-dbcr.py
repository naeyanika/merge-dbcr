import streamlit as st
import pandas as pd
import numpy as np
import io

st.title('Aplikasi Penggabungan Simpanan dan Pinjaman')
st.write("""1. Format file harus bernama dan menggunakan ekstensi csv di excelnya pilih save as *CSV UTF-8 berbatas koma atau coma delimited*, sehingga seperti ini : THC.csv, DbPinjaman.csv, DbSimpanan.csv""")

uploaded_files = st.file_uploader("Unggah file Excel", accept_multiple_files=True, type=["xlsx"])

if uploaded_files:
    dfs = {}
    for file in uploaded_files:
        df = pd.read_excel(file, engine='openpyxl')  # Baca file Excel dengan pandas
        dfs[file.name] = df



# Konversi data menjadi DataFrame
df_s = pd.DataFrame(pivot_simpanan)
df_p = pd.DataFrame(pivot_pinjaman)

dfs_merged = pd.merge(df_s, df_p[['DUMMY', 'Db PTN', 'Cr PTN', 'Db PRT', 'Cr PRT', 'Db DTP', 'Cr DTP', 'Db PMB', 'Cr PMB', 'Db PRR', 'Cr PRR',
            'Db PSA', 'Cr PSA', 'Db PU', 'Cr PU', 'Db Total2', 'Cr Total2']], on='DUMMY', how='left')
dfs_merged = dfs_merged.fillna(0)

dfs_merged['CENTER'] = dfs_merged['CENTER'].astype(str).str.zfill(3)
dfs_merged['KELOMPOK'] = dfs_merged['KELOMPOK'].astype(str).str.zfill(2)

# Download links for pivot tables
    for name, df in {
        'THC FINAL.xlsx': dfs_merged
    }.items():
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        buffer.seek(0)
        st.download_button(
            label=f"Unduh {name}",
            data=buffer.getvalue(),
            file_name=name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )