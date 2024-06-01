from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)
from langchain.document_loaders import PyPDFLoader
from langchain.retrievers import BM25Retriever


#local function
from ..pydanticBaseModel.pydanticBaseModel import CustomerInput

@tool(args_schema=CustomerInput)
def answer_about_bktechstore(query: CustomerInput):
    """Answer customer question about information of the BKTechStore policies such as business information, privacy, transaction term, online shopping guide, warranty policy, contact information, payment methods."""

    loader = PyPDFLoader("./static/chatbotref.pdf")
    docs = loader.load_and_split()

    doc_list = [doc.page_content for doc in docs]

    retriever = BM25Retriever.from_texts(doc_list)
    retriever.k = 3

    result = retriever.get_relevant_documents(query)

    info = "\n".join(item.page_content for item in result)

    print("\n--- result: ", result)
    print("\n--- policy info: ", info)

    policy_model = ChatOpenAI(engine="gpt-35-turbo-16k")
    policy_prompt = PromptTemplate.from_template(
        """You will be given information about BKTechStore policies, answer template and the customer's question, you will answer that question base on provided information.
        If no suitable information are mentioned that's fine - you answer that currently no information about this problem and tell them to contact customer care for exact details.
        It is important not to make up or guess any additional information.
        Do not contain the phrase "Based on the provided information" in your answer.

    Question: {input}
    
    Information of policies:
    {information}
    """
    )

    policy_chain = policy_prompt | policy_model | OpenAIFunctionsAgentOutputParser()
    res = policy_chain.invoke({"input": query, "information": info})
    return res
