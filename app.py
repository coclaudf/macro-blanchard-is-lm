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

# --- CÁLCULO DEL EQUILIBRIO (Matemática interna) ---
# Resolvemos el sistema IS-LM para Y
# IS: i = A/b2 - B*Y  |  LM: i = (k/h)Y - (M/Ph)
B = (1 - c1 - b1) / b2
alpha = (k / h) + B
y_equilibrio = ( (autonomo / b2) + (m_nominal / (precios * h)) ) / alpha
i_equilibrio = (k / h) * y_equilibrio - (m_nominal / (precios * h))

# --- GRÁFICO MEJORADO ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_range, is_curve, label="Curva IS (Bienes)", color="blue", lw=2)
ax.plot(y_range, lm_curve, label="Curva LM (Dinero)", color="red", lw=2)

# Añadir un punto en el equilibrio
if 0 < y_equilibrio < 800:
    ax.scatter(y_equilibrio, i_equilibrio, color='black', zorder=5)
    ax.annotate(f' Equilibrio\n (Y={y_equilibrio:.1f}, i={i_equilibrio:.1f})', 
                (y_equilibrio, i_equilibrio), fontsize=10, fontweight='bold')

# Ajuste dinámico de los ejes
ax.set_title("Equilibrio en el Mercado de Bienes y Dinero (IS-LM)", fontsize=14)
ax.set_xlabel("Ingreso / Producción (Y)")
ax.set_ylabel("Tasa de Interés (i)")

# Esto asegura que si la tasa es negativa (matemáticamente), el gráfico no se vea raro
ax.set_ylim(0, max(is_curve.max(), 15)) 
ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

# --- MÉTRICAS ---
col1, col2 = st.columns(2)
col1.metric("Producción de Equilibrio (Y*)", f"{y_equilibrio:.2f}")
col2.metric("Tasa de Interés (i*)", f"{i_equilibrio:.2f}%")
