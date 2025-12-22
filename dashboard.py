import streamlit as st
import requests
import time
BACKEND_URL = "https://your-appscrip-project.vercel.app/docs"

st.set_page_config(page_title="Appscrip Trade Intel", layout="wide")

# --- CALLBACKS ---
def add_to_comparison(item):
    if item not in st.session_state.compare:
        st.session_state.compare.append(item)
        st.toast(f"✅ Added {item['sector']}")

def clear_comparison():
    st.session_state.compare = []

# --- STATE MANAGEMENT ---
if "history" not in st.session_state: st.session_state.history = []
if "curr" not in st.session_state: st.session_state.curr = None
if "compare" not in st.session_state: st.session_state.compare = []
if "cooldown" not in st.session_state: st.session_state.cooldown = 0

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    key = st.text_input("X-API-KEY", type="password", value="appscrip_assignment_secret")
    model_choice = st.selectbox("Free Tier Model", ["gemini-2.5-flash-lite", "gemini-2.0-flash"])
    
    st.divider()
    st.subheader("📜 History")
    for idx, item in enumerate(reversed(st.session_state.history)):
        c1, c2 = st.columns([4, 1])
        if c1.button(f"📄 {item['sector']}", key=f"v_{idx}"):
            st.session_state.curr = item
        c2.button("➕", key=f"c_{idx}", on_click=add_to_comparison, args=(item,))

# --- MAIN UI ---
st.title("📊 Indian Market Intelligence")

# Check if we are in cooldown
current_ts = time.time()
if st.session_state.cooldown > current_ts:
    remaining = int(st.session_state.cooldown - current_ts)
    st.warning(f"⏳ Free Tier Rate Limit reached. Cooling down for {remaining} seconds...")
    st.progress(remaining / 60)
    time.sleep(1)
    st.rerun()

tab1, tab2 = st.tabs(["⚡ New Analysis", "⚖️ Comparison Mode"])

with tab1:
    sector = st.text_input("Target Sector", placeholder="e.g., Renewable Energy")
    if st.button("Generate Intelligence"):
        with st.spinner("Fetching 2025 Market Data..."):
            try:
                res = requests.get(
                    f"{BACKEND_URL}/analyze/{sector.lower()}",
                    headers={"X-API-KEY": key},
                    params={"model": model_choice},
                    timeout=90
                )
                if res.status_code == 200:
                    data = {"sector": sector.title(), "content": res.text, "model": model_choice}
                    st.session_state.history.append(data)
                    st.session_state.curr = data
                    st.rerun()
                elif res.status_code == 429:
                    st.session_state.cooldown = time.time() + 60
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Backend unreachable: {e}")

    if st.session_state.curr:
        st.divider()
        st.subheader(f"Strategic Report: {st.session_state.curr['sector']}")
        st.markdown(st.session_state.curr['content'])

with tab2:
    if not st.session_state.compare:
        st.info("Add reports from History (➕) to view side-by-side.")
    else:
        # Comparison Controls
        c1, c2 = st.columns([1, 4])
        c1.button("🗑️ Clear All", on_click=clear_comparison)
        
        # Markdown Export
        report_text = "# Market Comparison\n\n"
        for item in st.session_state.compare:
            report_text += f"## {item['sector']}\n{item['content']}\n\n---\n\n"
        c2.download_button("📥 Export as Markdown", report_text, file_name="comparison.md")
        
        st.divider()
        # Side-by-Side Display
        cols = st.columns(len(st.session_state.compare))
        for i, item in enumerate(st.session_state.compare):
            with cols[i]:
                st.subheader(item['sector'])
                st.caption(f"Model: {item['model']}")
                st.markdown(item['content'])