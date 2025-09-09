import streamlit as st
from flowchart import generate_dot_code
from exporter import save_dot_file, render_dot



st.set_page_config(page_title="AI Flowchart Generator", layout="wide")
st.title("🧠 AI Flowchart Generator (LangChain + Graphviz)")  

prompt = st.text_area("Describe your system or flow:")

if st.button("Generate Flowchart"):
    if not prompt.strip():
        st.warning("Please enter a valid description.")
    else:
        with st.spinner("Generating..."):
            dot_code = generate_dot_code(prompt)

            st.subheader("📄 DOT Code")
            st.code(dot_code, language='dot')

            st.subheader("📊 Flowchart Preview")
            st.graphviz_chart(dot_code)

            # dot_file = save_dot_file(dot_code)
            png_file = render_dot(dot_code, "png")
            pdf_file = render_dot(dot_code, "pdf")

            st.subheader("⬇️ Downloads")
            # with open(dot_file, "rb") as f:
            #     st.download_button("📥 Download DOT", f, file_name="flowchart.dot", mime="text/plain")

            with open(png_file, "rb") as f_png:
                st.download_button("🖼️ Download PNG", f_png, file_name="flowchart.png", mime="image/png")

            with open(pdf_file, "rb") as f_pdf:
                st.download_button("📄 Download PDF", f_pdf, file_name="flowchart.pdf", mime="application/pdf")
