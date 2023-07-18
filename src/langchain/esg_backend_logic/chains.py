from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from .init_database import *
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')

llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo-16k',
    openai_api_key=OPENAI_API_KEY
)

# init chains with indices for different sectors/disclosures


# standard chain for consolidated QA, works for most stuff
db_consolidated = create_cloud_index(False)
chain_consolidated = load_qa_chain(llm, chain_type="stuff")

# chain for environmental disclosures GRI
db_env_disclosure = get_env_retriever()
chain_env_disclosures = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_env_disclosure)

# chain for social disclosures GRI
db_soc_disclosure = get_soc_retriever()
chain_soc_disclosures = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_soc_disclosure)

# chain for governance disclosures GRI
db_gov_disclosure = get_gov_retriever()
chain_gov_disclosures = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_gov_disclosure)

# chain for consolidated sector GRI
db_sector = get_sector_retriever()
chain_sector = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_sector)

# chain for coal sector GRI
db_coal_sector = get_coal_retriever()
chain_coal_sector = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_coal_sector)

# chain for oil sector GRI
db_oil_sector = get_oil_gas_retriever()
chain_oil_gas_sector = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_oil_sector)

# chain for agrar and aqua sector GRI
db_agrar_aqua_sector = get_agrar_aqua_retriever()
chain_agrar_aqua_sector = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db_agrar_aqua_sector)


# run chains for provided templates

def run_standard(template):
    # hyperparameter k: number of document-chunks passed to model. (16k tokens is a lot)
    return chain_consolidated.run(input_documents=db_consolidated.similarity_search(template), question=template, k=5)


def run_local(template, chain):
    return chain(template)
