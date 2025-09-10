import streamlit as st
import fitz  # PyMuPDF
import pypdf
from io import BytesIO
import base64
from PIL import Image
import time
import uuid
import zipfile
import tempfile
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="PDF Tools Hub - Professional PDF Suite",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PROFESSIONAL CSS STYLING
# ============================================================================
def load_css():
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global Styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}

        /* Professional Color Scheme */
        :root {
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            --primary-color: #6366f1;
            --secondary-color: #8b5cf6;
            --accent-color: #06b6d4;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --dark-bg: #0f172a;
            --dark-card: #1e293b;
            --light-card: rgba(255, 255, 255, 0.95);
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: rgba(99, 102, 241, 0.2);
        }

        /* Main App Background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            min-height: 100vh;
        }

        /* Header Section */
        .main-header {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-color);
            margin: -70px -1rem 30px -1rem;
            padding: 20px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo {
            font-size: 28px;
            font-weight: 800;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .tagline {
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .nav-section {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .nav-item {
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            padding: 12px 20px;
            border-radius: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: rgba(99, 102, 241, 0.05);
            border: 1px solid transparent;
        }

        .nav-item:hover {
            background: var(--primary-gradient);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .nav-item.active {
            background: var(--primary-gradient);
            color: white;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        /* Tool Cards Grid */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin: 40px 0;
            padding: 0 20px;
        }

        .tool-card {
            background: var(--light-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 35px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .tool-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.6s;
        }

        .tool-card:hover::before {
            left: 100%;
        }

        .tool-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            border-color: var(--primary-color);
        }

        .tool-icon {
            font-size: 60px;
            margin-bottom: 25px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .tool-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 15px;
        }

        .tool-description {
            color: var(--text-secondary);
            font-size: 15px;
            line-height: 1.6;
            font-weight: 500;
        }

        .tool-status {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 15px;
        }

        .status-available {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }

        .status-coming {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
        }

        /* Workspace Container */
        .workspace {
            background: var(--light-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 40px;
            margin: 30px 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        }

        /* Upload Zone */
        .upload-zone {
            border: 3px dashed var(--primary-color);
            border-radius: 20px;
            padding: 50px 30px;
            text-align: center;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
            margin: 30px 0;
            transition: all 0.3s ease;
            position: relative;
        }

        .upload-zone:hover {
            border-color: var(--secondary-color);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 64px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }

        .upload-text {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 10px;
        }

        .upload-subtext {
            color: var(--text-secondary);
            font-size: 15px;
            font-weight: 500;
        }

        /* Mode Selection */
        .mode-selection {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
        }

        .mode-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 20px;
            text-align: center;
        }

        .mode-options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .mode-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .mode-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
        }

        .mode-card.selected {
            border-color: var(--primary-color);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
        }

        .mode-icon {
            font-size: 40px;
            margin-bottom: 15px;
        }

        .mode-card-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .mode-card-desc {
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* PDF Grid Layout */
        .pdf-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
            padding: 20px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.02), rgba(139, 92, 246, 0.02));
            border-radius: 20px;
            border: 1px solid var(--border-color);
        }

        .pdf-page-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 15px;
            text-align: center;
            cursor: move;
            transition: all 0.3s ease;
            position: relative;
            user-select: none;
        }

        .pdf-page-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15);
        }

        .pdf-page-card.selected {
            border-color: var(--primary-color);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3);
        }

        .page-thumbnail {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .page-info {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .page-number {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--primary-gradient);
            color: white;
            padding: 6px 10px;
            border-radius: 15px;
            font-size: 11px;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        .pdf-source-badge {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 600;
        }

        /* File Info Cards */
        .file-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }

        .file-info-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
            backdrop-filter: blur(15px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 25px;
            transition: all 0.3s ease;
        }

        .file-info-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
        }

        .file-name {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .file-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }

        .file-stat {
            text-align: center;
            padding: 12px;
            background: rgba(99, 102, 241, 0.05);
            border-radius: 12px;
        }

        .file-stat-value {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary-color);
        }

        .file-stat-label {
            font-size: 11px;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
        }

        /* Action Buttons */
        .action-section {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            text-align: center;
        }

        .action-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }

        .btn {
            padding: 16px 32px;
            font-weight: 700;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            font-size: 15px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            min-width: 180px;
            justify-content: center;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn-primary {
            background: var(--primary-gradient);
            color: white;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(99, 102, 241, 0.4);
        }

        .btn-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        }

        .btn-warning {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.9);
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
            backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
            background: var(--primary-gradient);
            color: white;
            transform: translateY(-3px);
        }

        /* Messages */
        .message {
            padding: 20px 25px;
            border-radius: 16px;
            margin: 25px 0;
            font-weight: 600;
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            backdrop-filter: blur(10px);
        }

        .message-success {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15));
            border: 2px solid rgba(16, 185, 129, 0.3);
            color: #065f46;
        }

        .message-error {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.15));
            border: 2px solid rgba(239, 68, 68, 0.3);
            color: #991b1b;
        }

        .message-info {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15));
            border: 2px solid rgba(99, 102, 241, 0.3);
            color: #3730a3;
        }

        .message-warning {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.15));
            border: 2px solid rgba(245, 158, 11, 0.3);
            color: #92400e;
        }

        /* Organization Controls */
        .organization-controls {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
        }

        .controls-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 20px;
            text-align: center;
        }

        .control-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .control-btn {
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 25px;
            border: 2px solid var(--border-color);
            background: white;
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .control-btn:hover {
            border-color: var(--primary-color);
            background: var(--primary-gradient);
            color: white;
            transform: translateY(-2px);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 50px 30px;
            margin-top: 80px;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            color: rgba(255, 255, 255, 0.8);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .footer-content {
            max-width: 800px;
            margin: 0 auto;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .footer-link {
            color: rgba(255, 255, 255, 0.6);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            padding: 8px 16px;
            border-radius: 8px;
        }

        .footer-link:hover {
            color: white;
            background: rgba(99, 102, 241, 0.2);
        }

        /* Responsive Design */
        @media (max-width: 1024px) {
            .mode-options {
                grid-template-columns: 1fr;
            }

            .pdf-grid {
                grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            }
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
                padding: 0 20px;
            }

            .nav-section {
                gap: 10px;
            }

            .nav-item {
                padding: 10px 16px;
                font-size: 12px;
            }

            .workspace {
                padding: 25px;
                margin: 20px 10px;
            }

            .tools-grid {
                grid-template-columns: 1fr;
                padding: 0 10px;
            }

            .pdf-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
            }

            .action-buttons {
                flex-direction: column;
                align-items: center;
            }

            .btn {
                width: 100%;
                max-width: 300px;
            }

            .file-info-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def pdf_to_images(file_bytes, file_name):
    """Convert PDF to list of PIL Images with caching"""
    try:
        images = []
        doc = fitz.open("pdf", file_bytes)
        for page_num in range(min(len(doc), 30)):  # Limit for performance
            pix = doc[page_num].get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_bytes = pix.tobytes("png")
            img = Image.open(BytesIO(img_bytes))
            images.append(img)
        doc.close()
        return images, len(doc)
    except Exception as e:
        st.error(f"Error converting {file_name} to images: {str(e)}")
        return [], 0

def get_pdf_page_count(file_bytes):
    """Get number of pages in PDF"""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        return len(reader.pages)
    except Exception as e:
        return 0

def merge_pdfs_organized(pdf_data_list, page_order):
    """Merge PDFs with custom page organization"""
    try:
        writer = pypdf.PdfWriter()

        for file_key, page_num in page_order:
            if file_key in pdf_data_list:
                reader = pypdf.PdfReader(BytesIO(pdf_data_list[file_key]['bytes']))
                if page_num - 1 < len(reader.pages):
                    writer.add_page(reader.pages[page_num - 1])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def merge_pdfs_plain(pdf_data_list):
    """Simple merge of all PDFs in order"""
    try:
        writer = pypdf.PdfWriter()

        for file_data in pdf_data_list.values():
            reader = pypdf.PdfReader(BytesIO(file_data['bytes']))
            for page in reader.pages:
                writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def remove_pages_from_pdf(file_bytes, pages_to_remove):
    """Remove specified pages from PDF"""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        writer = pypdf.PdfWriter()

        for i in range(len(reader.pages)):
            if (i + 1) not in pages_to_remove:
                writer.add_page(reader.pages[i])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error removing pages: {str(e)}")
        return None

def split_pdf_to_pages(file_bytes, filename):
    """Split PDF into individual pages and create ZIP"""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))

        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, page in enumerate(reader.pages):
                writer = pypdf.PdfWriter()
                writer.add_page(page)

                page_buffer = BytesIO()
                writer.write(page_buffer)
                page_buffer.seek(0)

                page_filename = f"{filename}_page_{i+1:03d}.pdf"
                zip_file.writestr(page_filename, page_buffer.getvalue())

        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except Exception as e:
        st.error(f"Error splitting PDF: {str(e)}")
        return None

def create_download_link(file_bytes, filename, link_text):
    """Create download link for processed files"""
    b64 = base64.b64encode(file_bytes).decode()
    file_size = len(file_bytes) // 1024
    href = f"""
    <a href="data:application/octet-stream;base64,{b64}" download="{filename}" class="btn btn-success">
        {link_text} ({file_size} KB)
    </a>
    """
    return href

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    load_css()

    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    if 'selected_pages' not in st.session_state:
        st.session_state.selected_pages = []

    # Header
    render_header()

    # Page routing
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'pdf_merge':
        show_pdf_merge_page()
    elif st.session_state.current_page == 'pdf_editor':
        show_pdf_editor_page()
    elif st.session_state.current_page == 'page_remove':
        show_page_remove_tool()
    elif st.session_state.current_page == 'pdf_split':
        show_pdf_split_tool()
    elif st.session_state.current_page == 'coming_soon':
        show_coming_soon_page()

    # Footer
    render_footer()

def render_header():
    """Render the main navigation header"""
    current_page = st.session_state.current_page

    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">📄 PDF Tools Hub</div>
                <div class="tagline">Professional PDF Suite</div>
            </div>
            <div class="nav-section">
                <a href="#" class="nav-item {'active' if current_page == 'home' else ''}" onclick="setPage('home')">🏠 Home</a>
                <a href="#" class="nav-item {'active' if current_page == 'pdf_merge' else ''}" onclick="setPage('pdf_merge')">🔗 PDF Merge</a>
                <a href="#" class="nav-item {'active' if current_page == 'pdf_editor' else ''}" onclick="setPage('pdf_editor')">✂️ PDF Editor</a>
                <a href="#" class="nav-item {'active' if current_page == 'coming_soon' else ''}" onclick="setPage('coming_soon')">📊 More Tools</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_home_page():
    """Display the home page with all tools"""
    st.markdown("""
    <div class="workspace">
        <div style="text-align: center; margin-bottom: 50px;">
            <h1 style="font-size: 48px; font-weight: 800; background: var(--primary-gradient); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       margin: 0 0 20px 0;">
                🚀 Professional PDF Tools Suite
            </h1>
            <p style="font-size: 20px; color: var(--text-secondary); font-weight: 500; 
                      max-width: 700px; margin: 0 auto; line-height: 1.6;">
                Complete PDF management solution with advanced features for professionals, 
                students, and businesses. Fast, secure, and user-friendly.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tools grid
    tools = [
        {
            'id': 'pdf_merge',
            'icon': '🔗',
            'title': 'PDF Merge',
            'description': 'Combine multiple PDFs with Plain or Organize modes. Advanced page positioning and live preview.',
            'status': 'available'
        },
        {
            'id': 'pdf_editor',
            'title': 'PDF Editor Suite',
            'icon': '✂️',
            'description': 'Complete PDF editing toolkit: merge, remove pages, split PDFs, and organize documents.',
            'status': 'available'
        },
        {
            'id': 'page_remove',
            'icon': '🗑️',
            'title': 'Page Removal',
            'description': 'Remove unwanted pages from your PDFs with precision. Batch selection and live preview.',
            'status': 'available'
        },
        {
            'id': 'pdf_split',
            'icon': '📑',
            'title': 'PDF Splitter',
            'description': 'Split PDFs into individual pages or create ZIP archives. Perfect for document organization.',
            'status': 'available'
        },
        {
            'id': 'coming_soon',
            'icon': '📊',
            'title': 'Engineering Plotter',
            'description': 'Create professional electrical diagrams, circuit schematics, and technical plots.',
            'status': 'coming'
        },
        {
            'id': 'coming_soon',
            'icon': '⚡',
            'title': 'Power Studies',
            'description': 'Advanced power system analysis, transient studies, and electrical engineering tools.',
            'status': 'coming'
        }
    ]

    st.markdown('<div class="tools-grid">', unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, tool in enumerate(tools):
        with cols[idx % 3]:
            if st.button(f"{tool['icon']} {tool['title']}", key=f"tool_{tool['id']}_{idx}", use_container_width=True):
                st.session_state.current_page = tool['id']
                st.rerun()

            status_class = 'status-available' if tool['status'] == 'available' else 'status-coming'
            status_text = 'Available Now' if tool['status'] == 'available' else 'Coming Soon'

            st.markdown(f"""
            <div class="tool-card">
                <div class="tool-icon">{tool['icon']}</div>
                <div class="tool-title">{tool['title']}</div>
                <div class="tool-description">{tool['description']}</div>
                <div class="tool-status {status_class}">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def show_pdf_merge_page():
    """Display the PDF merge tool with Plain and Organize modes"""
    st.markdown("""
    <div class="workspace">
        <h1 style="font-size: 36px; font-weight: 800; background: var(--primary-gradient); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 30px 0;">
            🔗 Advanced PDF Merge
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Home", key="back_home"):
        st.session_state.current_page = 'home'
        st.session_state.uploaded_files = {}
        st.rerun()

    # File upload
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📁</div>
        <div class="upload-text">Upload Multiple PDF Files</div>
        <div class="upload-subtext">
            Drag and drop up to 10 PDF files or click below to browse. Maximum 50MB each.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        key="pdf_merge_files",
        label_visibility="collapsed"
    )

    if uploaded_files:
        process_uploaded_files(uploaded_files)

        if st.session_state.uploaded_files:
            show_merge_modes()
    else:
        show_empty_state("Upload PDF files to start merging")

def show_merge_modes():
    """Show merge mode selection and processing"""
    st.markdown("""
    <div class="mode-selection">
        <div class="mode-title">🎯 Choose Merge Method</div>
    </div>
    """, unsafe_allow_html=True)

    # Mode selection
    col1, col2 = st.columns(2)

    with col1:
        plain_selected = st.button(
            "📚 Plain Merge", 
            key="plain_mode", 
            use_container_width=True,
            help="Merge all PDFs in upload order"
        )

        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">📚</div>
            <div class="mode-card-title">Plain Merge</div>
            <div class="mode-card-desc">
                Simple merge in upload order. Fast and straightforward 
                for basic document combination.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        organize_selected = st.button(
            "🎯 Organize Mode", 
            key="organize_mode", 
            use_container_width=True,
            help="Advanced organization with page-level control"
        )

        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🎯</div>
            <div class="mode-card-title">Organize Mode</div>
            <div class="mode-card-desc">
                Advanced page organization. Rearrange, select, and 
                customize the exact order of pages.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Show file info
    show_uploaded_files_info()

    # Process based on selection
    if plain_selected:
        process_plain_merge()
    elif organize_selected:
        show_organize_interface()

def show_organize_interface():
    """Show advanced organization interface with page grid"""
    st.markdown("""
    <div class="workspace">
        <h2 style="color: var(--text-primary); font-size: 24px; margin-bottom: 25px; font-weight: 700;">
            🎯 Organize Pages - Drag & Drop Style Interface
        </h2>
        <p style="color: var(--text-secondary); margin-bottom: 30px; font-size: 15px;">
            Click on pages to select/deselect them. Selected pages will be included in the merged document in the order shown.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Generate all pages from all PDFs
    all_pages = []
    for filename, file_data in st.session_state.uploaded_files.items():
        images, total_pages = pdf_to_images(file_data['bytes'], filename)
        for page_idx, image in enumerate(images):
            all_pages.append({
                'filename': filename,
                'page_num': page_idx + 1,
                'image': image,
                'key': f"{filename}_page_{page_idx + 1}"
            })

    if all_pages:
        # Organization controls
        st.markdown("""
        <div class="organization-controls">
            <div class="controls-title">📋 Organization Controls</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("✅ Select All", key="select_all"):
                st.session_state.selected_pages = [page['key'] for page in all_pages]
                st.rerun()

        with col2:
            if st.button("❌ Deselect All", key="deselect_all"):
                st.session_state.selected_pages = []
                st.rerun()

        with col3:
            if st.button("🔄 Reset Order", key="reset_order"):
                st.session_state.selected_pages = [page['key'] for page in all_pages]
                st.rerun()

        with col4:
            selected_count = len(st.session_state.selected_pages)
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: var(--primary-gradient); 
                        color: white; border-radius: 25px; font-weight: 700;">
                📊 {selected_count} Pages Selected
            </div>
            """, unsafe_allow_html=True)

        # Pages grid
        st.markdown('<div class="pdf-grid">', unsafe_allow_html=True)

        cols = st.columns(4)
        for idx, page_data in enumerate(all_pages):
            with cols[idx % 4]:
                page_key = page_data['key']
                is_selected = page_key in st.session_state.selected_pages

                # Page selection button
                if st.button(
                    f"{'✅' if is_selected else '⭕'} Select", 
                    key=f"select_{page_key}_{idx}",
                    use_container_width=True
                ):
                    if is_selected:
                        st.session_state.selected_pages.remove(page_key)
                    else:
                        st.session_state.selected_pages.append(page_key)
                    st.rerun()

                # Page card
                card_class = "pdf-page-card selected" if is_selected else "pdf-page-card"

                st.markdown(f"""
                <div class="{card_class}">
                    <div class="pdf-source-badge">{page_data['filename'][:8]}...</div>
                    <div class="page-number">{page_data['page_num']}</div>
                """, unsafe_allow_html=True)

                st.image(
                    page_data['image'], 
                    use_column_width=True,
                    caption=f"Page {page_data['page_num']}"
                )

                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Merge selected pages
        if st.session_state.selected_pages:
            st.markdown("""
            <div class="action-section">
                <h3 style="margin: 0 0 20px 0; font-weight: 700; color: var(--text-primary);">
                    🚀 Ready to Merge Selected Pages
                </h3>
                <p style="color: var(--text-secondary); margin-bottom: 0;">
                    Click below to merge the selected pages in the current order.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔗 Merge Selected Pages", key="merge_organized", use_container_width=True):
                process_organized_merge()

def process_plain_merge():
    """Process simple plain merge"""
    st.markdown("""
    <div class="action-section">
        <h3 style="margin: 0 0 20px 0; font-weight: 700; color: var(--text-primary);">
            📚 Plain Merge - All Files in Order
        </h3>
        <p style="color: var(--text-secondary); margin-bottom: 30px;">
            All PDF files will be merged in the order they were uploaded.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔗 Merge All PDFs", key="merge_plain_btn", use_container_width=True):
        with st.spinner("🔄 Merging PDFs..."):
            progress_bar = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress((i + 1) / 100)

            merged_pdf = merge_pdfs_plain(st.session_state.uploaded_files)

            if merged_pdf:
                st.markdown("""
                <div class="message message-success">
                    🎉 PDFs merged successfully! Your document is ready for download.
                </div>
                """, unsafe_allow_html=True)

                timestamp = int(time.time())
                download_link = create_download_link(
                    merged_pdf, 
                    f"merged_plain_{timestamp}.pdf",
                    "📥 Download Merged PDF"
                )
                st.markdown(download_link, unsafe_allow_html=True)

def process_organized_merge():
    """Process organized merge with selected pages"""
    with st.spinner("🔄 Merging selected pages..."):
        progress_bar = st.progress(0)

        # Build page order from selection
        page_order = []
        for page_key in st.session_state.selected_pages:
            filename, page_part = page_key.split('_page_')
            page_num = int(page_part)
            page_order.append((filename, page_num))

        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress((i + 1) / 100)

        merged_pdf = merge_pdfs_organized(st.session_state.uploaded_files, page_order)

        if merged_pdf:
            st.markdown("""
            <div class="message message-success">
                🎉 Selected pages merged successfully! Your organized document is ready.
            </div>
            """, unsafe_allow_html=True)

            timestamp = int(time.time())
            download_link = create_download_link(
                merged_pdf, 
                f"merged_organized_{timestamp}.pdf",
                "📥 Download Organized PDF"
            )
            st.markdown(download_link, unsafe_allow_html=True)

            st.info(f"📊 Final document contains {len(st.session_state.selected_pages)} pages")

def show_pdf_editor_page():
    """Display PDF Editor suite with multiple tools"""
    st.markdown("""
    <div class="workspace">
        <h1 style="font-size: 36px; font-weight: 800; background: var(--primary-gradient); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 30px 0;">
            ✂️ PDF Editor Suite
        </h1>
        <p style="color: var(--text-secondary); font-size: 16px; margin-bottom: 40px;">
            Complete PDF editing toolkit with advanced features for document management.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Home", key="back_editor"):
        st.session_state.current_page = 'home'
        st.rerun()

    # Editor tools
    st.markdown('<div class="tools-grid">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔗 PDF Merge", key="editor_merge", use_container_width=True):
            st.session_state.current_page = 'pdf_merge'
            st.rerun()

        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🔗</div>
            <div class="tool-title">PDF Merge</div>
            <div class="tool-description">
                Combine PDFs with Plain or Organize modes. 
                Advanced page positioning and live preview.
            </div>
            <div class="tool-status status-available">Available</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🗑️ Page Remove", key="editor_remove", use_container_width=True):
            st.session_state.current_page = 'page_remove'
            st.rerun()

        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🗑️</div>
            <div class="tool-title">Page Remove</div>
            <div class="tool-description">
                Remove unwanted pages from PDFs with precision. 
                Batch selection and live preview.
            </div>
            <div class="tool-status status-available">Available</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("📑 Split PDF", key="editor_split", use_container_width=True):
            st.session_state.current_page = 'pdf_split'
            st.rerun()

        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📑</div>
            <div class="tool-title">Split PDF</div>
            <div class="tool-description">
                Split PDFs into individual pages or create 
                ZIP archives for easy sharing.
            </div>
            <div class="tool-status status-available">Available</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def show_page_remove_tool():
    """Show page removal tool"""
    st.markdown("""
    <div class="workspace">
        <h1 style="font-size: 36px; font-weight: 800; background: var(--primary-gradient); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 30px 0;">
            🗑️ Page Removal Tool
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to PDF Editor", key="back_remove"):
        st.session_state.current_page = 'pdf_editor'
        st.rerun()

    # Single file upload for page removal
    uploaded_file = st.file_uploader(
        "Upload PDF to remove pages from",
        type="pdf",
        key="remove_file"
    )

    if uploaded_file:
        file_bytes = uploaded_file.read()
        images, total_pages = pdf_to_images(file_bytes, uploaded_file.name)

        st.success(f"✅ Loaded {uploaded_file.name} with {total_pages} pages")

        # Page selection for removal
        if images:
            st.markdown("""
            <div class="workspace">
                <h3 style="color: var(--text-primary); margin-bottom: 20px;">
                    Select Pages to Remove
                </h3>
            </div>
            """, unsafe_allow_html=True)

            # Initialize selected pages for removal
            if 'pages_to_remove' not in st.session_state:
                st.session_state.pages_to_remove = []

            # Control buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("❌ Clear Selection", key="clear_remove"):
                    st.session_state.pages_to_remove = []
                    st.rerun()

            with col2:
                remove_count = len(st.session_state.pages_to_remove)
                st.markdown(f"""
                <div style="text-align: center; padding: 12px; background: var(--error-color); 
                            color: white; border-radius: 25px; font-weight: 700;">
                    🗑️ {remove_count} Pages to Remove
                </div>
                """, unsafe_allow_html=True)

            # Pages grid for selection
            cols = st.columns(4)
            for idx, image in enumerate(images):
                with cols[idx % 4]:
                    page_num = idx + 1
                    is_selected = page_num in st.session_state.pages_to_remove

                    if st.button(
                        f"{'🗑️' if is_selected else '📄'} Page {page_num}", 
                        key=f"remove_page_{page_num}",
                        use_container_width=True
                    ):
                        if is_selected:
                            st.session_state.pages_to_remove.remove(page_num)
                        else:
                            st.session_state.pages_to_remove.append(page_num)
                        st.rerun()

                    # Visual feedback
                    if is_selected:
                        st.markdown("""
                        <div style="border: 3px solid var(--error-color); border-radius: 10px; padding: 5px;">
                        """, unsafe_allow_html=True)

                    st.image(image, caption=f"Page {page_num}", use_column_width=True)

                    if is_selected:
                        st.markdown('</div>', unsafe_allow_html=True)

            # Process removal
            if st.session_state.pages_to_remove:
                if st.button("🗑️ Remove Selected Pages", key="process_remove"):
                    with st.spinner("Removing selected pages..."):
                        result_pdf = remove_pages_from_pdf(file_bytes, st.session_state.pages_to_remove)

                        if result_pdf:
                            st.success(f"✅ Removed {len(st.session_state.pages_to_remove)} pages successfully!")

                            download_link = create_download_link(
                                result_pdf,
                                f"{uploaded_file.name.replace('.pdf', '_removed.pdf')}",
                                "📥 Download PDF (Pages Removed)"
                            )
                            st.markdown(download_link, unsafe_allow_html=True)

def show_pdf_split_tool():
    """Show PDF splitting tool"""
    st.markdown("""
    <div class="workspace">
        <h1 style="font-size: 36px; font-weight: 800; background: var(--primary-gradient); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 30px 0;">
            📑 PDF Splitter
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to PDF Editor", key="back_split"):
        st.session_state.current_page = 'pdf_editor'
        st.rerun()

    uploaded_file = st.file_uploader(
        "Upload PDF to split into pages",
        type="pdf",
        key="split_file"
    )

    if uploaded_file:
        file_bytes = uploaded_file.read()
        total_pages = get_pdf_page_count(file_bytes)

        st.success(f"✅ Loaded {uploaded_file.name} with {total_pages} pages")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background: var(--light-card); padding: 30px; border-radius: 16px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 15px;">📑</div>
                <h3>Split into Individual Pages</h3>
                <p>Create separate PDF file for each page</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📑 Split to Individual PDFs", key="split_individual"):
                with st.spinner("Splitting PDF into pages..."):
                    zip_data = split_pdf_to_pages(file_bytes, uploaded_file.name.replace('.pdf', ''))

                    if zip_data:
                        st.success(f"✅ Split into {total_pages} individual PDF files!")

                        download_link = create_download_link(
                            zip_data,
                            f"{uploaded_file.name.replace('.pdf', '_pages.zip')}",
                            f"📥 Download ZIP ({total_pages} PDFs)"
                        )
                        st.markdown(download_link, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: var(--light-card); padding: 30px; border-radius: 16px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
                <h3>Split by Page Range</h3>
                <p>Extract specific page ranges</p>
                <div style="color: var(--warning-color); font-weight: 600; margin-top: 15px;">
                    🚧 Coming Soon
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_coming_soon_page():
    """Show coming soon page for future tools"""
    st.markdown("""
    <div class="workspace">
        <div style="text-align: center; padding: 80px 30px;">
            <div style="font-size: 120px; margin-bottom: 30px;">🚧</div>
            <h1 style="font-size: 48px; font-weight: 800; background: var(--primary-gradient); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 20px 0;">
                More Amazing Tools Coming Soon!
            </h1>
            <p style="font-size: 18px; color: var(--text-secondary); max-width: 600px; margin: 0 auto 40px;">
                We're working hard to bring you more professional tools including Engineering Plotter, 
                Power System Studies, and Advanced Analytics.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Home", key="back_coming"):
        st.session_state.current_page = 'home'
        st.rerun()

    # Preview of coming tools
    upcoming_tools = [
        {
            'icon': '📊',
            'title': 'Engineering Plotter',
            'description': 'Professional electrical diagrams and technical plots',
            'eta': 'Phase 2 - Q1 2025'
        },
        {
            'icon': '⚡',
            'title': 'Power System Studies',
            'description': 'Advanced power analysis and transient studies',
            'eta': 'Phase 3 - Q2 2025'
        },
        {
            'icon': '📈',
            'title': 'Analytics Dashboard',
            'description': 'Document analytics and usage insights',
            'eta': 'Phase 4 - Q3 2025'
        }
    ]

    cols = st.columns(len(upcoming_tools))
    for col, tool in zip(cols, upcoming_tools):
        with col:
            st.markdown(f"""
            <div class="tool-card">
                <div class="tool-icon">{tool['icon']}</div>
                <div class="tool-title">{tool['title']}</div>
                <div class="tool-description">{tool['description']}</div>
                <div class="tool-status status-coming">{tool['eta']}</div>
            </div>
            """, unsafe_allow_html=True)

def process_uploaded_files(uploaded_files):
    """Process and validate uploaded files"""
    if len(uploaded_files) > 10:
        st.error("⚠️ Maximum 10 files allowed. Please select fewer files.")
        return

    with st.spinner("📄 Processing uploaded files..."):
        for file in uploaded_files:
            file_size = len(file.read())
            file.seek(0)

            if file_size > 50 * 1024 * 1024:  # 50MB limit
                st.error(f"⚠️ File {file.name} is too large (max 50MB)")
                continue

            if file.name not in st.session_state.uploaded_files:
                file_bytes = file.read()
                file.seek(0)

                st.session_state.uploaded_files[file.name] = {
                    'bytes': file_bytes,
                    'pages': get_pdf_page_count(file_bytes),
                    'size': file_size
                }

def show_uploaded_files_info():
    """Display information about uploaded files"""
    if st.session_state.uploaded_files:
        total_pages = sum(data['pages'] for data in st.session_state.uploaded_files.values())
        total_size = sum(data['size'] for data in st.session_state.uploaded_files.values())

        st.markdown(f"""
        <div class="message message-success">
            ✅ Successfully uploaded {len(st.session_state.uploaded_files)} PDF files 
            ({total_pages} total pages, {format_file_size(total_size)})
        </div>
        """, unsafe_allow_html=True)

        # File info grid
        st.markdown('<div class="file-info-grid">', unsafe_allow_html=True)

        for filename, data in st.session_state.uploaded_files.items():
            st.markdown(f"""
            <div class="file-info-card">
                <div class="file-name">📄 {filename}</div>
                <div class="file-stats">
                    <div class="file-stat">
                        <div class="file-stat-value">{data['pages']}</div>
                        <div class="file-stat-label">Pages</div>
                    </div>
                    <div class="file-stat">
                        <div class="file-stat-value">{format_file_size(data['size'])}</div>
                        <div class="file-stat-label">Size</div>
                    </div>
                    <div class="file-stat">
                        <div class="file-stat-value">PDF</div>
                        <div class="file-stat-label">Type</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def show_empty_state(message):
    """Show empty state with message"""
    st.markdown(f"""
    <div style="text-align: center; padding: 80px 30px; color: var(--text-secondary);">
        <div style="font-size: 80px; margin-bottom: 25px; opacity: 0.6;">📁</div>
        <h3 style="color: var(--text-primary); font-weight: 700;">{message}</h3>
        <p>Professional PDF tools at your fingertips</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render the footer"""
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <h3 style="margin: 0 0 15px 0; font-weight: 700;">PDF Tools Hub</h3>
            <p style="margin: 0 0 20px 0; opacity: 0.8;">
                Professional PDF solutions built with modern technology. 
                Fast, secure, and user-friendly for all your document needs.
            </p>
            <div class="footer-links">
                <a href="#" class="footer-link">Privacy Policy</a>
                <a href="#" class="footer-link">Terms of Service</a>
                <a href="#" class="footer-link">Contact Support</a>
                <a href="#" class="footer-link">Help Center</a>
                <a href="#" class="footer-link">API Documentation</a>
            </div>
            <p style="margin: 20px 0 0 0; font-size: 14px; opacity: 0.6;">
                © 2025 PDF Tools Hub. All rights reserved.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
