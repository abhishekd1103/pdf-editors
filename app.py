import streamlit as st
import fitz  # PyMuPDF
import pypdf
from io import BytesIO
import base64
from PIL import Image
import time
import uuid
import os
import tempfile

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="PDF Tools Hub - Professional PDF Editor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://your-domain.com/help',
        'Report a bug': 'https://your-domain.com/contact',
        'About': "PDF Tools Hub - Professional PDF editing made easy!"
    }
)

# ============================================================================
# CUSTOM CSS STYLING
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

        /* Main App Background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        /* Header Section */
        .main-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin: -70px -1rem 40px -1rem;
            padding: 25px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
            position: sticky;
            top: 0;
            z-index: 100;
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
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .tagline {
            font-size: 14px;
            color: #718096;
            font-weight: 500;
        }

        .nav-section {
            display: flex;
            gap: 30px;
            align-items: center;
        }

        .nav-item {
            color: #4a5568;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            padding: 8px 16px;
            border-radius: 8px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .nav-item:hover {
            color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }

        /* Workspace Container */
        .workspace {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 40px;
            margin: 30px auto;
            max-width: 1400px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }

        /* Upload Zone */
        .upload-zone {
            border: 3px dashed #667eea;
            border-radius: 20px;
            padding: 60px 40px;
            text-align: center;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
            margin: 30px 0;
            transition: all 0.3s ease;
        }

        .upload-zone:hover {
            border-color: #764ba2;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.12));
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 72px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }

        .upload-text {
            font-size: 24px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 12px;
        }

        .upload-subtext {
            color: #718096;
            font-size: 16px;
            font-weight: 500;
        }

        /* File Info Cards */
        .file-info-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }

        .file-info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.12);
        }

        .file-name {
            font-size: 18px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .file-stats {
            color: #718096;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            gap: 20px;
        }

        /* Position Selector */
        .position-selector {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            text-align: center;
        }

        .position-title {
            font-size: 24px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 25px;
        }

        .position-indicator {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            margin: 20px auto;
            display: inline-block;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        /* Action Buttons */
        .action-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 40px 0;
            flex-wrap: wrap;
        }

        .btn {
            padding: 16px 32px;
            font-weight: 700;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        .btn-success {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
            box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.9);
            color: #667eea;
            border: 2px solid #667eea;
            backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
            background: #667eea;
            color: white;
            transform: translateY(-3px);
        }

        /* Messages */
        .message {
            padding: 20px 25px;
            border-radius: 15px;
            margin: 25px 0;
            font-weight: 600;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .message-success {
            background: linear-gradient(135deg, rgba(72, 187, 120, 0.15), rgba(56, 161, 105, 0.15));
            border: 2px solid rgba(72, 187, 120, 0.3);
            color: #2f855a;
        }

        .message-error {
            background: linear-gradient(135deg, rgba(245, 101, 101, 0.15), rgba(229, 62, 62, 0.15));
            border: 2px solid rgba(245, 101, 101, 0.3);
            color: #c53030;
        }

        .message-info {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border: 2px solid rgba(102, 126, 234, 0.3);
            color: #553c9a;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 50px 30px;
            margin-top: 80px;
            background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            color: rgba(255, 255, 255, 0.8);
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
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }

        .footer-link:hover {
            color: white;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
                padding: 0 20px;
            }

            .nav-section {
                gap: 15px;
            }

            .workspace {
                padding: 25px;
                margin: 20px 10px;
            }

            .action-buttons {
                flex-direction: column;
                align-items: center;
            }

            .btn {
                width: 100%;
                max-width: 300px;
                justify-content: center;
            }

            .upload-zone {
                padding: 40px 20px;
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
        for page_num in range(min(len(doc), 20)):  # Limit to 20 pages for performance
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
        st.error(f"Error reading PDF: {str(e)}")
        return 0

def merge_pdfs_with_insert(main_pdf_bytes, insert_pdf_bytes, position):
    """Merge PDFs with insert at specific position"""
    try:
        main_reader = pypdf.PdfReader(BytesIO(main_pdf_bytes))
        insert_reader = pypdf.PdfReader(BytesIO(insert_pdf_bytes))
        writer = pypdf.PdfWriter()

        # Add pages before insertion point
        for i in range(position):
            if i < len(main_reader.pages):
                writer.add_page(main_reader.pages[i])

        # Add all pages from insert PDF
        for page in insert_reader.pages:
            writer.add_page(page)

        # Add remaining pages from main PDF
        for i in range(position, len(main_reader.pages)):
            writer.add_page(main_reader.pages[i])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def merge_all_pdfs(pdf_files):
    """Merge multiple PDF files in order"""
    try:
        writer = pypdf.PdfWriter()
        for file_data in pdf_files:
            reader = pypdf.PdfReader(BytesIO(file_data))
            for page in reader.pages:
                writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def create_download_link(file_bytes, filename):
    """Create download link for processed PDF"""
    b64 = base64.b64encode(file_bytes).decode()
    href = f"""
    <a href="data:application/pdf;base64,{b64}" download="{filename}" class="btn btn-success">
        📥 Download Merged PDF ({len(file_bytes) // 1024} KB)
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
    # Load custom CSS
    load_css()

    # Initialize session state
    if 'current_tool' not in st.session_state:
        st.session_state.current_tool = 'home'
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}

    # Header
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">📄 PDF Tools Hub</div>
                <div class="tagline">Professional PDF Solutions</div>
            </div>
            <div class="nav-section">
                <a href="#" class="nav-item">🏠 Home</a>
                <a href="#" class="nav-item">🔗 PDF Merger</a>
                <a href="#" class="nav-item">✂️ PDF Editor</a>
                <a href="#" class="nav-item">📊 Coming Soon</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main content based on current tool
    if st.session_state.current_tool == 'home':
        show_home_page()
    elif st.session_state.current_tool == 'merger':
        show_pdf_merger()

    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <h3 style="margin: 0 0 15px 0; font-weight: 700;">PDF Tools Hub</h3>
            <p style="margin: 0 0 20px 0; opacity: 0.8;">
                Professional PDF editing tools built with modern technology. 
                Fast, secure, and user-friendly.
            </p>
            <div class="footer-links">
                <a href="#" class="footer-link">Privacy Policy</a>
                <a href="#" class="footer-link">Terms of Service</a>
                <a href="#" class="footer-link">Contact Us</a>
                <a href="#" class="footer-link">Help Center</a>
            </div>
            <p style="margin: 20px 0 0 0; font-size: 14px; opacity: 0.6;">
                © 2025 PDF Tools Hub. Made with ❤️ using Streamlit.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_home_page():
    """Display the home page with tool selection"""
    st.markdown("""
    <div class="workspace">
        <div style="text-align: center; margin-bottom: 50px;">
            <h1 style="font-size: 48px; font-weight: 800; color: #2d3748; margin: 0 0 20px 0;">
                🚀 Professional PDF Tools
            </h1>
            <p style="font-size: 20px; color: #718096; font-weight: 500; max-width: 700px; margin: 0 auto; line-height: 1.6;">
                Upload, merge, edit, and manipulate your PDF files with our advanced tools. 
                Perfect for professionals, students, and businesses.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tool selection
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔗 Advanced PDF Merger", key="merger_btn", use_container_width=True):
            st.session_state.current_tool = 'merger'
            st.rerun()

    with col2:
        st.markdown("""
        <div style="padding: 30px; text-align: center; background: rgba(255,255,255,0.1); border-radius: 16px; margin: 10px 0;">
            <div style="font-size: 48px; margin-bottom: 15px;">✂️</div>
            <h3 style="color: #2d3748; margin-bottom: 10px;">PDF Editor Suite</h3>
            <p style="color: #718096; font-size: 14px;">Split, rotate, organize pages</p>
            <p style="color: #f59e0b; font-weight: 600; margin-top: 15px;">🚧 Coming Soon</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="padding: 30px; text-align: center; background: rgba(255,255,255,0.1); border-radius: 16px; margin: 10px 0;">
            <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
            <h3 style="color: #2d3748; margin-bottom: 10px;">Engineering Plotter</h3>
            <p style="color: #718096; font-size: 14px;">Technical diagrams & plots</p>
            <p style="color: #f59e0b; font-weight: 600; margin-top: 15px;">🚧 Coming Soon</p>
        </div>
        """, unsafe_allow_html=True)

def show_pdf_merger():
    """Display the PDF merger tool"""
    st.markdown("""
    <div class="workspace">
        <h1 style="font-size: 36px; font-weight: 800; color: #2d3748; margin: 0 0 30px 0;">
            🔗 Advanced PDF Merger
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.current_tool = 'home'
        st.session_state.uploaded_files = {}
        st.rerun()

    # File upload section
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📁</div>
        <div class="upload-text">Upload Your PDF Files</div>
        <div class="upload-subtext">
            Drag and drop multiple PDF files or click below to browse. Maximum 10 files, 50MB each.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choose PDF files to merge",
        type="pdf",
        accept_multiple_files=True,
        key="pdf_files",
        label_visibility="collapsed"
    )

    if uploaded_files:
        # Process files
        with st.spinner("📄 Processing uploaded files..."):
            for file in uploaded_files:
                if len(uploaded_files) > 10:
                    st.error("⚠️ Maximum 10 files allowed")
                    break

                file_size = len(file.read())
                file.seek(0)

                if file_size > 50 * 1024 * 1024:
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

        if st.session_state.uploaded_files:
            total_pages = sum(data['pages'] for data in st.session_state.uploaded_files.values())
            total_size = sum(data['size'] for data in st.session_state.uploaded_files.values())

            st.markdown(f"""
            <div class="message message-success">
                ✅ Successfully uploaded {len(st.session_state.uploaded_files)} PDF files 
                ({total_pages} total pages, {format_file_size(total_size)})
            </div>
            """, unsafe_allow_html=True)

            # Show file info
            for idx, (filename, data) in enumerate(st.session_state.uploaded_files.items()):
                st.markdown(f"""
                <div class="file-info-card">
                    <div class="file-name">📄 {filename}</div>
                    <div class="file-stats">
                        <span>📊 {data['pages']} pages</span>
                        <span>💾 {format_file_size(data['size'])}</span>
                        <span>🔢 File #{idx + 1}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Merge options
            if len(st.session_state.uploaded_files) >= 2:
                merge_option = st.radio(
                    "Choose merging method:",
                    ["📚 Simple Merge (All files in order)", "🎯 Advanced Merge (Insert at position)"],
                    key="merge_option"
                )

                if merge_option.startswith("📚"):
                    show_simple_merge()
                else:
                    show_advanced_merge()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 30px; color: #718096;">
            <div style="font-size: 80px; margin-bottom: 25px; opacity: 0.6;">📁</div>
            <h3 style="color: #4a5568; font-weight: 700;">No PDF files uploaded</h3>
            <p>Upload multiple PDF files to start merging</p>
        </div>
        """, unsafe_allow_html=True)

def show_simple_merge():
    """Show simple merge interface"""
    st.markdown("**📋 Merge Order:**")
    for idx, filename in enumerate(st.session_state.uploaded_files.keys()):
        st.markdown(f"**{idx + 1}.** {filename}")

    if st.button("🔗 Merge All PDFs", key="merge_all_btn"):
        with st.spinner("🔄 Merging PDFs..."):
            progress_bar = st.progress(0)
            file_data_list = [data['bytes'] for data in st.session_state.uploaded_files.values()]

            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress((i + 1) / 100)

            merged_pdf = merge_all_pdfs(file_data_list)

            if merged_pdf:
                st.markdown("""
                <div class="message message-success">
                    🎉 PDFs merged successfully!
                </div>
                """, unsafe_allow_html=True)

                download_link = create_download_link(merged_pdf, f"merged_all_{int(time.time())}.pdf")
                st.markdown(download_link, unsafe_allow_html=True)

def show_advanced_merge():
    """Show advanced merge interface"""
    files_list = list(st.session_state.uploaded_files.keys())

    col1, col2 = st.columns(2)
    with col1:
        main_pdf = st.selectbox("🎯 Main PDF:", files_list, key="main_pdf")
    with col2:
        insert_options = [f for f in files_list if f != main_pdf]
        if insert_options:
            insert_pdf = st.selectbox("📥 Insert PDF:", insert_options, key="insert_pdf")
        else:
            st.warning("Need at least 2 PDFs")
            return

    if main_pdf and insert_pdf:
        # Show previews
        tab1, tab2 = st.tabs([f"📄 {main_pdf}", f"📥 {insert_pdf}"])

        with tab1:
            main_images, _ = pdf_to_images(st.session_state.uploaded_files[main_pdf]['bytes'], main_pdf)
            if main_images:
                cols = st.columns(3)
                for idx, img in enumerate(main_images[:6]):
                    with cols[idx % 3]:
                        st.image(img, caption=f"Page {idx + 1}")

        with tab2:
            insert_images, _ = pdf_to_images(st.session_state.uploaded_files[insert_pdf]['bytes'], insert_pdf)
            if insert_images:
                cols = st.columns(3)
                for idx, img in enumerate(insert_images[:6]):
                    with cols[idx % 3]:
                        st.image(img, caption=f"Page {idx + 1}")

        # Position selector
        main_pages = st.session_state.uploaded_files[main_pdf]['pages']
        position = st.slider("Insert after page:", 0, main_pages, main_pages, key="position")

        st.markdown(f"""
        <div class="position-indicator">
            📍 Insert after page {position} of {main_pages}
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔗 Insert & Merge", key="merge_insert_btn"):
            with st.spinner("🔄 Merging with insertion..."):
                merged_pdf = merge_pdfs_with_insert(
                    st.session_state.uploaded_files[main_pdf]['bytes'],
                    st.session_state.uploaded_files[insert_pdf]['bytes'],
                    position
                )

                if merged_pdf:
                    st.markdown("""
                    <div class="message message-success">
                        🎉 PDFs merged successfully with insertion!
                    </div>
                    """, unsafe_allow_html=True)

                    download_link = create_download_link(merged_pdf, f"merged_insert_{int(time.time())}.pdf")
                    st.markdown(download_link, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
