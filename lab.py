import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- AYARLAR ---
st.set_page_config(page_title="Derin'in Fizik Projesi", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    h1 { color: #008080; text-align: center; font-family: 'Segoe UI', sans-serif; }
    .stSidebar { background-color: #bdc3c7; }
    </style>
    """, unsafe_allow_html=True)

st.title("💚 DERİNİN FİZİK PROJESİ 💚")

# --- KONTROL ---
st.sidebar.header("⚙️ Kontrol Paneli")
atıs_turu = st.sidebar.radio("Atış Türü:", ("Yatay Atış", "Dikey Atış"))
v0 = st.sidebar.slider("İlk Hız (m/s)", 1, 100, 25)
h = st.sidebar.slider("Yükseklik (m)", 0, 500, 100)
g = 10 # Sabit yerçekimi

# --- HESAPLAMA ---
if atıs_turu == "Yatay Atış":
    t_flight = np.sqrt(2 * h / g)
    t = np.linspace(0, t_flight, 100)
    x = v0 * t
    y = h - 0.5 * g * t**2
else:
    t_flight = (v0 + np.sqrt(v0**2 + 2 * g * h)) / g
    t = np.linspace(0, t_flight, 100)
    x = np.zeros_like(t)
    y = h + v0 * t - 0.5 * g * t**2

# --- GRAFİK ---
fig = go.Figure()
# Sabit top başlangıcı
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', name='Top', marker=dict(size=15, color='#008080')))
# Yörünge
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#00ced1', width=2, dash='dash')))

# Animasyon ayarları (Hıza göre süre)
duration = int(3000 / (v0 * 0.5 + 10))
fig.update_layout(
    plot_bgcolor='#ecf0f1',
    xaxis=dict(range=[-10, max(x)+10], title="Mesafe (m)"),
    yaxis=dict(range=[-5, h+50], title="Yükseklik (m)"),
    updatemenus=[dict(type="buttons", buttons=[
        dict(label="🚀 Başlat", method="animate", args=[None, {"frame": {"duration": duration}}]),
        dict(label="⏸️ Durdur", method="animate", args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
        dict(label="🔄 Yenile", method="animate", args=[[None], {"mode": "immediate"}])
    ])]
)
fig.frames = [go.Frame(data=[go.Scatter(x=[x[i]], y=[y[i]])]) for i in range(len(t))]

# --- EKRAN ---
col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.success(f"### 🎯 {atıs_turu} Mantığı")
    if atıs_turu == "Yatay Atış":
        st.latex(r"x = v_0 \cdot t \quad , \quad y = h - \frac{1}{2}gt^2")
        st.write("Yatay atışta yatay hız sabittir, dikeyde ise cisim serbest düşme yapar.")
    else:
        st.latex(r"y = h + v_0 \cdot t - \frac{1}{2}gt^2")
        st.write("Dikey atışta cisim, yerçekimine karşı yukarı yavaşlar ve sonra hızlanır.")
    st.info(f"**Uçuş Süresi:** {t_flight:.2f} s")