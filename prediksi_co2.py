import pickle
import streamlit as st
import pandas as pd
import altair as alt

model = pickle.load(open('prediksi_co2.sav','rb'))

df = pd.read_excel("CO2 dataset.xlsx")
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index(['Year'], inplace=True)

st.title('Forecasting Kualitas Udara')
st.write("Gunakan aplikasi ini untuk memprediksi emisi CO2 di masa depan.")

year = st.slider("Tentukan Jumlah Tahun untuk Prediksi",1,30, step=1)

if st.button("Predict"):
    try:
        pred = model.forecast(year)
        pred = pd.DataFrame(pred, columns=['CO2'])
        pred.index.name = 'Year'
        pred.reset_index(inplace=True)
        pred.index += 1
        pred.index.name = 'No'

        st.subheader("Hasil Prediksi")
        st.dataframe(pred, use_container_width=True)
        
        historical = df.reset_index()
        historical['Type'] = 'Data Aktual'
        pred['Type'] = 'Prediksi'
        combined = pd.concat([historical, pred], axis=0)

        chart = alt.Chart(combined).mark_line().encode(
            x=alt.X('Year:T', title='Tahun'),
            y=alt.Y('CO2:Q', title='Konsentrasi CO2'),
            color=alt.Color('Type:N', title='Keterangan', scale=alt.Scale(scheme='category10')),
            tooltip=['Year:T', 'CO2:Q', 'Type:N']
        ).properties(
            title="Prediksi Emisi CO2",
            width=700,
            height=400
        ).interactive() 

        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat prediksi: {e}")