import streamlit as st
import fitz  # PyMuPDF
import pypdf
from io import BytesIO
import base64
from PIL import Image
import time
import re

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="PDF Tools Hub - Advanced PDF Merger",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PROFESSIONAL UI STYLING (Inspired by LightPDF)
# ============================================================================
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}

        /* Professional Color Palette */
        :root {
            --primary-blue: #4A90E2;
            --primary-green: #7ED321;
            --primary-orange: #F5A623;
            --primary-red: #D0021B;
            --primary-purple: #9013FE;
            --light-blue: #E3F2FD;
            --light-green: #E8F5E8;
            --light-orange: #FFF8E1;
            --light-red: #FFEBEE;
            --light-purple: #F3E5F5;
            --dark-text: #2C3E50;
            --medium-text: #5D6D7E;
            --light-text: #85929E;
            --border-color: #E8EAED;
            --hover-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        /* Main App Background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        /* Header Section */
        .main-header {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            margin: -70px -1rem 30px -1rem;
            padding: 20px 0;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            border-bottom: 1px solid var(--border-color);
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 30px;
        }

        .logo-section {
            text-align: center;
        }

        .logo {
            font-size: 32px;
            font-weight: 800;
            color: var(--primary-blue);
            margin-bottom: 5px;
        }

        .tagline {
            font-size: 14px;
            color: var(--medium-text);
            font-weight: 600;
        }

        /* Main Container */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Tool Grid Layout (LightPDF Style) */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .tool-card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }

        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--hover-shadow);
            border-color: var(--primary-blue);
        }

        .tool-card.pdf-merge {
            background: linear-gradient(135deg, var(--light-blue), white);
        }

        .tool-card.page-remove {
            background: linear-gradient(135deg, var(--light-red), white);
        }

        .tool-card.pdf-split {
            background: linear-gradient(135deg, var(--light-green), white);
        }

        .tool-icon {
            font-size: 48px;
            margin-bottom: 20px;
            display: block;
        }

        .tool-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 10px;
        }

        .tool-description {
            font-size: 14px;
            color: var(--medium-text);
            line-height: 1.5;
        }

        /* Workflow Container */
        .workflow-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin: 30px auto;
            max-width: 1200px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }

        /* Step Cards */
        .step-card {
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            transition: all 0.3s ease;
        }

        .step-card.active {
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
        }

        .step-card.completed {
            border-color: var(--primary-green);
            background: linear-gradient(135deg, var(--light-green), white);
        }

        .step-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        .step-number {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--primary-blue);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 18px;
        }

        .step-number.completed {
            background: var(--primary-green);
        }

        .step-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--dark-text);
        }

        /* Upload Zone */
        .upload-zone {
            border: 3px dashed var(--primary-blue);
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            background: linear-gradient(135deg, var(--light-blue), rgba(255, 255, 255, 0.8));
            margin: 20px 0;
            transition: all 0.3s ease;
        }

        .upload-zone:hover {
            border-color: var(--primary-purple);
            background: linear-gradient(135deg, var(--light-purple), rgba(255, 255, 255, 0.8));
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 60px;
            color: var(--primary-blue);
            margin-bottom: 15px;
        }

        .upload-text {
            font-size: 20px;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 8px;
        }

        .upload-subtext {
            font-size: 14px;
            color: var(--medium-text);
        }

        /* File Info Cards */
        .file-info-card {
            background: linear-gradient(135deg, var(--light-blue), white);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .file-info-card:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .file-details {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .file-icon {
            font-size: 32px;
            color: var(--primary-red);
        }

        .file-text {
            display: flex;
            flex-direction: column;
        }

        .file-name {
            font-weight: 700;
            color: var(--dark-text);
            font-size: 16px;
        }

        .file-stats {
            font-size: 12px;
            color: var(--medium-text);
        }

        /* Modern Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: white;
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            color: var(--medium-text);
            font-weight: 600;
            padding: 12px 20px;
            border: none;
            transition: all 0.3s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple)) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: var(--light-blue);
            color: var(--primary-blue);
        }

        /* Insertion Point Selector */
        .insertion-point {
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
        }

        .insertion-point.active {
            border-color: var(--primary-orange);
            background: linear-gradient(135deg, var(--light-orange), white);
        }

        .insertion-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        .insertion-title {
            font-weight: 700;
            color: var(--dark-text);
            font-size: 16px;
        }

        /* Action Buttons */
        .btn {
            padding: 12px 24px;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple));
            color: white;
            box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--primary-green), #5CB85C);
            color: white;
        }

        .btn-warning {
            background: linear-gradient(135deg, var(--primary-orange), #F0AD4E);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--primary-red), #D9534F);
            color: white;
        }

        .btn-secondary {
            background: #F8F9FA;
            color: var(--dark-text);
            border: 2px solid var(--border-color);
        }

        .btn-secondary:hover {
            background: var(--light-blue);
            border-color: var(--primary-blue);
        }

        /* Page Removal Section */
        .page-removal-section {
            background: linear-gradient(135deg, var(--light-red), white);
            border: 1px solid #FFB3BA;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }

        .removal-title {
            color: var(--primary-red);
            font-weight: 700;
            font-size: 16px;
            margin-bottom: 10px;
        }

        /* Success/Error Messages */
        .message {
            padding: 16px 20px;
            border-radius: 12px;
            margin: 20px 0;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .message-success {
            background: linear-gradient(135deg, var(--light-green), white);
            border-left: 4px solid var(--primary-green);
            color: #155724;
        }

        .message-warning {
            background: linear-gradient(135deg, var(--light-orange), white);
            border-left: 4px solid var(--primary-orange);
            color: #856404;
        }

        .message-error {
            background: linear-gradient(135deg, var(--light-red), white);
            border-left: 4px solid var(--primary-red);
            color: #721c24;
        }

        .message-info {
            background: linear-gradient(135deg, var(--light-blue), white);
            border-left: 4px solid var(--primary-blue);
            color: #0c5460;
        }

        /* Progress Indicator */
        .progress-section {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
            text-align: center;
            border: 1px solid var(--border-color);
        }

        .progress-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 15px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                padding: 0 20px;
            }

            .workflow-container {
                padding: 25px;
                margin: 20px 10px;
            }

            .tools-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }

            .step-card {
                padding: 20px;
            }

            .file-info-card {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def safe_pdf_to_images(file_bytes, file_name, max_pages=10):
    """Safely convert PDF to images"""
    images = []
    doc = None
    try:
        doc = fitz.open("pdf", file_bytes)
        total_pages = len(doc)

        for page_num in range(min(total_pages, max_pages)):
            try:
                page = doc[page_num]
                mat = fitz.Matrix(1.2, 1.2)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(BytesIO(img_data))
                images.append(img)
                pix = None
            except Exception:
                placeholder = Image.new('RGB', (150, 200), color='lightgray')
                images.append(placeholder)

        return images, total_pages
    except Exception as e:
        st.error(f"Error processing {file_name}: {str(e)}")
        return [], 0
    finally:
        if doc:
            doc.close()

def get_page_count(file_bytes):
    """Get PDF page count"""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        return len(reader.pages)
    except Exception:
        return 0

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

def merge_pdf_workflow(mother_pdf, insertions):
    """Merge PDFs according to the workflow"""
    try:
        mother_reader = pypdf.PdfReader(BytesIO(mother_pdf['bytes']))
        writer = pypdf.PdfWriter()

        # Sort insertions by page number
        sorted_insertions = sorted(insertions, key=lambda x: x['after_page'])

        current_page = 0

        for insertion in sorted_insertions:
            # Add mother PDF pages up to insertion point
            while current_page < insertion['after_page']:
                if current_page < len(mother_reader.pages):
                    writer.add_page(mother_reader.pages[current_page])
                current_page += 1

            # Add pages from inserted PDF
            insert_reader = pypdf.PdfReader(BytesIO(insertion['pdf_bytes']))
            for page in insert_reader.pages:
                writer.add_page(page)

        # Add remaining mother PDF pages
        while current_page < len(mother_reader.pages):
            writer.add_page(mother_reader.pages[current_page])
            current_page += 1

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def create_download_link(file_bytes, filename):
    """Create download link"""
    b64 = base64.b64encode(file_bytes).decode()
    size_kb = len(file_bytes) // 1024
    href = f"""
    <div style="text-align: center; margin: 30px 0;">
        <a href="data:application/pdf;base64,{b64}" download="{filename}" class="btn btn-success">
            📥 Download Merged PDF ({size_kb} KB)
        </a>
    </div>
    """
    return href

def parse_page_numbers(page_string):
    """Parse comma-separated page numbers"""
    if not page_string.strip():
        return []

    pages = []
    try:
        for part in page_string.split(','):
            part = part.strip()
            if '-' in part:
                # Handle ranges like "1-5"
                start, end = map(int, part.split('-'))
                pages.extend(range(start, end + 1))
            else:
                pages.append(int(part))
        return sorted(list(set(pages)))
    except ValueError:
        st.error("Invalid page number format. Use comma-separated numbers like: 1, 3, 5-8")
        return []

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    load_css()

    # Initialize session state
    if 'mother_pdf' not in st.session_state:
        st.session_state.mother_pdf = None
    if 'insertions' not in st.session_state:
        st.session_state.insertions = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    # Header
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">📄 PDF Tools Hub</div>
                <div class="tagline">Professional PDF Solutions</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Show workflow or home based on state
    if st.session_state.current_step == 1 and not st.session_state.mother_pdf:
        show_home_page()
    else:
        show_workflow()

    st.markdown('</div>', unsafe_allow_html=True)

def show_home_page():
    """Display home page with tool selection"""
    st.markdown("""
    <div class="workflow-container">
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 36px; font-weight: 800; color: var(--dark-text); margin-bottom: 15px;">
                🚀 Professional PDF Tools
            </h1>
            <p style="font-size: 18px; color: var(--medium-text); max-width: 600px; margin: 0 auto;">
                Choose from our advanced PDF editing tools designed for professional workflows
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tool cards (LightPDF style)
    st.markdown('<div class="tools-grid">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Start PDF Merge", key="merge_tool", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()

        st.markdown("""
        <div class="tool-card pdf-merge">
            <div class="tool-icon">🔗</div>
            <div class="tool-title">Advanced PDF Merge</div>
            <div class="tool-description">
                Insert PDFs at specific page positions. Perfect for creating comprehensive reports 
                with multiple document sources.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tool-card page-remove">
            <div class="tool-icon">🗑️</div>
            <div class="tool-title">Page Removal</div>
            <div class="tool-description">
                Remove unwanted pages from any PDF. Specify page numbers 
                with comma-separated format for bulk operations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="tool-card pdf-split">
            <div class="tool-icon">📑</div>
            <div class="tool-title">PDF Splitter</div>
            <div class="tool-description">
                Split large PDFs into smaller files or extract specific 
                page ranges for targeted document sharing.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def show_workflow():
    """Display the main PDF merge workflow"""
    st.markdown("""
    <div class="workflow-container">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 28px; font-weight: 800; color: var(--dark-text);">
                🔗 Advanced PDF Merge Workflow
            </h1>
            <p style="color: var(--medium-text);">
                Create comprehensive reports by inserting PDFs at specific positions
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Home", key="back_home"):
        st.session_state.mother_pdf = None
        st.session_state.insertions = []
        st.session_state.current_step = 1
        st.rerun()

    # Step 1: Mother PDF Upload
    show_step_1()

    # Step 2: Add Insertions (if mother PDF is loaded)
    if st.session_state.mother_pdf:
        show_step_2()

    # Step 3: Final Processing (if insertions exist)
    if st.session_state.insertions:
        show_step_3()

def show_step_1():
    """Step 1: Upload Mother/Main PDF"""
    step_class = "step-card active" if not st.session_state.mother_pdf else "step-card completed"

    st.markdown(f"""
    <div class="{step_class}">
        <div class="step-header">
            <div class="step-number {'completed' if st.session_state.mother_pdf else ''}">1</div>
            <div class="step-title">Upload Mother PDF</div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.mother_pdf:
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">📄</div>
            <div class="upload-text">Select Your Main/Mother PDF</div>
            <div class="upload-subtext">This will be the base document for your merged report</div>
        </div>
        """, unsafe_allow_html=True)

        mother_file = st.file_uploader(
            "Choose Mother PDF file",
            type="pdf",
            key="mother_pdf_uploader",
            label_visibility="collapsed"
        )

        if mother_file:
            # Process mother PDF
            file_bytes = mother_file.read()
            mother_file.seek(0)

            st.session_state.mother_pdf = {
                'name': mother_file.name,
                'bytes': file_bytes,
                'pages': get_page_count(file_bytes),
                'size': len(file_bytes)
            }
            st.rerun()
    else:
        # Show mother PDF info
        show_pdf_info(st.session_state.mother_pdf, "Mother PDF", is_mother=True)

        # Page removal for mother PDF
        show_page_removal_section(st.session_state.mother_pdf, "mother")

    st.markdown('</div>', unsafe_allow_html=True)

def show_step_2():
    """Step 2: Add PDF Insertions"""
    st.markdown("""
    <div class="step-card active">
        <div class="step-header">
            <div class="step-number">2</div>
            <div class="step-title">Add PDF Insertions</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color: var(--medium-text); margin-bottom: 20px;">
        Insert additional PDFs after specific pages of your mother PDF 
        (Total pages: {st.session_state.mother_pdf['pages']})
    </p>
    """, unsafe_allow_html=True)

    # Show existing insertions
    for i, insertion in enumerate(st.session_state.insertions):
        show_insertion_card(insertion, i)

    # Add new insertion
    st.markdown("""
    <div class="insertion-point">
        <div class="insertion-header">
            <div class="insertion-title">➕ Add New PDF Insertion</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        new_pdf = st.file_uploader(
            "Choose PDF to insert",
            type="pdf",
            key=f"insert_pdf_{len(st.session_state.insertions)}",
            label_visibility="collapsed"
        )

    with col2:
        after_page = st.number_input(
            "Insert after page:",
            min_value=0,
            max_value=st.session_state.mother_pdf['pages'],
            value=st.session_state.mother_pdf['pages'],
            key=f"after_page_{len(st.session_state.insertions)}"
        )

    if new_pdf and st.button("➕ Add This Insertion", key="add_insertion"):
        file_bytes = new_pdf.read()
        new_pdf.seek(0)

        insertion = {
            'name': new_pdf.name,
            'bytes': file_bytes,
            'pages': get_page_count(file_bytes),
            'size': len(file_bytes),
            'after_page': after_page
        }

        st.session_state.insertions.append(insertion)
        st.success(f"✅ Added {new_pdf.name} to be inserted after page {after_page}")
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

def show_step_3():
    """Step 3: Final Processing and Download"""
    st.markdown("""
    <div class="step-card active">
        <div class="step-header">
            <div class="step-number">3</div>
            <div class="step-title">Final Processing & Download</div>
        </div>
    """, unsafe_allow_html=True)

    # Summary of operations
    total_insertions = len(st.session_state.insertions)
    total_pages = st.session_state.mother_pdf['pages'] + sum(ins['pages'] for ins in st.session_state.insertions)

    st.markdown(f"""
    <div style="background: var(--light-blue); padding: 20px; border-radius: 12px; margin: 20px 0;">
        <h4 style="color: var(--dark-text); margin-bottom: 15px;">📊 Merge Summary</h4>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; text-align: center;">
            <div>
                <div style="font-size: 24px; font-weight: 700; color: var(--primary-blue);">{st.session_state.mother_pdf['pages']}</div>
                <div style="font-size: 12px; color: var(--medium-text);">Mother PDF Pages</div>
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: var(--primary-orange);">{total_insertions}</div>
                <div style="font-size: 12px; color: var(--medium-text);">PDF Insertions</div>
            </div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: var(--primary-green);">{total_pages}</div>
                <div style="font-size: 12px; color: var(--medium-text);">Total Final Pages</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Process merge button
    if st.button("🔗 Process Final Merge", key="process_merge", type="primary", use_container_width=True):
        with st.spinner("🔄 Processing your merged PDF..."):
            # Apply page removals first
            processed_mother = st.session_state.mother_pdf.copy()
            processed_insertions = []

            # Process mother PDF page removals
            if f"mother_remove_pages" in st.session_state and st.session_state[f"mother_remove_pages"]:
                pages_to_remove = parse_page_numbers(st.session_state[f"mother_remove_pages"])
                if pages_to_remove:
                    processed_bytes = remove_pages_from_pdf(processed_mother['bytes'], pages_to_remove)
                    if processed_bytes:
                        processed_mother['bytes'] = processed_bytes
                        processed_mother['pages'] = get_page_count(processed_bytes)

            # Process insertion page removals
            for i, insertion in enumerate(st.session_state.insertions):
                processed_insertion = insertion.copy()
                if f"insert_{i}_remove_pages" in st.session_state and st.session_state[f"insert_{i}_remove_pages"]:
                    pages_to_remove = parse_page_numbers(st.session_state[f"insert_{i}_remove_pages"])
                    if pages_to_remove:
                        processed_bytes = remove_pages_from_pdf(insertion['bytes'], pages_to_remove)
                        if processed_bytes:
                            processed_insertion['bytes'] = processed_bytes
                            processed_insertion['pages'] = get_page_count(processed_bytes)

                processed_insertions.append(processed_insertion)

            # Perform the merge
            merged_pdf = merge_pdf_workflow(processed_mother, processed_insertions)

            if merged_pdf:
                st.markdown("""
                <div class="message message-success">
                    🎉 Your consolidated report has been created successfully!
                </div>
                """, unsafe_allow_html=True)

                timestamp = int(time.time())
                download_link = create_download_link(merged_pdf, f"consolidated_report_{timestamp}.pdf")
                st.markdown(download_link, unsafe_allow_html=True)

                # Reset workflow option
                if st.button("🔄 Start New Merge", key="restart_workflow"):
                    st.session_state.mother_pdf = None
                    st.session_state.insertions = []
                    st.session_state.current_step = 1
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def show_pdf_info(pdf_info, title, is_mother=False):
    """Display PDF information card"""
    icon = "📄" if is_mother else "📎"

    st.markdown(f"""
    <div class="file-info-card">
        <div class="file-details">
            <div class="file-icon">{icon}</div>
            <div class="file-text">
                <div class="file-name">{title}: {pdf_info['name']}</div>
                <div class="file-stats">{pdf_info['pages']} pages • {len(pdf_info['bytes']) // 1024} KB</div>
            </div>
        </div>
        <div>
            <span class="btn btn-secondary" style="font-size: 12px;">✅ Loaded</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_insertion_card(insertion, index):
    """Display insertion card with details"""
    st.markdown(f"""
    <div class="insertion-point active">
        <div class="insertion-header">
            <div class="insertion-title">📎 Insertion #{index + 1}</div>
            <button onclick="removeInsertion({index})" style="background: var(--primary-red); color: white; border: none; border-radius: 4px; padding: 4px 8px; font-size: 12px;">❌</button>
        </div>
        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 15px; align-items: center;">
            <div>
                <strong>{insertion['name']}</strong><br>
                <small style="color: var(--medium-text);">{insertion['pages']} pages • {insertion['size'] // 1024} KB</small>
            </div>
            <div>
                <strong>After Page:</strong><br>
                <span style="color: var(--primary-orange);">{insertion['after_page']}</span>
            </div>
            <div>
                <button class="btn btn-secondary" style="font-size: 12px; padding: 6px 12px;">📄 Preview</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Page removal for this insertion
    show_page_removal_section(insertion, f"insert_{index}")

    # Remove insertion button
    if st.button(f"🗑️ Remove Insertion #{index + 1}", key=f"remove_insertion_{index}"):
        st.session_state.insertions.pop(index)
        st.rerun()

def show_page_removal_section(pdf_info, prefix):
    """Show page removal section for a PDF"""
    st.markdown(f"""
    <div class="page-removal-section">
        <div class="removal-title">🗑️ Remove Pages (Optional)</div>
        <p style="font-size: 12px; color: var(--medium-text); margin: 5px 0;">
            Enter page numbers to remove (e.g., "1, 3, 5-8" removes pages 1, 3, and 5 through 8)
        </p>
    </div>
    """, unsafe_allow_html=True)

    remove_pages = st.text_input(
        f"Pages to remove from {pdf_info['name']}:",
        key=f"{prefix}_remove_pages",
        placeholder="e.g., 1, 3, 5-8",
        help="Enter page numbers separated by commas. Use ranges like 5-8 for multiple consecutive pages."
    )

    if remove_pages:
        pages = parse_page_numbers(remove_pages)
        if pages:
            valid_pages = [p for p in pages if 1 <= p <= pdf_info['pages']]
            if valid_pages:
                st.markdown(f"""
                <div class="message message-warning">
                    ⚠️ Will remove {len(valid_pages)} page(s): {', '.join(map(str, valid_pages))}
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
