import streamlit as st
import os

# ==========================================
# 1. DFA LOGIC (Strictly matching your 19-state diagram)
# ==========================================
def get_next_state(state, char):
    """Transition function representing the DFA table."""
    if char == 'M': return 1
    if char == 'D': return 6
    if char == 'P': return 9
    if char == 'N': return 14

    if state == 0: return 0
    elif state == 1: return 2 if char == 'r' else 0
    elif state == 2:
        if char == '.': return 3
        if char == 's': return 4
        return 2 
    elif state == 3: return 3
    elif state == 4: return 5 if char == '.' else 4
    elif state == 5: return 5
    elif state == 6: return 7 if char == 'r' else 0
    elif state == 7: return 8 if char == '.' else 7
    elif state == 8: return 8
    elif state == 9: return 10 if char == 'r' else 0
    elif state == 10: return 11 if char == 'o' else 0
    elif state == 11: return 12 if char == 'f' else 0
    elif state == 12: return 13 if char == '.' else 12
    elif state == 13: return 13
    elif state == 14: return 15 if char == 'i' else 0
    elif state == 15: return 16 if char == 'c' else 0
    elif state == 16: return 17 if char == 'o' else 0
    elif state == 17: return 18 if char == 'l' else 0
    elif state == 18: return 18
    return 0

def run_dfa(text):
    """Processes text character by character."""
    accept_states = {2, 3, 4, 5, 7, 8, 12, 13, 18}
    state = 0
    current_start = -1
    matches = []

    for i, char in enumerate(text):
        prev_state = state
        state = get_next_state(state, char)

        if char in ['M', 'D', 'P', 'N'] and state in [1, 6, 9, 14]:
            current_start = i

        if state in accept_states:
            if prev_state != state:
                match_obj = {'start': current_start, 'end': i, 'pattern': text[current_start:i+1]}
                if matches and matches[-1]['start'] == current_start:
                    matches[-1] = match_obj
                else:
                    matches.append(match_obj)
    return matches


# ==========================================
# 2. STREAMLIT WEB INTERFACE (USM Theme)
# ==========================================

def main():
    st.set_page_config(
        page_title="CPT411 - L3 People Finder",
        page_icon="🔎",
        layout="wide"
    )

    # --- STYLE ---
    st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 800;
            color: #b892ff; /* Lighter purple for dark mode readability */
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #a0a0a0;
            margin-bottom: 30px;
            font-weight: 500;
        }
        .highlight-box {
            border: 1px solid #4f2b7b; 
            border-radius: 8px; 
            padding: 16px; 
            background-color: #1e1e2f;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🎓 CPT411 Project")
        st.info("**L3: People Finder**\n\nThis system uses a 19-state Deterministic Finite Automaton (DFA) to recognize specific naming patterns character-by-character.")
        
        st.markdown("### 🎯 Target Patterns")
        st.markdown("""
        * Mr, Mr.
        * Mrs, Mrs.
        * Dr, Dr.
        * Prof, Prof.
        * Nicol
        """)
        st.divider()
        st.caption("Universiti Sains Malaysia")

    # --- MAIN TITLE ---
    st.markdown('<div class="title">🔎 DFA Recognizer: People Finder</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Character-by-Character Pattern Recognition System</div>', unsafe_allow_html=True)

    # --- SESSION STATE INITIALIZATION ---
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "last_uploaded" not in st.session_state:
        st.session_state.last_uploaded = None

    # --- CALLBACK FUNCTION TO CLEAR INPUTS ---
    def clear_all_inputs():
        """This runs BEFORE the page redraws, avoiding the instantiation error."""
        st.session_state.input_text = ""
        st.session_state.uploader_key += 1
        st.session_state.last_uploaded = None

    # --- INPUT SECTION ---
    st.markdown("#### 📝 1. Provide Text to Scan")

    uploaded_file = st.file_uploader(
        "Upload a .txt file (Optional)", 
        type=["txt"], 
        key=f"uploader_{st.session_state.uploader_key}"
    )

    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        if st.session_state.last_uploaded != file_content:
            st.session_state.input_text = file_content
            st.session_state.last_uploaded = file_content

    # The text area is tied to the session state variable
    text = st.text_area(
        "Text Input",
        key="input_text",
        height=180,
        label_visibility="collapsed",
        placeholder="Type your text here or upload a .txt file above..."
    )

    # --- BUTTONS (One Line, Equal Size) ---
    st.write("") # Little bit of spacing
    col1, col2, col3 = st.columns(3)

    with col1:
        # type="primary" makes the button stand out with a solid background color!
        run_btn = st.button("🚀 Run DFA Scanner", type="primary", use_container_width=True)

    with col2:
        clear_res_btn = st.button("🧹 Clear Results", use_container_width=True)

    with col3:
        st.button("🗑 Clear Input", use_container_width=True, on_click=clear_all_inputs)

    st.divider()

    # --- PROCESS & RESULTS ---
    if run_btn:
        current_text = st.session_state.input_text.strip()

        if not current_text:
            st.warning("⚠️ Please enter or upload text before running the machine.")
            return

        matches = run_dfa(current_text)

        st.markdown("#### 📊 2. Scan Results")

        # STATUS BANNER
        if matches:
            st.success(f"✅ **STATUS: ACCEPT** — The machine found **{len(matches)}** pattern(s) in the text.")
        else:
            st.error("❌ **STATUS: REJECT** — No target patterns were found in the text.")

        if matches:
            # Count occurrences of each pattern
            pattern_counts = {}
            for m in matches:
                pat = m['pattern']
                pattern_counts[pat] = pattern_counts.get(pat, 0) + 1

            # --- TABS ---
            tab1, tab2, tab3 = st.tabs([
                "📈 Dashboard Summary",
                "🔢 Pattern Occurrences",
                "📍 Exact Positions",
            ])

            # -------- TAB 1: SUMMARY (Using Metrics) --------
            with tab1:
                st.write("<br>", unsafe_allow_html=True)
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric(label="Total Patterns Found", value=len(matches))
                m_col2.metric(label="Unique Titles/Names", value=len(pattern_counts))
                m_col3.metric(label="Total Characters Scanned", value=len(current_text))
                st.write("<br>", unsafe_allow_html=True)

            # -------- TAB 2: OCCURRENCES (Using a Table) --------
            with tab2:
                st.write("<br>", unsafe_allow_html=True)
                table_md = "| Pattern Found | Total Occurrences |\n|---|---|\n"
                for pat, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
                    table_md += f"| **{pat}** | {count} |\n"
                st.markdown(table_md)

            # -------- TAB 3: POSITIONS (Using a Table) --------
            with tab3:
                st.write("<br>", unsafe_allow_html=True)
                pos_md = "| # | Matched Pattern | Start Index | End Index |\n|---|---|---|---|\n"
                for idx, m in enumerate(matches, 1):
                    pos_md += f"| {idx} | **{m['pattern']}** | {m['start']} | {m['end']} |\n"
                st.markdown(pos_md)

            # --- HIGHLIGHTED TEXT ---
            st.write("<br>", unsafe_allow_html=True)
            st.markdown("#### ✨ 3. Visualized Output")
            
            highlighted = ""
            last = 0

            for m in matches:
                highlighted += current_text[last:m['start']]
                highlighted += f"<mark style='background-color:#ffcb05; color:#000000; font-weight:bold; padding:2px 4px; border-radius:4px; box-shadow: 0px 2px 4px rgba(0,0,0,0.2);'>{current_text[m['start']:m['end']+1]}</mark>"
                last = m['end'] + 1

            highlighted += current_text[last:]

            st.markdown(f"""
            <div class="highlight-box">
                <p style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.8; color: #e0e0e0; margin: 0; white-space: pre-wrap; word-wrap: break-word;">
                    {highlighted}
                </p>
            </div>
            """, unsafe_allow_html=True)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    main()
