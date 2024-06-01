from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)

#local function
from ..pydanticBaseModel.pydanticBaseModel import CustomerInput

@tool(args_schema=CustomerInput)
def answer_about_yourself(query: CustomerInput):
    """Answer customer question about introduce yourself or greetings as hi, hello, etc"""

    qa_model = ChatOpenAI(engine="gpt-35-turbo-16k")
    qa_prompt = PromptTemplate.from_template(
        """You will be given information and the customer's question, you will answer that question base on provided information.
        If customer greets you, greets them back and introduce to customer who you are base on the provided information. 
        It is important not to make up or guess any additional information.

    Question: {input}
    
    Information:
    You are an assistant of BKTechStore website. You will help the customer with their questions about the BKTechStore website which sells computer and related devices."""
    )

    qa_chain = qa_prompt | qa_model | OpenAIFunctionsAgentOutputParser()
    res = qa_chain.invoke({"input": query})
    return res