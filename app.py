import streamlit as st
from flowchart import generate_dot_code
from exporter import save_dot_file, render_dot
import time

# Page configuration
st.set_page_config(
    page_title="AI Flowchart Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS for styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    
    .header-container {
        text-align: center;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .warning-msg {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .info-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4facfe;
        margin: 1rem 0;
    }
    
    .download-container {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'flowchart_generated' not in st.session_state:
    st.session_state.flowchart_generated = False
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0
if 'total_chars' not in st.session_state:
    st.session_state.total_chars = 0

# Header
st.markdown("""
<div class="header-container">
    <h1>🧠 AI Flowchart Generator</h1>
    <p>Transform your ideas into beautiful flowcharts using LangChain + Graphviz</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    
    # Statistics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{st.session_state.generation_count}</h3>
            <p>Flowchart</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{st.session_state.total_chars}</h3>
            <p>Character</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    # Example prompts
    st.subheader("💡 Quick Examples")
    
    if st.button("🔐 Login System", use_container_width=True):
        st.session_state.example_text = "User login system with authentication, validation, and dashboard access flow"
    
    if st.button("🛒 Checkout Process", use_container_width=True):
        st.session_state.example_text = "E-commerce checkout flow with cart review, payment processing, and order confirmation"
    
    if st.button("📊 Data Pipeline", use_container_width=True):
        st.session_state.example_text = "Data processing pipeline with validation, transformation, analysis, and reporting stages"
    
    st.markdown("---")
    
    # Tips
    st.markdown("""
    <div class="info-card">
        <h4>💡 Pro Tips</h4>
        <ul>
            <li>Be specific about each step</li>
            <li>Include decision points</li>
            <li>Mention start/end states</li>
            <li>Describe the sequence clearly</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Describe Your Workflow")
    
    # Get example text if button was clicked
    initial_text = ""
    if 'example_text' in st.session_state:
        initial_text = st.session_state.example_text
        # del st.session_state.example_text
    
    # Text input area - this should work now
    prompt = st.text_area(
        "Enter your system or process description:",
        value=initial_text if initial_text else 
        st.session_state.get('current_prompt', ''),
        height=250,
        placeholder="""Example descriptions:

• User Registration Process:
  - User enters details
  - System validates input
  - Check if user exists
  - Create account or show error
  - Send confirmation email

• Order Processing:
  - Receive order
  - Check inventory
  - Process payment
  - Update inventory
  - Ship product
  - Send tracking info""",
        help="Describe your workflow step by step"
    )
    
    # Character counter
    char_count = len(prompt) if prompt else 0
    max_chars = 2000
    
    # Progress bar for character count
    progress = min(char_count / max_chars, 1.0) if max_chars > 0 else 0
    st.progress(progress)
    
    # Character count display
    color = "🔴" if char_count > max_chars * 0.9 else "🟡" if char_count > max_chars * 0.7 else "🟢"
    st.caption(f"{color} {char_count}/{max_chars} characters")
    if prompt:
        st.session_state.current_prompt = prompt
    # Generate button
    generate_clicked = st.button("🚀 Generate Flowchart", type="primary", use_container_width=True)
    
    if generate_clicked:
        if not prompt or not prompt.strip():
            st.markdown("""
            <div class="warning-msg">
                ⚠️ Please enter a description of your workflow to generate a flowchart.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show loading state
            with st.spinner("🔄 Generating your flowchart..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Progress simulation
                for i in range(0, 101, 5):
                    progress_bar.progress(i)
                    if i < 30:
                        status_text.text("🤖 Analyzing description...")
                    elif i < 60:
                        status_text.text("🎨 Creating flowchart...")
                    elif i < 90:
                        status_text.text("⚙️ Generating code...")
                    else:
                        status_text.text("✨ Finalizing...")
                    time.sleep(0.1)
                
                try:
                    # Generate flowchart using your existing function
                    dot_code = generate_dot_code(prompt)
                    
                    # Update session state
                    st.session_state.flowchart_generated = True
                    st.session_state.generation_count += 1
                    st.session_state.total_chars += char_count
                    st.session_state.current_dot_code = dot_code
                    st.session_state.current_prompt = prompt
                    
                    # Success message
                    progress_bar.progress(100)
                    status_text.text("✅ Success!")
                    
                    st.markdown("""
                    <div class="success-msg">
                        🎉 Flowchart generated successfully! Check the preview and download options →
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.rerun()
                    
                except Exception as e:
                    st.markdown(f"""
                    <div class="warning-msg">
                        ❌ Error: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)

with col2:
    st.subheader("📊 Output")
    
    if st.session_state.flowchart_generated and 'current_dot_code' in st.session_state:
        # Tabs for output
        tab1, tab2, tab3 = st.tabs(["🖼️ Preview", "📄 Code", "⬇️ Download"])
        
        with tab1:
            st.markdown("**Flowchart Preview:**")
            try:
                st.graphviz_chart(st.session_state.current_dot_code)
            except Exception as e:
                st.error(f"Preview error: {e}")
        
        with tab2:
            st.markdown("**Generated DOT Code:**")
            # Editable DOT code area
            edited_dot_code = st.text_area(
                "Edit DOT code:",
                value=st.session_state.current_dot_code,
                height=250,
                key="dot_code_editor"
            )
            update_clicked = st.button("🔄 Update Flowchart", key="update_flowchart_btn")
            if update_clicked:
                st.session_state.current_dot_code = edited_dot_code
                st.success("Flowchart updated! Preview and downloads will use your changes.")
                st.rerun()
            st.code(st.session_state.current_dot_code, language='dot')
            if st.button("📋 Copy Code"):
                st.success("Code ready to copy!")
        
        with tab3:
            st.markdown("""
            <div class="download-container">
                <h4>📥 Download Your Flowchart</h4>
                <p>Choose your preferred format:</p>
                <div class="warning-msg" style="margin-top:1em;">
                    ⚠️ <strong>Note:</strong> Files are automatically deleted after 1 hour. Please save your flowchart .
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                # Generate files using your existing functions
                png_file = render_dot(st.session_state.current_dot_code, "png")
                pdf_file = render_dot(st.session_state.current_dot_code, "pdf")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    with open(png_file, "rb") as f:
                        st.download_button(
                            "🖼️ PNG Image",
                            f,
                            file_name="flowchart.png",
                            mime="image/png",
                            use_container_width=True
                        )
                
                with col_b:
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "📄 PDF Document",
                            f,
                            file_name="flowchart.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                
                # DOT file
                dot_file = save_dot_file(st.session_state.current_dot_code)
                with open(dot_file, "rb") as f:
                    st.download_button(
                        "📝 DOT Source Code",
                        f,
                        file_name="flowchart.dot",
                        mime="text/plain",
                        use_container_width=True
                    )
                        
            except Exception as e:
                st.error(f"Download preparation error: {e}")
    
    else:
        # Placeholder
        st.markdown("""
        <div style="
            background: #f8f9fa;
            border: 2px dashed #dee2e6;
            border-radius: 12px;
            padding: 3rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4>Flowchart Preview</h4>
            <p>Enter a description and generate to see your flowchart here</p>
        </div>
        """, unsafe_allow_html=True)

# Footer with additional information
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("""
    <div class="metric-container">
        <h4>🎯 Features</h4>
        <ul>
            <li>AI-powered flowchart generation</li>
            <li>Multiple export formats</li>
            <li>Real-time preview</li>
            <li>Customizable styling</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div class="metric-container">
        <h4>🚀 Powered By</h4>
        <ul>
            <li>LangChain for AI processing</li>
            <li>Graphviz for rendering</li>
            <li>Streamlit for interface</li>
            <li>Python ecosystem</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_f3:
    st.markdown("""
    <div class="metric-container">
        <h4>📈 Session Stats</h4>
        <p><strong>Flowcharts:</strong> {}</p>
        <p><strong>Characters:</strong> {}</p>
        <p><strong>Status:</strong> Ready</p>
        <hr>
        <h4>🔗 Connect with datascilearn</h4>
        <p style="font-size:1.3em;">
            <a href="https://youtube.com/@datascilearn" target="_blank" style="text-decoration:none; margin-right:10px;">
                <svg height="24" width="24" viewBox="0 0 24 24" style="vertical-align:middle;"><path fill="#FF0000" d="M23.498 6.186a2.994 2.994 0 0 0-2.112-2.112C19.413 3.5 12 3.5 12 3.5s-7.413 0-9.386.574A2.994 2.994 0 0 0 .502 6.186C0 8.159 0 12 0 12s0 3.841.502 5.814a2.994 2.994 0 0 0 2.112 2.112C4.587 20.5 12 20.5 12 20.5s7.413 0 9.386-.574a2.994 2.994 0 0 0 2.112-2.112C24 15.841 24 12 24 12s0-3.841-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
            <a href="https://instagram.com/datascilearn" target="_blank" style="text-decoration:none; margin-right:10px;">
                <svg height="24" width="24" viewBox="0 0 24 24" style="vertical-align:middle;"><path fill="#E1306C" d="M12 2.163c3.204 0 3.584.012 4.85.07 1.366.062 2.633.334 3.608 1.308.975.974 1.246 2.242 1.308 3.608.058 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.062 1.366-.334 2.633-1.308 3.608-.974.975-2.242 1.246-3.608 1.308-1.266.058-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.366-.062-2.633-.334-3.608-1.308-.975-.974-1.246-2.242-1.308-3.608C2.175 15.584 2.163 15.204 2.163 12s.012-3.584.07-4.85c.062-1.366.334-2.633 1.308-3.608C4.516 2.497 5.784 2.226 7.15 2.163 8.416 2.105 8.796 2.163 12 2.163zm0 1.838c-3.18 0-3.563.012-4.82.07-1.042.047-1.612.218-1.99.396-.378.178-.646.39-.924.668-.278.278-.49.546-.668.924-.178.378-.349.948-.396 1.99-.058 1.257-.07 1.64-.07 4.82s.012 3.563.07 4.82c.047 1.042.218 1.612.396 1.99.178.378.39.646.668.924.278.278.546.49.924.668.378.178.948.349 1.99.396 1.257.058 1.64.07 4.82.07s3.563-.012 4.82-.07c1.042-.047 1.612-.218 1.99-.396.378-.178.646-.39.924-.668.278-.278.49-.546.668-.924.178-.378.349-.948.396-1.99.058-1.257.07-1.64.07-4.82s-.012-3.563-.07-4.82c-.047-1.042-.218-1.612-.396-1.99-.178-.378-.39-.646-.668-.924-.278-.278-.546-.49-.924-.668-.378-.178-.948-.349-1.99-.396-1.257-.058-1.64-.07-4.82-.07zm0 3.838a5.002 5.002 0 1 0 0 10.004 5.002 5.002 0 0 0 0-10.004zm0 8.164a3.162 3.162 0 1 1 0-6.324 3.162 3.162 0 0 1 0 6.324zm6.406-8.406a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0z"/></svg>
            </a>
            <a href="https://www.linkedin.com/company/datascilearn" target="_blank" style="text-decoration:none;">
                <svg height="24" width="24" viewBox="0 0 24 24" style="vertical-align:middle;"><path fill="#0077B5" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.761 0 5-2.239 5-5v-14c0-2.761-2.239-5-5-5zm-11.75 20h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.25 11.268h-3v-5.604c0-1.337-.026-3.063-1.867-3.063-1.868 0-2.154 1.459-2.154 2.967v5.7h-3v-10h2.881v1.367h.041c.401-.761 1.379-1.563 2.838-1.563 3.036 0 3.6 2.001 3.6 4.601v5.595z"/></svg>
            </a>
        </p>
    </div>
    """.format(st.session_state.generation_count, st.session_state.total_chars), unsafe_allow_html=True)

