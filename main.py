import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import joblib 

# 1. Muat Model yang Sudah Dilatih
model = joblib.load('model/camera_price_model.pkl')

st.title('Prediksi Harga Kamera')

mapping_brand = {'Agfa': 0, 'Canon': 1, 'Casio': 2, 'Contax': 3, 'Epson': 4, 'Fujifilm': 5,
                  'HP': 6,'JVC': 7, 'Kodak': 8, 'Kyocera': 9, 'Leica': 10, 'Nikon': 11, 'Olympus': 12,
                  'Panasonic': 13, 'Pentax': 14, 'Ricoh': 15, 'Samsung': 16, 'Sanyo': 17, 'Sigma': 18,
                  'Sony': 19, 'Toshiba': 20}
mapping_tahun = {'1997': 0, '1998': 1, '2000': 2, '1999': 3, '2001': 4, '1996': 5, '2002': 6, '2003': 7,
                 '2004': 8, '2005': 9, '2006': 10, '2007': 11, '1994': 12, '1995': 13}
brand_box,tahun_box = st.columns(2)
brand = brand_box.selectbox("Brand Kamera", list(mapping_brand.keys()))
brand = mapping_brand[brand]
tahun = tahun_box.selectbox("Tahun Rilis Kamera", list(mapping_tahun.keys()))
tahun = mapping_tahun[tahun]
MaxRes, MinRes = st.columns(2)
MaxRes = MaxRes.number_input("Resolusi Maksimum(px)", 0)
MinRes = MinRes.number_input("Resolusi Minimum(px)", 0)
Pixel_efektif = st.number_input("Pixel Efektif(MP)", 0)
Wide_zoom, Tele_zoom = st.columns(2)
Wide_zoom = Wide_zoom.number_input("Wide Zoom(mm)", 0)
Tele_zoom = Tele_zoom.number_input("Tele Zoom(mm)", 0)
Normal_fokus, Makro_fokus = st.columns(2)
Normal_fokus = Normal_fokus.number_input("Jarak Fokus Normal(cm)", 0)
Makro_fokus = Makro_fokus.number_input("Jarak Fokus Makro(cm)", 0)
penyimpanan, berat, dimensi = st.columns(3)
penyimpanan = penyimpanan.number_input("Penyimpanan(MB)", 0)
berat = berat.number_input("Berat(g)", 0)
dimensi = dimensi.number_input("Dimensi panjang(mm)", 0)

parameter_prediksi = pd.DataFrame([{
    'Model': brand,
    'Release date': tahun,
    'Max resolution': MaxRes,
    'Low resolution': MinRes,
    'Effective pixels':Pixel_efektif,
    'Zoom wide (W)': Wide_zoom,
    'Zoom tele (T)': Tele_zoom,
    'Normal focus range': Normal_fokus,
    'Macro focus range': Makro_fokus,
    'Storage included': penyimpanan,
    'Weight (inc. batteries)': berat,
    'Dimensions': dimensi,
}])
if st.button("Prediksi Harga"):
    predicted_price = model.predict(parameter_prediksi)
    predicted_price_rupiah = predicted_price*15000.0
    st.write(f"Harga yang diprediksi: {predicted_price[0]:.2f} dollar")
    st.write(f"Harga yang diprediksi: {predicted_price_rupiah[0]:.2f} rupiah")
