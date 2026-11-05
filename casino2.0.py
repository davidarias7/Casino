import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Configuración de página y Estilo CSS Personalizado
# ---------------------------------------------------------
st.set_page_config(
    page_title="Royal Streamlit Casino 🎰",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado estilo Casino de Lujo
st.markdown("""
<style>
    /* Fondo principal y fuentes */
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }

    /* Títulos dorados */
    .casino-header {
        font-family: 'Trebuchet MS', sans-serif;
        color: #ffd700;
        text-shadow: 0px 0px 12px rgba(255, 215, 0, 0.6);
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .casino-sub {
        text-align: center;
        color: #cccccc;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* Targetas de saldo y métricas */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #00ff88 !important;
        text-shadow: 0px 0px 8px rgba(0, 255, 136, 0.4);
    }

    /* Contenedores de juegos */
    .slot-box {
        background: linear-gradient(145deg, #181d27, #11141c);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.15);
        margin-bottom: 20px;
    }

    /* Carretes del tragamonedas */
    .slot-reel {
        font-size: 4.5rem;
        background: #000000;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid #333;
        display: inline-block;
        margin: 0 5px;
        box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2);
    }

    /* Botones de acción */
    .stButton>button {
        background: linear-gradient(45deg, #ffd700, #ff9900);
        color: #000;
        font-weight: bold;
        font-size: 1.2rem;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.6);
        color: #000;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Inicialización del Estado de Sesión (Session State)
# ---------------------------------------------------------
if "balance" not in st_session_state if "st_session_state" in locals() else False:
    pass

if "balance" not in st.session_state:
    st.session_state.balance = 1000  # Saldo inicial
if "history" not in st.session_state:
    st.session_state.history = []
if "bj_game" not in st.session_state:
    st.session_state.bj_game = {"active": False, "player_hand": [], "dealer_hand": [], "bet": 0}

# ---------------------------------------------------------
# 3. Barra Lateral - Saldo, Recarga y Historial
# ---------------------------------------------------------
st.sidebar.markdown("## 💰 VIP Banker")
st.sidebar.metric("Saldo Disponible", f"${st.session_state.balance:,.2f}")

# Recargar saldo
with st.sidebar.expander("💳 Recargar Fichas"):
    add_amount = st.number_input("Monto a depositar ($)", min_value=10, max_value=5000, value=500, step=50)
    if st.button("Depositar Fichas"):
        st.session_state.balance += add_amount
        st.sidebar.success(f"¡Se agregaron ${add_amount} a tu cuenta!")
        st.rerun()

# Historial de Apuestas
st.sidebar.markdown("---")
st.sidebar.markdown("### 📜 Historial de Apuestas")
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    st.sidebar.dataframe(df_hist.iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.sidebar.info("Aún no has hecho apuestas en esta sesión.")

# Resetear Sesión
if st.sidebar.button("🔄 Reiniciar Sesión"):
    st.session_state.balance = 1000
    st.session_state.history = []
    st.session_state.bj_game = {"active": False, "player_hand": [], "dealer_hand": [], "bet": 0}
    st.rerun()

# ---------------------------------------------------------
# 4. Encabezado Principal
# ---------------------------------------------------------
st.markdown("<div class='casino-header'>🎰 ROYAL STREAMLIT CASINO 💎</div>", unsafe_allow_html=True)
st.markdown("<div class='casino-sub'>La experiencia VIP de apuestas virtuales en Python</div>", unsafe_allow_html=True)

# Selección de juego
tab1, tab2, tab3 = st.tabs(["🎰 Tragamonedas (Slots)", "🎡 Ruleta", "🃏 Blackjack 21"])

# =========================================================
# JUEGO 1: TRAGAMONEDAS (SLOT MACHINE)
# =========================================================
with tab1:
    st.subheader("🎰 Máquina Tragamonedas Deluxe")
    st.caption("¡3 símbolos iguales pagan 10x! ¡2 símbolos iguales pagan 2x!")

    col_play, col_vis = st.columns([1, 2])

    with col_play:
        apuesta_slot = st.number_input("Apuesta ($)", min_value=5, max_value=int(max(5, st.session_state.balance)),
                                       value=25, step=5, key="slot_bet")
        btn_spin = st.button("🔥 ¡GIRAR AHORA!", key="btn_slot")

    with col_vis:
        symbols = ["7️⃣", "💎", "👑", "🍒", "🔔", "🍋", "🍀"]

        # Área de carretes
        reel_container = st.empty()
        reel_container.markdown("""
        <div class='slot-box'>
            <span class='slot-reel'>❓</span>
            <span class='slot-reel'>❓</span>
            <span class='slot-reel'>❓</span>
        </div>
        """, unsafe_allow_html=True)

        if btn_spin:
            if st.session_state.balance < apuesta_slot:
                st.error("❌ ¡Saldo insuficiente!")
            else:
                st.session_state.balance -= apuesta_slot

                # Efecto de animación de giro
                for _ in range(12):
                    r1 = random.choice(symbols)
                    r2 = random.choice(symbols)
                    r3 = random.choice(symbols)
                    reel_container.markdown(f"""
                    <div class='slot-box'>
                        <span class='slot-reel'>{r1}</span>
                        <span class='slot-reel'>{r2}</span>
                        <span class='slot-reel'>{r3}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.08)

                # Resultado final
                res1, res2, res3 = random.choice(symbols), random.choice(symbols), random.choice(symbols)
                reel_container.markdown(f"""
                <div class='slot-box'>
                    <span class='slot-reel'>{res1}</span>
                    <span class='slot-reel'>{res2}</span>
                    <span class='slot-reel'>{res3}</span>
                </div>
                """, unsafe_allow_html=True)

                # Cálculo de ganancias
                if res1 == res2 == res3:
                    premio = apuesta_slot * 10
                    st.session_state.balance += premio
                    st.balloons()
                    st.success(f"🎉 ¡¡JACKPOT TRIPLE!! Ganaste ${premio:,.2f} (10x)")
                    st.session_state.history.append(
                        {"Juego": "Slot", "Apuesta": apuesta_slot, "Resultado": f"+${premio}"})
                elif res1 == res2 or res2 == res3 or res1 == res3:
                    premio = apuesta_slot * 2
                    st.session_state.balance += premio
                    st.info(f"✨ ¡Par coincidente! Ganaste ${premio:,.2f} (2x)")
                    st.session_state.history.append(
                        {"Juego": "Slot", "Apuesta": apuesta_slot, "Resultado": f"+${premio}"})
                else:
                    st.error(f"❌ Sin suerte esta vez. Perdiste ${apuesta_slot}")
                    st.session_state.history.append(
                        {"Juego": "Slot", "Apuesta": apuesta_slot, "Resultado": f"-${apuesta_slot}"})

                time.sleep(1)
                st.rerun()

# =========================================================
# JUEGO 2: RULETA FRANCESA / AMERICANA
# =========================================================
with tab2:
    st.subheader("🎡 Ruleta Monte Carlo")

    col_r_ctrl, col_r_graph = st.columns([1, 1])

    with col_r_ctrl:
        apuesta_ruleta = st.number_input("Monto de Apuesta ($)", min_value=5,
                                         max_value=int(max(5, st.session_state.balance)), value=50, step=10,
                                         key="roulette_bet")
        tipo_apuesta = st.selectbox("Tipo de Apuesta", ["Color (Rojo/Negro)", "Par/Impar", "Número Exacto (0-36)"])

        opcion_apuesta = None
        if tipo_apuesta == "Color (Rojo/Negro)":
            opcion_apuesta = st.radio("Selecciona Color:", ["🔴 Rojo", "⚫ Negro"])
        elif tipo_apuesta == "Par/Impar":
            opcion_apuesta = st.radio("Selecciona:", ["Par", "Impar"])
        else:
            opcion_apuesta = st.slider("Selecciona Número:", 0, 36, 7)

        btn_spin_roulette = st.button("🎲 GIRAR RULETA", key="btn_roulette")

    with col_r_graph:
        # Colores reales de ruleta
        rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

        if btn_spin_roulette:
            if st.session_state.balance < apuesta_ruleta:
                st.error("❌ ¡Saldo insuficiente!")
            else:
                st.session_state.balance -= apuesta_ruleta

                # Simular giro
                with st.spinner("Girando la rueda y lanzando la bola..."):
                    time.sleep(1.5)
                    numero_ganador = random.randint(0, 36)

                    if numero_ganador == 0:
                        color_ganador = "🟢 Verde"
                    elif numero_ganador in rojos:
                        color_ganador = "🔴 Rojo"
                    else:
                        color_ganador = "⚫ Negro"

                st.markdown(f"### Resultado: **{numero_ganador}** ({color_ganador})")

                # Evaluar victoria
                gano = False
                pago = 0

                if tipo_apuesta == "Color (Rojo/Negro)":
                    if (opcion_apuesta == "🔴 Rojo" and color_ganador == "🔴 Rojo") or \
                            (opcion_apuesta == "⚫ Negro" and color_ganador == "⚫ Negro"):
                        gano = True
                        pago = apuesta_ruleta * 2
                elif tipo_apuesta == "Par/Impar":
                    if numero_ganador != 0:
                        es_par = (numero_ganador % 2 == 0)
                        if (opcion_apuesta == "Par" and es_par) or (opcion_apuesta == "Impar" and not es_par):
                            gano = True
                            pago = apuesta_ruleta * 2
                else:  # Número exacto
                    if opcion_apuesta == numero_ganador:
                        gano = True
                        pago = apuesta_ruleta * 36

                if gano:
                    st.session_state.balance += pago
                    st.snow()
                    st.success(f"🎉 ¡ACERTASTE! Ganaste ${pago:,.2f}")
                    st.session_state.history.append(
                        {"Juego": "Ruleta", "Apuesta": apuesta_ruleta, "Resultado": f"+${pago}"})
                else:
                    st.error(f"❌ Perdiste ${apuesta_ruleta:,.2f}")
                    st.session_state.history.append(
                        {"Juego": "Ruleta", "Apuesta": apuesta_ruleta, "Resultado": f"-${apuesta_ruleta}"})

                time.sleep(1.5)
                st.rerun()

# =========================================================
# JUEGO 3: BLACKJACK 21
# =========================================================
with tab3:
    st.subheader("🃏 Blackjack Royal (21)")


    # Lógica de Cartas
    def crear_carta():
        palos = ["♠️", "♥️", "♦️", "♣️"]
        valores = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        v = random.choice(valores)
        p = random.choice(palos)
        return {"num": v, "palo": p}


    def calcular_puntos(mano):
        puntos = 0
        ases = 0
        for c in mano:
            v = c["num"]
            if v in ["J", "Q", "K"]:
                puntos += 10
            elif v == "A":
                ases += 1
                puntos += 11
            else:
                puntos += int(v)
        while puntos > 21 and ases > 0:
            puntos -= 10
            ases -= 1
        return puntos


    def render_mano(mano, oculta=False):
        html = "<div style='display: flex; gap: 10px;'>"
        for idx, c in enumerate(mano):
            if oculta and idx == 0:
                html += "<div style='background:#222; border:2px solid #555; padding:15px; border-radius:8px; font-size:1.5rem;'>❓</div>"
            else:
                color = "#ff4d4d" if c["palo"] in ["♥️", "♦️"] else "#ffffff"
                html += f"<div style='background:#1c2333; border:2px solid #ffd700; padding:10px 15px; border-radius:8px; color:{color}; font-size:1.4rem; font-weight:bold;'>{c['num']}{c['palo']}</div>"
        html += "</div>"
        return html


    game = st.session_state.bj_game

    if not game["active"]:
        col_bj_start, _ = st.columns([1, 2])
        with col_bj_start:
            bet_bj = st.number_input("Apuesta Blackjack ($)", min_value=10,
                                     max_value=int(max(10, st.session_state.balance)), value=50, step=10,
                                     key="bj_bet_input")
            if st.button("🎮 INICIAR PARTIDA"):
                if st.session_state.balance < bet_bj:
                    st.error("❌ Saldo insuficiente")
                else:
                    st.session_state.balance -= bet_bj
                    st.session_state.bj_game = {
                        "active": True,
                        "player_hand": [crear_carta(), crear_carta()],
                        "dealer_hand": [crear_carta(), crear_carta()],
                        "bet": bet_bj
                    }
                    st.rerun()
    else:
        pts_player = calcular_puntos(game["player_hand"])

        # Mesa de Blackjack
        c_dealer, c_player = st.columns(2)

        with c_dealer:
            st.markdown("### 🤵 Mano del Crupier")
            st.markdown(render_mano(game["dealer_hand"], oculta=True), unsafe_allow_html=True)

        with c_player:
            st.markdown("### 🫵 Tu Mano")
            st.markdown(render_mano(game["player_hand"]), unsafe_allow_html=True)
            st.markdown(f"**Puntos Totales: {pts_player}**")

        st.markdown("---")

        # Acciones
        c_hit, c_stand, _ = st.columns([1, 1, 2])

        if pts_player > 21:
            st.error(f"💥 ¡Te pasaste de 21! Perdiste ${game['bet']}")
            st.session_state.history.append(
                {"Juego": "Blackjack", "Apuesta": game['bet'], "Resultado": f"-${game['bet']}"})
            st.session_state.bj_game["active"] = False
            if st.button("Nueva Partida"):
                st.rerun()
        else:
            if c_hit.button("🃏 Pedir Carta (Hit)"):
                game["player_hand"].append(crear_carta())
                st.rerun()

            if c_stand.button("✋ Plantarse (Stand)"):
                # Turno del Crupier
                pts_dealer = calcular_puntos(game["dealer_hand"])
                while pts_dealer < 17:
                    game["dealer_hand"].append(crear_carta())
                    pts_dealer = calcular_puntos(game["dealer_hand"])

                # Definir ganador
                st.markdown("### 🏁 Resultado Final")
                st.markdown(f"**Crupier obtuvo {pts_dealer} puntos.**")

                if pts_dealer > 21 or pts_player > pts_dealer:
                    pago = game["bet"] * 2
                    st.session_state.balance += pago
                    st.balloons()
                    st.success(f"🏆 ¡GANASTE! Recibes ${pago:,.2f}")
                    st.session_state.history.append(
                        {"Juego": "Blackjack", "Apuesta": game['bet'], "Resultado": f"+${pago}"})
                elif pts_player == pts_dealer:
                    st.session_state.balance += game["bet"]
                    st.warning("⚖️ Empate (Push). Te devolvemos tu apuesta.")
                    st.session_state.history.append(
                        {"Juego": "Blackjack", "Apuesta": game['bet'], "Resultado": "$0 (Empate)"})
                else:
                    st.error(f"❌ El Crupier gana. Perdiste ${game['bet']}")
                    st.session_state.history.append(
                        {"Juego": "Blackjack", "Apuesta": game['bet'], "Resultado": f"-${game['bet']}"})

                st.session_state.bj_game["active"] = False
                time.sleep(2)
                st.button("Jugar Otra Vez")
