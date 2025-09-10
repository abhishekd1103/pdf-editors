import streamlit as st
import fitz  # PyMuPDF
import pypdf
from io import BytesIO
import base64
from PIL import Image
import time
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
# SIMPLIFIED PROFESSIONAL CSS STYLING
# ============================================================================
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}

        .stApp {
            background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
            min-height: 100vh;
        }

        .main-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            margin: -70px -1rem 30px -1rem;
            padding: 20px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
        }

        .logo {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .workspace {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin: 20px auto;
            max-width: 1200px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .upload-zone {
            border: 3px dashed #3b82f6;
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05));
            margin: 20px 0;
            transition: all 0.3s ease;
        }

        .upload-zone:hover {
            border-color: #8b5cf6;
            transform: scale(1.02);
        }

        .pdf-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
            padding: 20px;
            background: rgba(59, 130, 246, 0.05);
            border-radius: 16px;
        }

        .page-card {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }

        .page-card:hover {
            border-color: #3b82f6;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
        }

        .page-card.selected {
            border-color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }

        .page-thumbnail {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .page-number {
            position: absolute;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
        }

        .file-badge {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            border-radius: 8px;
            font-size: 10px;
            font-weight: 600;
        }

        .btn {
            padding: 12px 24px;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }

        .btn-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }

        .btn-warning {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
        }

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
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #065f46;
        }

        .message-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #991b1b;
        }

        .message-info {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #1e40af;
        }

        .controls-section {
            background: rgba(59, 130, 246, 0.05);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }

        .file-info {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 15px;
            }

            .pdf-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
            }

            .workspace {
                margin: 20px 10px;
                padding: 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# IMPROVED UTILITY FUNCTIONS
# ============================================================================

def safe_pdf_to_images(file_bytes, file_name, max_pages=20):
    """Safely convert PDF to images with proper error handling"""
    images = []
    total_pages = 0
    doc = None

    try:
        # Open document
        doc = fitz.open("pdf", file_bytes)
        total_pages = len(doc)

        # Limit pages for performance
        pages_to_process = min(total_pages, max_pages)

        for page_num in range(pages_to_process):
            try:
                page = doc[page_num]
                # Use lower resolution for faster processing
                mat = fitz.Matrix(1.5, 1.5)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                pix = None  # Free memory

                img = Image.open(BytesIO(img_data))
                images.append(img)

            except Exception as page_error:
                st.warning(f"Could not process page {page_num + 1} of {file_name}: {str(page_error)}")
                # Create a placeholder image for failed pages
                placeholder = Image.new('RGB', (200, 300), color='lightgray')
                images.append(placeholder)

    except Exception as e:
        st.error(f"Error processing {file_name}: {str(e)}")
        return [], 0

    finally:
        # Always close the document
        if doc:
            doc.close()

    return images, total_pages

def get_pdf_page_count(file_bytes):
    """Get number of pages in PDF with error handling"""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        return len(reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return 0

def merge_pdfs_organized(pdf_data, page_selections):
    """Merge PDFs based on page selections"""
    try:
        writer = pypdf.PdfWriter()

        for filename, page_num in page_selections:
            if filename in pdf_data:
                reader = pypdf.PdfReader(BytesIO(pdf_data[filename]['bytes']))
                if page_num - 1 < len(reader.pages):
                    writer.add_page(reader.pages[page_num - 1])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def merge_pdfs_plain(pdf_data):
    """Simple merge of all PDFs"""
    try:
        writer = pypdf.PdfWriter()

        for file_data in pdf_data.values():
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

def create_download_link(file_bytes, filename):
    """Create download link"""
    b64 = base64.b64encode(file_bytes).decode()
    size_kb = len(file_bytes) // 1024
    href = f"""
    <a href="data:application/pdf;base64,{b64}" download="{filename}" class="btn btn-success">
        📥 Download PDF ({size_kb} KB)
    </a>
    """
    return href

def format_file_size(size_bytes):
    """Format file size"""
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
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    if 'selected_pages' not in st.session_state:
        st.session_state.selected_pages = []

    # Header
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo">📄 PDF Tools Hub</div>
            <div style="color: #64748b; font-weight: 600;">Professional PDF Solutions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown("""
    <div class="workspace">
        <h1 style="font-size: 36px; font-weight: 800; text-align: center; margin-bottom: 30px;">
            🔗 PDF Merge Tool
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # File upload
    st.markdown("""
    <div class="upload-zone">
        <div style="font-size: 48px; margin-bottom: 15px;">📁</div>
        <h3>Upload Multiple PDF Files</h3>
        <p>Drag and drop up to 10 PDF files (max 50MB each)</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        key="pdf_files",
        label_visibility="collapsed"
    )

    if uploaded_files:
        process_files(uploaded_files)

        if st.session_state.uploaded_files:
            show_merge_interface()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px; color: #64748b;">
            <div style="font-size: 60px; margin-bottom: 20px;">📄</div>
            <h3>No files uploaded yet</h3>
            <p>Upload PDF files to start merging</p>
        </div>
        """, unsafe_allow_html=True)

def process_files(uploaded_files):
    """Process uploaded files with better error handling"""
    if len(uploaded_files) > 10:
        st.error("⚠️ Maximum 10 files allowed")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name}...")

        file_size = len(file.read())
        file.seek(0)

        if file_size > 50 * 1024 * 1024:  # 50MB limit
            st.error(f"⚠️ {file.name} is too large (max 50MB)")
            continue

        if file.name not in st.session_state.uploaded_files:
            file_bytes = file.read()
            file.seek(0)

            st.session_state.uploaded_files[file.name] = {
                'bytes': file_bytes,
                'pages': get_pdf_page_count(file_bytes),
                'size': file_size
            }

        progress_bar.progress((idx + 1) / len(uploaded_files))

    status_text.text("✅ All files processed!")
    time.sleep(1)
    status_text.empty()
    progress_bar.empty()

def show_merge_interface():
    """Show the main merge interface"""
    total_files = len(st.session_state.uploaded_files)
    total_pages = sum(data['pages'] for data in st.session_state.uploaded_files.values())
    total_size = sum(data['size'] for data in st.session_state.uploaded_files.values())

    st.markdown(f"""
    <div class="message message-success">
        ✅ Successfully loaded {total_files} files ({total_pages} pages, {format_file_size(total_size)})
    </div>
    """, unsafe_allow_html=True)

    # Show file info
    for filename, data in st.session_state.uploaded_files.items():
        st.markdown(f"""
        <div class="file-info">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>📄 {filename}</strong>
                </div>
                <div style="display: flex; gap: 20px; color: #64748b;">
                    <span>📊 {data['pages']} pages</span>
                    <span>💾 {format_file_size(data['size'])}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Merge mode selection using proper Streamlit tabs
    tab1, tab2 = st.tabs(["📚 Plain Merge", "🎯 Organize Mode"])

    with tab1:
        show_plain_merge()

    with tab2:
        show_organize_mode()

def show_plain_merge():
    """Show plain merge interface"""
    st.markdown("""
    <div class="controls-section">
        <h3>📚 Plain Merge - All Files in Order</h3>
        <p>All PDF files will be merged in the order they appear above.</p>
    </div>
    """, unsafe_allow_html=True)

    # Show merge order
    st.markdown("**📋 Merge Order:**")
    for idx, filename in enumerate(st.session_state.uploaded_files.keys()):
        st.markdown(f"**{idx + 1}.** {filename}")

    if st.button("🔗 Merge All PDFs", key="merge_plain", type="primary", use_container_width=True):
        with st.spinner("🔄 Merging PDFs..."):
            merged_pdf = merge_pdfs_plain(st.session_state.uploaded_files)

            if merged_pdf:
                st.success("🎉 PDFs merged successfully!")

                timestamp = int(time.time())
                download_link = create_download_link(merged_pdf, f"merged_plain_{timestamp}.pdf")
                st.markdown(download_link, unsafe_allow_html=True)

def show_organize_mode():
    """Show organize mode with grid interface"""
    st.markdown("""
    <div class="controls-section">
        <h3>🎯 Organize Pages - Click to Select</h3>
        <p>Click on pages to select/deselect. Selected pages will be merged in order.</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate page data
    all_pages = []
    for filename, file_data in st.session_state.uploaded_files.items():
        try:
            images, total_pages = safe_pdf_to_images(file_data['bytes'], filename)

            for page_idx, image in enumerate(images):
                all_pages.append({
                    'filename': filename,
                    'page_num': page_idx + 1,
                    'image': image,
                    'key': f"{filename}_page_{page_idx + 1}",
                    'total_pages': total_pages
                })
        except Exception as e:
            st.error(f"Error processing {filename}: {str(e)}")

    if all_pages:
        # Control buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("✅ Select All", key="select_all"):
                st.session_state.selected_pages = [page['key'] for page in all_pages]
                st.rerun()

        with col2:
            if st.button("❌ Clear All", key="clear_all"):
                st.session_state.selected_pages = []
                st.rerun()

        with col3:
            selected_count = len(st.session_state.selected_pages)
            st.markdown(f"**📊 {selected_count} Selected**")

        with col4:
            if selected_count > 0 and st.button("🔗 Merge Selected", key="merge_selected", type="primary"):
                merge_selected_pages(all_pages)

        # Pages grid
        st.markdown('<div class="pdf-grid">', unsafe_allow_html=True)

        # Create columns dynamically
        cols = st.columns(4)
        for idx, page_data in enumerate(all_pages):
            with cols[idx % 4]:
                page_key = page_data['key']
                is_selected = page_key in st.session_state.selected_pages

                # Toggle selection button
                button_text = "✅ Selected" if is_selected else "⭕ Select"
                if st.button(button_text, key=f"btn_{page_key}", use_container_width=True):
                    if is_selected:
                        st.session_state.selected_pages.remove(page_key)
                    else:
                        st.session_state.selected_pages.append(page_key)
                    st.rerun()

                # Page card
                card_class = "page-card selected" if is_selected else "page-card"

                st.markdown(f"""
                <div class="{card_class}">
                    <div class="file-badge">{page_data['filename'][:8]}...</div>
                    <div class="page-number">{page_data['page_num']}</div>
                """, unsafe_allow_html=True)

                # Display image
                st.image(
                    page_data['image'],
                    use_column_width=True,
                    caption=f"Page {page_data['page_num']} of {page_data['total_pages']}"
                )

                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ No pages could be processed. Please check your PDF files.")

def merge_selected_pages(all_pages):
    """Merge selected pages"""
    if not st.session_state.selected_pages:
        st.warning("⚠️ No pages selected for merging")
        return

    with st.spinner("🔄 Merging selected pages..."):
        # Build page selections in order
        page_selections = []
        for page_key in st.session_state.selected_pages:
            # Find the page data
            for page_data in all_pages:
                if page_data['key'] == page_key:
                    page_selections.append((page_data['filename'], page_data['page_num']))
                    break

        merged_pdf = merge_pdfs_organized(st.session_state.uploaded_files, page_selections)

        if merged_pdf:
            st.success(f"🎉 Successfully merged {len(page_selections)} selected pages!")

            timestamp = int(time.time())
            download_link = create_download_link(merged_pdf, f"merged_organized_{timestamp}.pdf")
            st.markdown(download_link, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
