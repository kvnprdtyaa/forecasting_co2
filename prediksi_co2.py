import pickle
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
        page_title="Forecasting CO2",
        page_icon=":cloud:",
        layout="wide"
)

custom_css = """
<style>
    .header {
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .header a {
        color: #1E90FF;
        text-decoration: none;
    }
    .header a:hover {
        text-decoration: underline;
    }
    .stButton>button {
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

model = pickle.load(open('prediksi_co2.sav','rb'))
df = pd.read_excel("CO2 dataset.xlsx")
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index(['Year'], inplace=True)

st.markdown("""
<div class='header'>
    <h1>Forecasting Kualitas Udara</h1>
    <p>Gunakan aplikasi ini untuk memprediksi emisi CO2 di masa depan.</p> 
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Pengaturan")
    year = st.slider("Tentukan Jumlah Tahun Prediksi", 1, 30, step=1)

tab1, tab2 = st.tabs(["Prediksi", "Informasi Dataset"])

with tab1:
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
