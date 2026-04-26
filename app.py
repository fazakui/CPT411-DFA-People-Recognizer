import streamlit as st

# 1. DFA LOGIC 
def get_next_state(state, char):
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
    accept_states = {2, 3, 4, 5, 7, 8, 12, 13, 18}
    state, current_start = 0, -1
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

# 2. STREAMLIT WEB INTERFACE
def main():
    st.set_page_config(page_title="CPT411 - L3 People Finder", page_icon="🔎", layout="centered")

    st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .title { text-align: center; font-size: 2rem; font-weight: 800; color: #b892ff; margin-bottom: 0; }
        .subtitle { text-align: center; font-size: 1rem; color: #a0a0a0; margin-bottom: 15px; }
        
        .highlight-box { 
            border: 1px solid rgba(128, 128, 128, 0.2); 
            border-radius: 8px; 
            padding: 15px; 
            background-color: var(--secondary-background-color); /* Auto-switches to white/light-gray in light mode */
            color: var(--text-color); /* Ensures text is always readable */
            box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.15); /* 0px offset creates an even shadow on ALL sides */
        }
        
        table { width: 100%; } 
        th { text-align: left !important; }
    </style>
    """, unsafe_allow_html=True)

    # HEADER 
    st.markdown('<div class="title">🔎 DFA Recognizer: People Finder</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Character-by-Character Pattern Recognition System</div>', unsafe_allow_html=True)

    # SESSION STATE 
    if "uploader_key" not in st.session_state: st.session_state.uploader_key = 0
    if "input_text" not in st.session_state: st.session_state.input_text = ""
    if "last_uploaded" not in st.session_state: st.session_state.last_uploaded = None

    def clear_all_inputs():
        st.session_state.input_text = ""
        st.session_state.uploader_key += 1
        st.session_state.last_uploaded = None

    # INPUT 
    uploaded_file = st.file_uploader("Upload .txt file (Optional)", type=["txt"], key=f"uploader_{st.session_state.uploader_key}")
    if uploaded_file:
        file_content = uploaded_file.getvalue().decode("utf-8")
        if st.session_state.last_uploaded != file_content:
            st.session_state.input_text = file_content
            st.session_state.last_uploaded = file_content

    text = st.text_area("Text Input", key="input_text", height=150, label_visibility="collapsed", placeholder="Type your text here...")

    # BUTTONS 
    col1, col2, col3 = st.columns(3)
    run_btn = col1.button("Run DFA Scanner", type="primary", use_container_width=True)
    col2.button("Clear Results", use_container_width=True)
    col3.button("Clear Input", use_container_width=True, on_click=clear_all_inputs)

    # RESULTS 
    if run_btn:
        current_text = st.session_state.input_text.strip()
        if not current_text:
            st.warning("Please enter text.")
            return

        matches = run_dfa(current_text)

        if matches:
            st.success(f" **ACCEPT:** Found **{len(matches)}** pattern(s).")
            pattern_counts = {}
            for m in matches: pattern_counts[m['pattern']] = pattern_counts.get(m['pattern'], 0) + 1

            # COMPACT DATA DASHBOARD
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Total Patterns", len(matches))
            m_col2.metric("Unique Titles", len(pattern_counts))
            m_col3.metric("Characters Scanned", len(current_text))
            
            st.markdown("---") # Thin divider

            t_col1, t_col2 = st.columns([1, 1.2]) 
            with t_col1:
                st.markdown("##### Pattern Occurrences")
                table_md = "| Pattern | Occurrences |\n|---|---|\n"
                for pat, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True): table_md += f"| **{pat}** | {count} |\n"
                st.markdown(table_md)

            with t_col2:
                st.markdown("##### Exact Positions")
                pos_md = "| # | Pattern | Start | End |\n|---|---|---|---|\n"
                for idx, m in enumerate(matches, 1): pos_md += f"| {idx} | **{m['pattern']}** | {m['start']} | {m['end']} |\n"
                st.markdown(pos_md)

            # VISUALIZATION
            st.markdown("##### Output")
            highlighted, last = "", 0
            for m in matches:
                highlighted += current_text[last:m['start']]
                highlighted += f"<mark style='background-color:#ffcb05; color:#000; font-weight:bold; padding:2px 4px; border-radius:4px;'>{current_text[m['start']:m['end']+1]}</mark>"
                last = m['end'] + 1
            highlighted += current_text[last:]

            st.markdown(f'<div class="highlight-box"><p style="margin:0; line-height: 1.8; white-space:pre-wrap;">{highlighted}</p></div>', unsafe_allow_html=True)
        else:
            st.error(" **REJECT:** No target patterns found.")

if __name__ == "__main__":
    main()
