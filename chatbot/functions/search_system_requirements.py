from langchain.agents import tool
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.prompts import PromptTemplate
from langchain.agents.agent_toolkits import (
    create_csv_agent,
)
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import regex as re
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda
from langchain.output_parsers.openai_functions import (
    JsonKeyOutputFunctionsParser
)
#local function
from ..pydanticBaseModel.pydanticBaseModel import Software, Info
from ..functions.csv_retrieval import csv_retrieval

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list

@tool(args_schema=Software)
def search_system_requirements(name: Software):
    """Search system requirements of an software (could be game, application, so on)"""

    functions = [convert_pydantic_to_openai_function(Info)]

    extraction_prompt = PromptTemplate.from_template(
        """A article will be passed to you. Extract from it most 3 system requirements for an application that are mentioned by this article match the requirement of customer. 

    If customer not provide enough information to you to extracting, just ask customer.

    Do not extract the name of the article itself. If no system requirements are mentioned that's fine - you don't need to extract any! Just return an empty list.

    Do not make up or guess ANY extra information. Only extract what exactly is in the text.

    Article below:
    {input}"""
    )

    url_data = csv_retrieval(str(name))

    if not url_data:
        return "No information was found!"

    extraction_model = ChatOpenAI(
        engine="gpt-35-turbo-16k",  # engine = "deployment_name"
    ).bind(functions=functions, function_call={"name": "Info"})
    loader = WebBaseLoader(url_data)
    documents = loader.load()
    doc = documents[0]
    splits = text_splitter.split_text(doc.page_content)

    prep = RunnableLambda(lambda x: [{"input": doc} for doc in splits])

    extraction_chain = (
        extraction_prompt
        | extraction_model
        | JsonKeyOutputFunctionsParser(key_name="reqs")
    )
    flatten_chain = prep | extraction_chain.map() | flatten
    # test_chain = extraction_prompt | extraction_model |  JsonKeyOutputFunctionsParser(key_name="reqs")
    # test_result = test_chain.invoke({"input": splits[2]})
    # print('\n ---test result: ', test_result)
    result = flatten_chain.invoke({"input": doc.page_content})
    print("\n---1", result)

    choice_prompt = PromptTemplate.from_template(
        """You will be given a list of system requirements for a specific product, as well as the customer's requirements and an example answer. 
        
        Your task is to choose up to three requirements from the list that best match the customer's needs and provide an answer using the example answer as a template. 

        If no suitable information are mentioned that's fine - you don't need to do any! Just return an empty list.
        
        It is important not to make up or guess any additional information.

        Customer requirements:
        {customer_input}.

        Information:
        {info}

        Please note that the following example is not an official answer, but it demonstrates the format for providing an answer. Let's call it Application X. You can add or delete attributes based on the provided information:
        Example Answer:
            Here are the system requirements I recommend for Application X:
            1/ 
            X Version: 1999
            Operating System: Windows 2 (11-bit), Windows 3 (12-bit), or Windows 7 SP1 (64-bit)
            Processor: 1 GHz (1+ GHz recommended)
            Memory: 1 GB RAM (11 GB recommended)
            Screen Display: 123 x 123 resolution with True Color
            Display Card: 4 GB GPU with 29 GB/s Bandwidth
            Pointing Device: MS-Mouse compliant
            Network: Internet connection for installation and licensing
            2/ 
            X Version: 2000
            Operating System: Windows 2 (11-bit), Windows 3 (12-bit), or Windows 7 SP1 (64-bit)
            Processor: 1 GHz (1+ GHz recommended)
            Memory: 1 GB RAM (11 GB recommended)
            Screen Display: 123 x 123 resolution with True Color
            Display Card: 4 GB GPU with 29 GB/s Bandwidth
            Pointing Device: MS-Mouse compliant
            Network: Internet connection for installation and licensing
            3/
            X Version: 3000
            Operating System: Windows 2 (11-bit), Windows 3 (12-bit), or Windows 7 SP1 (64-bit)
            Processor: 1 GHz (1+ GHz recommended)
            Memory: 1 GB RAM (11 GB recommended)
            Screen Display: 123 x 123 resolution with True Color
            Display Card: 4 GB GPU with 29 GB/s Bandwidth
            Pointing Device: MS-Mouse compliant
            Network: Internet connection for installation and licensing
        """
    )

    choice_model = ChatOpenAI(
        engine="gpt-35-turbo-16k",  # engine = "deployment_name"
    )

    choice_chain = choice_prompt | choice_model
    new_list = [{"system info": d} for d in result]
    info = "".join(str(item) for item in new_list)
    res = choice_chain.invoke({"customer_input": """system requirements of {name}""", "info": info})
    print("\n---2", res)

    return res
