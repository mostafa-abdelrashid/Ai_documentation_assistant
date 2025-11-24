import streamlit as st
import requests
import os
from dotenv import load_dotenv
import tempfile

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")

# --- Page Setup ---
st.set_page_config(
    page_title="AI Documentation Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("About AI Documentation Assistant")
st.sidebar.info(
    """
    This assistant helps you automatically generate **code analysis**, **architecture overview**, and **documentation** from your code or prompt.

    **Tabs:**
    - 📝 **Analysis**: Purpose, key components, dependencies, and configuration.
    - 🏗️ **Architecture**: Design patterns, components, data flow, and design details.
    - 📄 **Documentation**: Markdown documentation preview and copyable raw code.
    """
)

# --- Main Title ---
st.title("🤖 AI Documentation Assistant")
st.markdown(
    "Generate code analysis, architecture overview, and markdown documentation automatically.\n\n"
    "Paste your code or write a prompt below and click **Generate Documentation**."
)

# --- Centered Prompt Input ---
prompt = st.text_area(
    "Enter your code or prompt:",
    height=250,
    placeholder="Paste your code here or write a prompt to generate documentation..."
)
generate_btn = st.button("Generate Documentation")

# Initialize session state to store results
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None

# --- Generate and Display Results ---
if generate_btn and prompt:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"prompt": prompt}

    with st.spinner("Generating..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            analysis, arch, doc = data.get("response", ())
            
            # Store results in session state
            st.session_state.generated_data = {
                "analysis": analysis,
                "arch": arch,
                "doc": doc
            }
            
        except requests.HTTPError as e:
            st.error(f"HTTP error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# Display results if they exist in session state
if st.session_state.generated_data:
    analysis = st.session_state.generated_data["analysis"]
    arch = st.session_state.generated_data["arch"]
    doc = st.session_state.generated_data["doc"]

    # --- Tabs Layout ---
    tab1, tab2, tab3 = st.tabs(["📝 Analysis", "🏗️ Architecture", "📄 Documentation"])

    # ----- Analysis Tab -----
    with tab1:
        st.header("Analysis")
        st.info("Overview of code purpose and key details.")
        with st.expander("Purpose", expanded=True):
            st.write(analysis.get("purpose"))
        with st.expander("Key Components", expanded=True):
            st.write(analysis.get("key_components"))
        with st.expander("Dependencies", expanded=True):
            st.write(analysis.get("dependencies"))
        with st.expander("Configuration", expanded=True):
            st.write(analysis.get("config"))

    # ----- Architecture Tab -----
    with tab2:
        st.header("Architecture")
        st.info("Design patterns, components, and data flow.")
        with st.expander("Pattern", expanded=True):
            st.write(arch.get("pattern"))
        with st.expander("Components", expanded=True):
            st.write(arch.get("components"))
        with st.expander("Data Flow", expanded=True):
            st.write(arch.get("data_flow"))
        with st.expander("Design", expanded=True):
            st.write(arch.get("design"))


# ----- Documentation Tab -----
    with tab3:
        st.header("Documentation")
        st.info("Generated markdown documentation.")

        # Raw markdown code (collapsed by default)
        with st.expander("Markdown Code (click to copy)", expanded=False):
            st.code(doc.get("markdown"), language="markdown")

        # Markdown preview displayed normally
        st.subheader("Preview")
        st.markdown(doc.get("markdown"))

        # --- PDF Download ---
        st.subheader("Download")
        
        # Create PDF download functionality
        try:
            from weasyprint import HTML
            import markdown
            
            # Convert markdown to proper HTML
            markdown_content = doc.get("markdown", "")
            html_content = markdown.markdown(markdown_content)
            
            # Create styled HTML document
            full_html_content = f"""<html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Arial', 'Helvetica', sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 5px;
            }}
            h3 {{
                color: #46627f;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 2px 6px;
                border-radius: 3px;
                border: 1px solid #e9ecef;
                font-family: 'Courier New', monospace;
                color: #e83e8c;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #e9ecef;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                line-height: 1.4;
            }}
            blockquote {{
                border-left: 4px solid #2c3e50;
                padding-left: 15px;
                margin-left: 0;
                color: #7f8c8d;
                font-style: italic;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_content}
        </div>
    </body>
    </html>"""
            
            # Generate PDF
            pdf_file = HTML(string=full_html_content).write_pdf()
            
            # Create download button
            st.download_button(
                label="📥 Download Documentation as PDF",
                data=pdf_file,
                file_name="documentation.pdf",
                mime="application/pdf",
                key="pdf_download"
            )
            
        except ImportError as e:
            st.error(f"Required library not installed: {e}. Please install using: pip install weasyprint markdown")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")