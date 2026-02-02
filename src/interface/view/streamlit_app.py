
import streamlit as st
import time
import sys
import os

# Add the project root to python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.interface.presenters.mock_presenter import MockPresenter

# Page config
st.set_page_config(
    page_title="Kickboxing Trainer",
    page_icon="🥊",
    layout="centered"
)

# Initialize Session State
if 'presenter' not in st.session_state:
    st.session_state.presenter = MockPresenter()

presenter = st.session_state.presenter

# --- SIDEBAR: Settings ---
with st.sidebar:
    st.header("Settings")
    lang_options = {"Français": "fr", "English": "en", "Español": "es"}
    selected_lang_label = st.selectbox("Language", list(lang_options.keys()))
    presenter.set_language(lang_options[selected_lang_label])

# --- MAIN UI ---

# Get ViewModel
vm = presenter.get_current_view_model()

# Custom CSS for styling
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {vm.background_color};
    }}
    .big-timer {{
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        color: white;
    }}
    .status-text {{
        font-size: 40px;
        text-align: center;
        color: #fbbf24;
    }}
    .instruction-text {{
        font-size: 30px;
        text-align: center;
        color: white;
        margin-top: 20px;
    }}
    .block-title {{
        font-size: 24px;
        color: #e5e7eb;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown(f"<div class='block-title'>{vm.current_block_name} - Round {vm.current_round}/{vm.total_rounds}</div>", unsafe_allow_html=True)

# Timer Display
st.markdown(f"<div class='status-text'>{vm.status_text}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='big-timer'>{vm.time_display}</div>", unsafe_allow_html=True)

# Progress Bar
st.progress(vm.progress)

# Instruction
st.markdown(f"<div class='instruction-text'>{vm.current_instruction}</div>", unsafe_allow_html=True)

# Controls
col1, col2, col3 = st.columns(3)

with col1:
    if not vm.is_running:
        if st.button("▶ START", use_container_width=True):
            presenter.start_workout()
            st.rerun()
    else:
        if st.button("⏸ PAUSE", use_container_width=True):
            presenter.pause_workout()
            st.rerun()

with col2:
    if st.button("⏮ RESET", use_container_width=True):
        presenter.reset_workout()
        st.rerun()

# Logic Loop
if vm.is_running:
    time.sleep(1)
    presenter.tick()
    st.rerun()
