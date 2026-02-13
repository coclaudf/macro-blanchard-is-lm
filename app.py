import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título y descripción
st.title("📊 Modelo IS-LM: Simulación Interactiva")
st.markdown("Basado en el modelo de economía cerrada de **Olivier Blanchard**.")

# --- BARRA LATERAL (ENTRADAS PARA EL ALUMNO) ---
st.sidebar.header("Variables de Política")

# Política Fiscal
gasto = st.sidebar.slider("Gasto Público (G)", 10, 100, 50)
impuestos = st.sidebar.slider("Impuestos (T)", 10, 100, 40)

# Política Monetaria
m_nominal = st.sidebar.slider("Oferta Monetaria Nominal (M)", 500, 2000, 1000)
precios = st.sidebar.slider("Nivel de Precios (P)", 1.0, 5.0, 2.0)

# Parámetros Estructurales (puedes dejarlos fijos o darles control)
st.sidebar.divider()
c1 = 0.6  # Propensión marginal a consumir
b1 = 0.2  # Sensibilidad de inversión ante el ingreso
b2 = 10   # Sensibilidad de inversión ante la tasa de interés

# --- LÓGICA MATEMÁTICA ---
y_range = np.linspace(0, 800, 500)

# Curva IS: i = [c0 + G - c1*T] / b2 - [ (1 - c1 - b1) / b2 ] * Y
# Simplificamos c0 a 100 para el ejemplo
autonomo = 100 + gasto - (c1 * impuestos)
is_curve = (autonomo / b2) - ((1 - c1 - b1) / b2) * y_range

# Curva LM: i = (k/h)*Y - (1/h)*(M/P)
# Supuestos: k=0.4 (sensibilidad demanda dinero a ingreso), h=20 (sensibilidad a i)
k, h = 0.4, 20
lm_curve = (k / h) * y_range - (1 / h) * (m_nominal / precios)

# --- GRÁFICO ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_range, is_curve, label="Curva IS (Bienes)", color="blue", lw=2)
ax.plot(y_range, lm_curve, label="Curva LM (Dinero)", color="red", lw=2)

# Estética del gráfico
ax.set_title("Equilibrio en el Mercado de Bienes y Dinero")
ax.set_xlabel("Ingreso / Producción (Y)")
ax.set_ylabel("Tasa de Interés (i)")
ax.set_ylim(0, 20)
ax.set_xlim(0, 800)
ax.grid(True, alpha=0.3)
ax.legend()

# Mostrar en la App
st.pyplot(fig)

# --- ANÁLISIS ECONÓMICO ---
st.info(f"**Análisis:** Con G={gasto} y M/P={m_nominal/precios:.2f}, el modelo muestra el equilibrio dinámico.")
