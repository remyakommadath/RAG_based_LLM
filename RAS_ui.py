import os
import streamlit as st
import requests
from dotenv import load_dotenv
import arxiv
import shutil

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))

try: shutil.rmtree('./Documents')
except:pass
os.makedirs('Documents')

# Streamlit UI elements
st.title("Research Article Extraction")

question = st.text_input( "Enter a keyword",placeholder="Write your keyword here")
question2 = st.text_input( "Enter your query",placeholder="Write your query related to the keyword here")


# Construct the default API client.
client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = question,
  max_results = 5,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)

# `results` is a generator; you can iterate over its elements one by one...
for r in client.results(search):
  ids = [r.entry_id.split('/')[-1]]
  paper = next(arxiv.Client().results(arxiv.Search(id_list=ids)))
  # Download the PDF to a specified directory with a custom filename.
  paper.download_pdf(dirpath="./Documents")

if question2:

    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to Pathway API. Status code: {response.status_code}")
