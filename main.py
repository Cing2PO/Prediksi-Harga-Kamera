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

url = 'dataset/camera_dataset.csv'
data = pd.read_csv(url)
data['Model'] = data['Model'].apply(lambda x: x.split()[0])

# Fitur (X) dan Target (y)
X = data[['Model','Release date',	'Max resolution',	'Low resolution',	'Effective pixels',	'Zoom wide (W)',	'Zoom tele (T)',	'Normal focus range',	'Macro focus range',	'Storage included',	'Weight (inc. batteries)',	'Dimensions']]
y = data['Price']

# Encoding kolom kategorikal
label_encoder = LabelEncoder()
X['Model'] = label_encoder.fit_transform(X['Model'])
X['Release date'] = label_encoder.fit_transform(X['Release date'])

# Membagi data menjadi pelatihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

# Model Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

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
Wide_zoom = Wide_zoom.number_input("Wide Focal Length(mm)", 0)
Tele_zoom = Tele_zoom.number_input("Tele Focal Length(mm)", 0)
Normal_fokus, Makro_fokus = st.columns(2)
Normal_fokus = Normal_fokus.number_input("Jarak Fokus Normal(cm)", 0)
Makro_fokus = Makro_fokus.number_input("Jarak Fokus Makro(cm)", 0)
penyimpanan, berat, dimensi = st.columns(3)
penyimpanan = penyimpanan.number_input("Penyimpanan(MB)", 0)
berat = berat.number_input("Berat(g)", 0)
dimensi = dimensi.number_input("Dimensi panjang(mm)", 0)

st.write("brand:", brand)
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
    #predicted_price = predicted_price*15876.0
    st.write(f"Predicted Price: {predicted_price[0]:.2f}")
