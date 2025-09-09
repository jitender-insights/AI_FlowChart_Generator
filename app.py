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

# Simplified CSS that doesn't interfere with functionality
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
            st.code(st.session_state.current_dot_code, language='dot')
            
            if st.button("📋 Copy Code"):
                st.success("Code ready to copy!")
        
        with tab3:
            st.markdown("""
            <div class="download-container">
                <h4>📥 Download Your Flowchart</h4>
                <p>Choose your preferred format:</p>
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
    </div>
    """.format(st.session_state.generation_count, st.session_state.total_chars), unsafe_allow_html=True)

# Add some JavaScript for enhanced interactions (optional)
st.markdown("""
<script>
// Add any custom JavaScript here for enhanced interactions
document.addEventListener('DOMContentLoaded', function() {
    // Custom animations or interactions can be added here
});
</script>
""", unsafe_allow_html=True)
