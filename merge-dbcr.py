import streamlit as st
import pandas as pd
import numpy as np
import io

st.title('Aplikasi Penggabungan Simpanan dan Pinjaman')
st.write("""Gabungkan file simpanan dan pinjaman (yang sudah digabungkan dan pinjaman N/A""")

uploaded_files = st.file_uploader("Unggah file Excel", accept_multiple_files=True, type=["xlsx"])

if uploaded_files:
    dfs = {}
    for file in uploaded_files:
        df = pd.read_excel(file, engine='openpyxl')  # Baca file Excel dengan pandas
        dfs[file.name] = df



    # Konversi data menjadi DataFrame
    if 'pivot_simpanan.xlsx' in dfs:
        df_s = dfs['pivot_simpanan.xlsx']
    if 'pivot_pinjaman.xlsx' in dfs:
        df_p = dfs['pivot_pinjaman.xlsx']

    dfs_merged = pd.merge(df_s, df_p[['DUMMY', 'Db PTN', 'Cr PTN', 'Db PRT', 'Cr PRT', 'Db DTP', 'Cr DTP', 'Db PMB', 'Cr PMB', 'Db PRR', 'Cr PRR',
            'Db PSA', 'Cr PSA', 'Db PU', 'Cr PU', 'Db Total2', 'Cr Total2']], on='DUMMY', how='left')
    dfs_merged = dfs_merged.fillna(0)

    st.write("THC Final setelah di proses:")
    st.write(dfs_merged)

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
