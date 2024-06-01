from langchain.utilities import SQLDatabase
import os
from dotenv import load_dotenv
from langchain.agents import tool
from ..pydanticBaseModel.pydanticBaseModel import CustomerInput
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)

from ...db_funcs.bot_sql_executor_controller import get_product_data


load_dotenv()
# db = SQLDatabase.from_uri(os.getenv("DATABASE_URI"))


@tool(args_schema=CustomerInput)
def find_product(query: CustomerInput):
    """Answer customer question about finding a product in BKTechStore with customer requirement"""

    input = query

    model = ChatOpenAI(engine="gpt-35-turbo-16k", temperature=0)

    prompt = PromptTemplate.from_template(
        """Given the provided table information and the user's question, you need to generate an SQL query based on the information.
        However, if there is no suitable SQL query that can be adapted to the user's question, you should only respond with the phrase "cannot generate sql"


    Question: {input}
    



    Table Information:
    CREATE TABLE IF NOT EXISTS product_line(
        id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        category TEXT,
        vendor TEXT NOT NULL ,
        name VARCHAR(30) NOT NULL ,
        CONSTRAINT fk_product_category
            FOREIGN KEY (category) REFERENCES category(category_name)
                ON DELETE set NULL
                ON UPDATE CASCADE,
        CONSTRAINT fk_product_vendor
            FOREIGN KEY (vendor) REFERENCES vendor(code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY  ,
        name TEXT not null ,
        sku CHAR(10) UNIQUE ,
        local_specs JSONB,
        quantity QUANTITY DEFAULT 1,
        list_price PRICE,
        product_line SERIAL NOT NULL ,
        CONSTRAINT fk_productLine
            FOREIGN KEY (product_line) REFERENCES product_line(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS vendor(
        id TEXT PRIMARY KEY ,
        name TEXT UNIQUE
    );

    


    Table Sample Insert Data:
    some keyword can be used with query product category are: laptop, apple, audio, accessories, games, streams;
    some keyword can be used with query product vendor are: asus, acer, apple, hp, samsung, sony, STEELSERIES, intel, seagate, corsair, samsung, jbl, xiaomi, logitech;
    
    Query Instruction (5 notes):
    1. Not select attribute `images`, `sku` while in the SQL statements. You are encouraged to join the product_line and product tables together in the SQL query.
    2. Check and change case sensitive of the user's query to match the given keywords have been provided to you (vendor and category, for example: LOGITECH change to logitech, Laptop change to laptop).
    3. Check and compare user's keyword to match the attribute keywords have been provided to you (vendor and category, for example: user keyword - hp laptop, vendor keyword - hp, category keyword - laptop).
    4. If you are given the full name of product such as "laptop lenovo ideapad", "laptop hp omen", please do the query by product name and MUST include the local_specs column in the select list.
    5. In case need to query N records of data, select limit upto 5.
    6. Priority to use ILIKE operator in ALL the query statement rather than simply LIKE.

    
    Some basic example output:
    keyword use: SELECT product.name, product.list_price , product_line.category, product.quantity FROM product INNER JOIN product_line ON product.product_line=product_line.id WHERE product_line.category ILIKE '%%laptop%%' LIMIT 5;
    product name use: SELECT product.local_specs, product.name, product.list_price , product.quantity FROM product where product.name ILIKE '%%laptop lenovo ideapad%%';


    Please note that you should not make up or guess any additional information or additional newline when generating the SQL query.
    """
    )

    qa_chain = prompt | model | OpenAIFunctionsAgentOutputParser()
    res = qa_chain.invoke({"input": query})
    print(res.return_values['output'])

    product_data = get_product_data(res.return_values['output'])

    print(f"PRODUCT DATA FOUND: {product_data} - end.")

    return product_data
