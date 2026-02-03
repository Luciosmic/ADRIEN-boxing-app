
import streamlit as st
import asyncio
import sys
import os
import time

# Add the project root to python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.composition_root import CompositionRoot
from streamlit_sortables import sort_items

# Page config
st.set_page_config(
    page_title="Kickboxing Trainer",
    page_icon="🥊",
    layout="centered"
)

# Custom CSS for styling
def apply_styles(bg_color):
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color};
        }}
        .big-timer {{
            font-size: 80px;
            font-weight: bold;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px #000000;
        }}
        .status-text {{
            font-size: 40px;
            text-align: center;
            color: #fbbf24;
            text-shadow: 1px 1px 2px #000000;
        }}
        .instruction-text {{
            font-size: 30px;
            text-align: center;
            color: white;
            margin-top: 20px;
            background-color: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 10px;
        }}
        .block-title {{
            font-size: 24px;
            color: #e5e7eb;
            text-align: center;
            margin-bottom: 20px;
        }}
        </style>
        """, unsafe_allow_html=True)

# Helper to run async in sidebar/callbacks
def run_async(coro):
    return asyncio.run(coro)

# Initialize Session State
if 'presenter' not in st.session_state:
    # Use composition root to create fully-wired presenter
    presenter = CompositionRoot.create_presenter(language='fr', use_audio=True)
    run_async(presenter.initialize())
    st.session_state.presenter = presenter

presenter = st.session_state.presenter

# --- SIDEBAR: Settings & Editor ---
with st.sidebar:
    st.header("Settings")
    lang_options = {"Français": "fr", "English": "en", "Español": "es"}
    selected_lang_label = st.selectbox("Language", list(lang_options.keys()))
    if lang_options[selected_lang_label] != presenter.language:
        presenter.set_language(lang_options[selected_lang_label])
        st.rerun()

    st.divider()
    st.header("Workout Editor")
    
    # Workout Selector
    if presenter.workouts_summary:
        workout_names = [w.name for w in presenter.workouts_summary]
        selected_workout_name = st.selectbox("Select Workout", workout_names)
        
        # Find ID
        selected_w = next((w for w in presenter.workouts_summary if w.name == selected_workout_name), None)
        if selected_w and selected_w.id != presenter.current_workout_id:
             run_async(presenter.select_workout(selected_w.id))
             st.rerun()

    # Drag and Drop Blocks
    if presenter._cached_workout_detail:
        st.subheader("Order Blocks")
        blocks = presenter._cached_workout_detail.blocks
        
        # Create unique items for sortables
        # Format: "index::BlockType (Time)" to be unique and parsable
        items = [f"{i}::{b.type} ({b.work_time}s)" for i, b in enumerate(blocks)]
        
        sorted_items = sort_items(items, direction="vertical")
        
        # Logic to detect move
        if sorted_items and sorted_items != items:
            # Find the moved item
            # We assume single move for simplicity or process seq
            # Map sorted items back to original indices
            new_indices = [int(item.split("::")[0]) for item in sorted_items]
            
            # Identify first deviation
            for current_idx, original_idx in enumerate(new_indices):
                if current_idx != original_idx:
                    # Item at 'current_idx' should be 'original_idx'
                    # Call move_block
                    # Note: MoveBlock(from, to).
                    # If we move original_idx to current_idx.
                    run_async(presenter.move_block(original_idx, current_idx))
                    st.rerun()
                    break

# --- MAIN UI ---

# Tick if running
vm = presenter.get_current_view_model()
if vm.is_running:
    # Non-blocking delay? Streamlit sleep is blocking.
    # We slept at end of loop.
    pass

apply_styles(vm.background_color)

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
            run_async(presenter.start_workout())
            st.rerun()
    else:
        if st.button("⏸ PAUSE", use_container_width=True):
            run_async(presenter.pause_workout())
            st.rerun()

with col2:
    if st.button("⏮ RESET", use_container_width=True):
        run_async(presenter.reset_workout())
        st.rerun()
        
# Auto-refresh loop
if vm.is_running:
    time.sleep(1)
    run_async(presenter.tick())
    st.rerun()
