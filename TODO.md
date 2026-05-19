- [x] Apply replacements for deprecated Streamlit parameter `use_container_width` (True/False mapping) across the whole project (no occurrences found)
- [ ] Remove/adjust any Streamlit warnings from rendering code
- [x] Ensure sidebar is declared at the very beginning of each page (after st.set_page_config / before heavy work)
- [x] Ensure no heavy computation runs before sidebar is defined (gated heavy work)
- [x] Ensure no dataframe/plot rendering happens before sidebar is defined (reordered EDA load)
- [x] Re-run search to confirm no `use_container_width` remains and check affected render calls
- [ ] Provide list of modified files and exact corrections


