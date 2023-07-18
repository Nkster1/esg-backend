import hashlib
import os
from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import pinecone, Pinecone

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone

from src.langchain.data_model import ChatRequest


# load dotenv content
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '1ced76ab-879c-4da5-a3e8-1c83b77ee8e0')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'us-central1-gcp')

if OPENAI_API_KEY is None:
    raise ValueError("Please set OPENAI_API_KEY and PINECONE_API_KEY")


_chat_gpt_template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {input}
Assistant:"""

chat_gpt_prompt = PromptTemplate(
    input_variables=["history", "input"], template=_chat_gpt_template
)



def question_answering_query_based_on_vector_db(local_filepath: str, query: str):
    """
    loads pdf under local_filepath , indexes it using pinecone and asks LLM for results given the query and the pinecone vector db
    :param local_filepath: pdf filepath that is used for pinecone
    :param query: query to db
    :return:
    """
    if not local_filepath.endswith(".pdf"):
        raise ValueError("local_filepath must be a pdf file")
    # load PDF file
    loader = PyPDFLoader(local_filepath)
    data = loader.load()

    # Split PDF data into chunks
    text_split = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_split.split_documents(data)

    # Create embeddings for semantic search
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index_name = "esg-nav"
    embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_texts(
        [t.page_content for t in texts], embeddings_model, index_name=index_name
    )

    docs = docsearch.similarity_search(query)

    # Query results from similarity search using OpenAI QA Chain
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=docs, question=query)

    return result


def chat(chat_request: ChatRequest):
    """
    chat with llm
    :return: answer to question
    """
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    memory = ConversationBufferWindowMemory(k=3)
    for user_input, ai_output in chat_request.to_conversation_buffer_memory_format():
        memory.save_context(user_input, ai_output)

    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=chat_gpt_prompt,
        verbose=True,
        memory=None,
    )

    output = chatgpt_chain.predict(
        input=chat_request.new_message, history=memory.load_memory_variables({})
    )
    return output


# ignore for now maybe useful for storing docs locally
def hash_filename(filename: str):
    """Generate a hash of a file using md5."""
    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()
