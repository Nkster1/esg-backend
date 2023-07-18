from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone, Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
import os
import pinecone

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '1ced76ab-879c-4da5-a3e8-1c83b77ee8e0')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'us-central1-gcp')


# create different indexes for the sector/disclosure GRI with chroma and consolidated with pinecone
def create_local_index(index, path, is_dir, build):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    _dir = index
    

    # only activate, when documents added/changed for local storage
    if build:
        db = Chroma.from_documents(documents=load_documents(path, is_dir), embedding=embeddings,
                                   persist_directory=_dir)
        db.persist()

    db = Chroma(persist_directory=_dir, embedding_function=embeddings)

    return db.as_retriever(search_kwargs={"k": 5})


# index for consolidated set of GRI
def create_cloud_index(init):
    # create embeddings for semantic search
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = "esg"

    if init:
        document_search = Pinecone.from_texts([t.page_content for t in load_documents(
            '../documents/consolidated_gri/Consolidated Set of the GRI Standards.pdf', False)], embeddings,
                                              index_name=index_name)

    else:
        document_search = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

    return document_search


def load_documents(path, is_dir):
    if is_dir:
        loader = DirectoryLoader(path)
    else:
        loader = PyPDFLoader(path)

    # load data
    data = loader.load()
    # create batches, chunk_overlap s.t. no (little) meaning potentially lost when splitting
    text_split = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    texts = text_split.split_documents(data)
    return texts


def get_sector_retriever():
    # index for sector
    return create_local_index('sector_index', '../documents/sector_gri', True, False)


def get_coal_retriever():
    # index for coal_sector_gri
    return create_local_index('coal_index', '../documents/GRI 12_ Coal Sector 2022.pdf', False, False)


def get_oil_gas_retriever():
    # index for coal_sector_gri
    return create_local_index('oil_gas_index', '../documents/GRI 11_ Oil and Gas Sector 2021.pdf', False, False)


def get_agrar_aqua_retriever():
    # index for coal_sector_gri
    return create_local_index('agrar_aqua_index',
                              '../documents/GRI 13_ Agriculture Aquaculture and Fishing Sectors 2022.pdf',
                              False, False)


def get_gov_retriever():
    # index for gov disclosures
    return create_local_index('gov_disclosure', '../documents/disclosure_gov', True, False)


def get_soc_retriever():
    # index for soc disclosures
    return create_local_index('soc_disclosure', '../documents/disclosure_soc', True, False)


def get_env_retriever():
    # index for env disclosures
    return create_local_index('env_disclosure', '../documents/disclosure_env', True, False)
