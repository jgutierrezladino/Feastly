import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Título de la aplicación
st.title("Aplicación de Predicción con Machine Learning")

# Descripción de la aplicación
st.write("Esta es una aplicación de ejemplo para hacer predicciones usando un modelo de regresión lineal simple.")

# Input de datos para realizar predicciones
st.subheader("Ingresar datos")
input_data = st.number_input("Ingrese el valor de entrada:", min_value=0.0, max_value=100.0, step=1.0)

# Entrenamiento de un modelo de ejemplo (esto se haría antes en un flujo real)
X = np.array([[10], [20], [30], [40], [50]])
y = np.array([15, 25, 35, 45, 55])
model = LinearRegression().fit(X, y)

# Botón para realizar predicción
if st.button("Predecir"):
    prediction = model.predict([[input_data]])
    st.write(f"La predicción del modelo es: {prediction[0]:.2f}")
else:
    st.write("Ingrese un valor y haga clic en 'Predecir' para ver el resultado.")

