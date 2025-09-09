import streamlit as st
import fitz  # PyMuPDF
import pypdf  # Updated from PyPDF2 to pypdf (maintained version)
from io import BytesIO
import base64

st.set_page_config(
    page_title="PDF Editor Pro", 
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #4ecdc4;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff5252;
    }
    .upload-box {
        border: 2px dashed #4ecdc4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
@st.cache_data
def pdf_to_images(file_bytes, file_name):
    """Convert PDF file bytes to list of images (one per page)."""
    try:
        images = []
        doc = fitz.open("pdf", file_bytes)
        for page_num in range(len(doc)):
            # Convert page to image with good quality
            pix = doc[page_num].get_pixmap(matrix=fitz.Matrix(2, 2))  
            img_bytes = pix.tobytes("png")
            images.append(img_bytes)
        doc.close()
        return images, len(images)
    except Exception as e:
        st.error(f"Error converting {file_name} to images: {str(e)}")
        return [], 0

def get_pdf_page_count(file_bytes):
    """Get number of pages in PDF from bytes."""
    try:
        pdf_reader = pypdf.PdfReader(BytesIO(file_bytes))
        return len(pdf_reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return 0

def delete_pages(file_bytes, pages_to_delete):
    """Delete specified pages from PDF."""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        writer = pypdf.PdfWriter()

        for i in range(len(reader.pages)):
            if (i + 1) not in pages_to_delete:
                writer.add_page(reader.pages[i])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error deleting pages: {str(e)}")
        return None

def reorder_pages(file_bytes, new_order):
    """Reorder PDF pages according to new_order list."""
    try:
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        writer = pypdf.PdfWriter()

        for page_num in new_order:
            writer.add_page(reader.pages[page_num - 1])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error reordering pages: {str(e)}")
        return None

def insert_pages_at_position(main_file_bytes, insert_file_bytes, position):
    """Insert pages from one PDF into another at specified position."""
    try:
        main_reader = pypdf.PdfReader(BytesIO(main_file_bytes))
        insert_reader = pypdf.PdfReader(BytesIO(insert_file_bytes))
        writer = pypdf.PdfWriter()

        # Add pages before insertion point
        for i in range(position - 1):
            if i < len(main_reader.pages):
                writer.add_page(main_reader.pages[i])

        # Add all pages from insert file
        for page in insert_reader.pages:
            writer.add_page(page)

        # Add remaining pages from main file
        for i in range(position - 1, len(main_reader.pages)):
            writer.add_page(main_reader.pages[i])

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error inserting pages: {str(e)}")
        return None

def merge_pdfs(file_bytes_list):
    """Merge multiple PDF files into one."""
    try:
        writer = pypdf.PdfWriter()

        for file_bytes in file_bytes_list:
            reader = pypdf.PdfReader(BytesIO(file_bytes))
            for page in reader.pages:
                writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error merging PDFs: {str(e)}")
        return None

def create_download_link(file_bytes, filename, text="Download"):
    """Create a download link for processed PDF."""
    b64 = base64.b64encode(file_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Main App Interface
st.markdown('<h1 class="main-header">📑 PDF Editor Pro</h1>', unsafe_allow_html=True)
st.markdown("**Upload, preview, edit, and download PDFs with ease - No coding required!**")

# Sidebar for operations
with st.sidebar:
    st.header("🔧 Operations")
    operation = st.radio(
        "Select Operation:",
        ["Preview PDFs", "Delete Pages", "Reorder Pages", "Insert Pages", "Merge PDFs"]
    )

# File Upload Section
st.markdown('<div class="section-header">📤 Upload PDF Files</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Choose PDF files to work with:",
    type="pdf",
    accept_multiple_files=True,
    help="You can upload multiple PDF files at once. Each file should be under 200MB.",
    key="pdf_uploader"
)

if uploaded_files:
    # Store file data in session state for persistence
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = {}

    # Process uploaded files
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        st.session_state.pdf_data[uploaded_file.name] = {
            'bytes': file_bytes,
            'pages': get_pdf_page_count(file_bytes)
        }

    # Display file information
    st.success(f"✅ {len(uploaded_files)} PDF file(s) uploaded successfully!")

    # File overview table
    import pandas as pd
    file_info = []
    for name, data in st.session_state.pdf_data.items():
        file_info.append({
            'File Name': name,
            'Pages': data['pages'],
            'Size': f"{len(data['bytes']) / 1024:.1f} KB"
        })

    df = pd.DataFrame(file_info)
    st.dataframe(df, use_container_width=True)

    # Operation-specific interface
    if operation == "Preview PDFs":
        st.markdown('<div class="section-header">👁️ PDF Preview</div>', unsafe_allow_html=True)

        selected_file = st.selectbox("Select PDF to preview:", list(st.session_state.pdf_data.keys()))

        if selected_file:
            file_data = st.session_state.pdf_data[selected_file]

            with st.spinner("Converting PDF to images..."):
                images, page_count = pdf_to_images(file_data['bytes'], selected_file)

            if images:
                st.info(f"📄 {selected_file} - {page_count} pages")

                # Display images in grid layout
                cols = st.columns(3)
                for i, img_bytes in enumerate(images):
                    with cols[i % 3]:
                        st.image(
                            img_bytes,
                            caption=f"Page {i+1}",
                            use_column_width=True
                        )

    elif operation == "Delete Pages":
        st.markdown('<div class="section-header">🗑️ Delete Pages</div>', unsafe_allow_html=True)

        selected_file = st.selectbox("Select PDF to edit:", list(st.session_state.pdf_data.keys()))

        if selected_file:
            file_data = st.session_state.pdf_data[selected_file]
            max_pages = file_data['pages']

            st.info(f"📄 {selected_file} has {max_pages} pages")

            pages_to_delete = st.multiselect(
                "Select pages to delete:",
                range(1, max_pages + 1),
                help="Hold Ctrl/Cmd to select multiple pages"
            )

            if pages_to_delete and st.button("🗑️ Delete Selected Pages"):
                with st.spinner("Deleting pages..."):
                    result_bytes = delete_pages(file_data['bytes'], pages_to_delete)

                if result_bytes:
                    st.success(f"✅ Deleted {len(pages_to_delete)} page(s) successfully!")
                    st.download_button(
                        "📥 Download Edited PDF",
                        data=result_bytes,
                        file_name=f"{selected_file.replace('.pdf', '_deleted.pdf')}",
                        mime="application/pdf"
                    )

    elif operation == "Reorder Pages":
        st.markdown('<div class="section-header">🔄 Reorder Pages</div>', unsafe_allow_html=True)

        selected_file = st.selectbox("Select PDF to reorder:", list(st.session_state.pdf_data.keys()))

        if selected_file:
            file_data = st.session_state.pdf_data[selected_file]
            max_pages = file_data['pages']

            st.info(f"📄 {selected_file} has {max_pages} pages")
            st.write(f"**Current order:** {list(range(1, max_pages + 1))}")

            new_order_text = st.text_input(
                "Enter new page order (comma-separated):",
                value=",".join(str(i) for i in range(1, max_pages + 1)),
                help="Example: 3,1,2,4 to move page 3 to the beginning"
            )

            if st.button("🔄 Reorder Pages"):
                try:
                    new_order = [int(x.strip()) for x in new_order_text.split(",")]

                    # Validation
                    if len(new_order) != max_pages:
                        st.error(f"❌ Please specify exactly {max_pages} page numbers")
                    elif sorted(new_order) != list(range(1, max_pages + 1)):
                        st.error("❌ Invalid page numbers. Use each page number exactly once.")
                    else:
                        with st.spinner("Reordering pages..."):
                            result_bytes = reorder_pages(file_data['bytes'], new_order)

                        if result_bytes:
                            st.success("✅ Pages reordered successfully!")
                            st.write(f"**New order:** {new_order}")
                            st.download_button(
                                "📥 Download Reordered PDF",
                                data=result_bytes,
                                file_name=f"{selected_file.replace('.pdf', '_reordered.pdf')}",
                                mime="application/pdf"
                            )
                except ValueError:
                    st.error("❌ Please enter valid page numbers separated by commas")

    elif operation == "Insert Pages":
        st.markdown('<div class="section-header">📥 Insert Pages</div>', unsafe_allow_html=True)

        if len(st.session_state.pdf_data) < 2:
            st.warning("⚠️ You need at least 2 PDF files to use the insert pages feature")
        else:
            files_list = list(st.session_state.pdf_data.keys())

            col1, col2 = st.columns(2)

            with col1:
                main_file = st.selectbox("Select main PDF:", files_list)

            with col2:
                insert_file = st.selectbox("Select PDF to insert:", [f for f in files_list if f != main_file])

            if main_file and insert_file:
                main_pages = st.session_state.pdf_data[main_file]['pages']
                insert_pages = st.session_state.pdf_data[insert_file]['pages']

                st.info(f"📄 **{main_file}**: {main_pages} pages")
                st.info(f"📥 **{insert_file}**: {insert_pages} pages will be inserted")

                position = st.number_input(
                    "Insert at position (page number):",
                    min_value=1,
                    max_value=main_pages + 1,
                    value=main_pages + 1,
                    help=f"Position 1 = beginning, Position {main_pages + 1} = end"
                )

                if st.button("📥 Insert Pages"):
                    with st.spinner("Inserting pages..."):
                        result_bytes = insert_pages_at_position(
                            st.session_state.pdf_data[main_file]['bytes'],
                            st.session_state.pdf_data[insert_file]['bytes'],
                            position
                        )

                    if result_bytes:
                        st.success(f"✅ Inserted {insert_pages} page(s) at position {position}!")
                        st.download_button(
                            "📥 Download Combined PDF",
                            data=result_bytes,
                            file_name=f"{main_file.replace('.pdf', '_with_insert.pdf')}",
                            mime="application/pdf"
                        )

    elif operation == "Merge PDFs":
        st.markdown('<div class="section-header">🔗 Merge PDFs</div>', unsafe_allow_html=True)

        if len(st.session_state.pdf_data) < 2:
            st.warning("⚠️ You need at least 2 PDF files to merge")
        else:
            st.info("📋 All uploaded PDFs will be merged in the order shown above")

            total_pages = sum(data['pages'] for data in st.session_state.pdf_data.values())
            st.write(f"**Total pages after merge:** {total_pages}")

            if st.button("🔗 Merge All PDFs"):
                with st.spinner("Merging PDFs..."):
                    file_bytes_list = [data['bytes'] for data in st.session_state.pdf_data.values()]
                    result_bytes = merge_pdfs(file_bytes_list)

                if result_bytes:
                    st.success(f"✅ Merged {len(st.session_state.pdf_data)} PDFs successfully!")
                    st.download_button(
                        "📥 Download Merged PDF",
                        data=result_bytes,
                        file_name="merged_document.pdf",
                        mime="application/pdf"
                    )

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>Welcome to PDF Editor Pro! 🎉</h2>
        <p>Upload your PDF files above to get started with these features:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **👁️ Preview**
        - View PDF pages as images
        - High-quality thumbnails
        - Easy navigation
        """)

    with col2:
        st.markdown("""
        **✂️ Edit Pages**
        - Delete unwanted pages
        - Reorder page sequence
        - Insert pages from other PDFs
        """)

    with col3:
        st.markdown("""
        **🔗 Merge PDFs**
        - Combine multiple PDFs
        - Maintain quality
        - One-click download
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <small>Built with ❤️ using Streamlit, PyMuPDF, and pypdf | 
    <a href="https://github.com" target="_blank">Source Code</a>
    </small>
</div>
""", unsafe_allow_html=True)
