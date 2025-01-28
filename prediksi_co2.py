import pickle
import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO

st.set_page_config(
    page_title="Forecasting CO2",
    page_icon=":cloud:",
    layout="wide"
)

def apply_custom_styles():
    st.markdown("""
        <style>
            .header {
                color: white;
                text-align: center;
                margin-bottom: 20px;
            }
            .stButton>button {
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            [data-testid="stAppViewContainer"] {
                background-image: url("https://blog.1a23.com/wp-content/uploads/sites/2/2020/02/pattern-5.svg"),
                    linear-gradient(#4d4d4d, transparent),
                    linear-gradient(to top left, #333333, transparent),
                    linear-gradient(to top right, #4d4d4d, transparent);
                background-size: contain;
                width: 100%;
                height: 100vh;
                position: fixed;
                background-position: left;
                background-repeat: repeat-x;
                background-blend-mode: darken;
                will-change: transform;
            }
            #MainMenu, [data-testid="stStatusWidget"], [data-testid="stToolbar"], [data-testid="stHeader"] {
                visibility: hidden;
            }
        </style>
""", unsafe_allow_html=True)

apply_custom_styles()

st.markdown(
    """
    <div style="text-align: right; margin-bottom: 25px;">
        <a href="https://github.com/kvnprdtyaa/forecasting_co2">
            <img src="https://badgen.net/badge/icon/GitHub?icon=github&label" alt="GitHub Badge">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class='header'>
    <h1>Forecasting Kualitas Udara</h1>
    <p>Gunakan aplikasi ini untuk memprediksi emisi CO2 di masa depan.</p> 
</div>
""", unsafe_allow_html=True)

model = pickle.load(open('prediksi_co2.sav','rb'))
df = pd.read_excel("CO2 dataset.xlsx")
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index(['Year'], inplace=True)

tab1, tab2 = st.tabs(["Prediksi", "Dataset"])

with tab1:
    year = st.slider("Tentukan Jumlah Tahun Prediksi", 1, 30, step=1)

    if st.button("Predict"):
        try:
            forecast = model.forecast(year)
            pred = pd.DataFrame(forecast, columns=['CO2'])
            pred.index = pd.date_range(start=df.index[-1], periods=len(pred), freq='Y')
            pred.index.name = 'Year'
            pred['Type'] = 'Prediksi'

            historical = df.copy()
            historical['Type'] = 'Data Aktual'
            combined = pd.concat([historical, pred])

            st.subheader("Hasil Prediksi")
            st.dataframe(pred.reset_index(), use_container_width=True)

            chart = alt.Chart(combined.reset_index()).mark_line().encode(
                x=alt.X('Year:T', title='Tahun'),
                y=alt.Y('CO2:Q', title='Konsentrasi CO2'),
                color=alt.Color('Type:N', title='Keterangan', scale=alt.Scale(scheme='category10')),
                tooltip=['Year:T', 'CO2:Q', 'Type:N']
            ).properties(
                title="Prediksi Emisi CO2",
                width='container',
                height=450
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

            def to_excel(dataframe):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    dataframe.to_excel(writer, index=True, sheet_name='Prediksi')
                return output.getvalue()

            excel_data = to_excel(pred)

            st.download_button(
                label="Download Prediksi",
                data=excel_data,
                file_name='hasil_prediksi_co2.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")
    else:
        st.info("Klik tombol 'Prediksi' untuk memulai.")

with tab2:
    st.subheader("Informasi Dataset")
    st.write("""
    Dataset ini digunakan untuk memprediksi emisi CO2 di masa depan. Anda dapat mengunjungi 
    [Kaggle](https://www.kaggle.com/datasets/rohitshirudkar/air-quality-forecasting-co2-emissions) 
    untuk melihat dataset lebih detail.
    """)
    st.write("Pratinjau Data:")
    st.dataframe(df.reset_index().head(), use_container_width=True)
