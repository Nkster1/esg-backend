from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from src.langchain.esg_backend_logic import chains

"""
class ChatBox:
    def __init__(self, context, company):
        # context is the json generated from generate_esg_reporting
        self.context = context
        self.company = company
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(chains.llm, chains.chain_consolidated, memory=self.memory)
        self.chat_history = []
        query = "what is are the relevant GRI topics and GRI disclosures for the company: " + self.company + "?"
"""
        # result = f"""This json-file contains the relevant topics and disclosures for the company: {self.context} with the following information about the company: {self.company}."""
"""       
        self.chat_history.append((query, result))

    def chat_box(self, user_query):
        res = self.qa({"question": user_query, "chat_history": self.chat_history})['answer']
        self.chat_history.append((user_query, res))
        return res
"""

from langchain import PromptTemplate

_company_description_increase_esg_template = """
Answer the question based on the context below
Context: description of a company as context: {company_description}

Question: what concrete measures can they take to increase their ESG rating?

Answer: """

company_description_increase_esg_prompt = PromptTemplate(
    template=_company_description_increase_esg_template,
    input_variables=["company_description"],
)

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