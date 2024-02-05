import streamlit as st
import PyPDF2
from io import BytesIO
# Import any other libraries you need to process your PDFs. For example, PyPDF2.
import streamlit as st

from aws.opensearch import OpenSearch_custom
from llm_chain.chain.parser_resume import ResumeParserLLM, json_sample_schema_resume
from llm_chain.embedding import EmbeddingModel

os_client = OpenSearch_custom(
    host="search-ui-test-j4slt3fz7uu5ahsm6vgu3hwqem.us-east-2.es.amazonaws.com"
)
embedder = EmbeddingModel(model="text-embedding-ada-002")

def recommend_jobs(file):
    """
    Recommends jobs based on the provided resume file.

    Args:
        file_path (str): The path to the resume file.

    Returns:
        list: A list of recommended jobs.
    """

    resume_parser = ResumeParserLLM(model="gpt-3.5-turbo-1106")
    parsed_resume = resume_parser.parse(file, json_sample_schema_resume)

    serialized_string = ", ".join(f"{k}: {v}" for k, v in parsed_resume.items() if v)
    resume_embedding = embedder.get_embedding(text=serialized_string)

    # Search for jobs
    jobs = os_client.search_vector(
        index_name="jobs-index-vector",
        query=resume_embedding,
    )

    return jobs
# Function to read PDF content
def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        return first_page.extract_text()

def main():
    # Streamlit app layout
    st.title("PDF Upload App")

    # User input fields
    name = st.text_input("Enter your name:")

    age = st.number_input("Enter your age:", min_value=1)

    # PDF file uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Show details of the uploaded file
        #st.write("Filename:", uploaded_file.name)
        
        # Read and display PDF content
        text = read_pdf(uploaded_file)
        jobs = recommend_jobs(text)
        st.write(jobs)
    else:
        st.write("No file uploaded yet.")

# You can add more logic here based on the PDF content or user's inputs

'''
def main():
    st.title("PDF Upload Example")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        pdf_file = BytesIO(bytes_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        st.write(f"Number of pages in the PDF: {len(pdf_reader.pages)}")

        
        # Display text of the first page as an example
        page = pdf_reader.pages[0]
        page_text = page.extract_text()
        st.write(page_text)
'''
if __name__ == "__main__":
    main()
