# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import PyPDF2
from io import BytesIO

try ModuleNotFoundError:
    !pip install PyPDF2
else:
    pass

def merge_pdfs(pdfs):
    pdf_writer = PyPDF2.PdfWriter()
    for pdf in pdfs:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
    buf = BytesIO()
    pdf_writer.write(buf)
    buf.seek(0)
    return buf

def save_selected_pages(source_pdf, target_pdf_name, pages):
    pdf_reader = PyPDF2.PdfReader(source_pdf)
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in pages:
        try:
            page = pdf_reader.pages[int(page_num) - 1]
            pdf_writer.add_page(page)
        except IndexError:
            st.error(f"Page {page_num} is out of range.")
            return None
        except ValueError:
            st.error("Please make sure all entries in the pages list are numbers.")
            return None
    buf = BytesIO()
    pdf_writer.write(buf)
    buf.seek(0)
    return buf

# Setup tabs
tab1, tab2 = st.tabs(["PDF Merger", "PDF Extractor"])

# PDF Merger Tab
with tab1:
    st.header("Merge PDFs")
    uploaded_files = st.file_uploader("Select PDF files to merge", type="pdf", accept_multiple_files=True, key="merger")
    merged_pdf_name = st.text_input("Enter a name for the merged PDF file", "merged_document.pdf", key="merger_name")

    if st.button("Merge PDFs", key="merge"):
        if uploaded_files and merged_pdf_name:
            merged_pdf = merge_pdfs(uploaded_files)
            if merged_pdf:
                st.success("PDFs merged successfully!")
                st.download_button("Download Merged PDF", merged_pdf, file_name=merged_pdf_name, mime="application/pdf")
        else:
            st.error("Please upload some PDF files and specify a name for the merged file.")

# PDF Extractor Tab
with tab2:
    st.header("Extract Pages from PDF")
    source_pdf = st.file_uploader("Choose a PDF file", type=["pdf"], key="extractor")
    target_pdf_name = st.text_input("Enter the name for the new PDF file", "selected_pages.pdf", key="extractor_name")
    pages_to_save = st.text_input("Enter the pages to save (e.g., 1,3,5)", key="pages")

    if st.button("Extract Pages", key="extract"):
        if source_pdf and target_pdf_name and pages_to_save:
            pages_list = pages_to_save.split(',')
            new_pdf = save_selected_pages(source_pdf, target_pdf_name, pages_list)
            if new_pdf:
                st.success("Pages extracted successfully!")
                st.download_button("Download New PDF", new_pdf, file_name=target_pdf_name, mime="application/pdf")
        else:
            st.error("Please upload a PDF file, specify the new PDF file name, and enter the pages to extract.")

