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

from ...db_funcs.product_data import get_product_data


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
        supplier TEXT NOT NULL ,
        name VARCHAR(30) NOT NULL ,
        CONSTRAINT fk_product_category
            FOREIGN KEY (category) REFERENCES category(category_name)
                ON DELETE set NULL
                ON UPDATE CASCADE,
        CONSTRAINT fk_product_supplier
            FOREIGN KEY (supplier) REFERENCES supplier(code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY  ,
        name TEXT not null ,
        sku CHAR(10) UNIQUE ,
        images text[],
        local_specs JSONB,
        quantity QUANTITY DEFAULT 1,
        price PRICE,
        is_standard BOOLEAN DEFAULT FALSE,
        product_line SERIAL NOT NULL ,
        CONSTRAINT fk_productLine
            FOREIGN KEY (product_line) REFERENCES product_line(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS supplier(
        code TEXT PRIMARY KEY ,
        name TEXT UNIQUE
    );

    


    Table Sample Insert Data:
    some keyword used with product category: category - ('laptop');
        
    some keyword used with supplier: supplier - ('asus'), ('dell'), ('apple'), ('acer'), ('hp'), ('lenovo'), ('msi'), ('kingston'), ('intel'), ('seagate'), ('corsair'), ('adata'), ('sandisk'), ('xigmatek'), ('samsung'), ('gigabyte'), ('wd'), ('deepcool'), ('soundpeats'), ('jbl'), ('dareu'), ('havit'), ('lg'), ('bose'), ('xiaomi'), ('microtek'), ('baseus'),('logitech'), ('hyperx'), ('soundmax'), ('sdrd'), ('razer'), ('segotep'), ('nzxt');
    
    some example existed records:
    INSERT INTO product_line (category, name, supplier) VALUES  ('laptop', 'lenovo ideapad', 'lenovo');

    INSERT INTO public.product (local_specs, quantity, price, is_standard, product_line, sku, images) VALUES  ('this is example specification list', 18, 15490000, false, 2, '22100234814 ', 'this is place holder for the real images list');




    Query Instruction (5 notes):
    1. Not select attribute `images`, `sku` while in the SQL statements. You are encouraged to join the product_line and product tables together in the SQL query.
    2. Check and change case sensitive of the user's query to match the given keywords have been provided to you (supplier and category, for example: LOGITECH change to logitech, Laptop change to laptop).
    3. Check and compare user's keyword to match the attribute keywords have been provided to you (supplier and category, for example: user keyword - hp laptop, supplier keyword - hp, category keyword - laptop).
    4. In case need to query N records of data, select limit upto 5.
    5. Priority to use ILIKE operator in the query statement rather than simply LIKE.

    


    Some basic example output:
    SELECT * FROM product LIMIT 5;
    SELECT product.name, product.price, product_line.category, product.quantity FROM product INNER JOIN product_line ON product.product_line=product_line.id LIMIT 5;

    


    Please note that you should not make up or guess any additional information or additional newline when generating the SQL query.
    """
    )

    qa_chain = prompt | model | OpenAIFunctionsAgentOutputParser()
    res = qa_chain.invoke({"input": query})
    print(res.return_values['output'])

    product_data = get_product_data(res.return_values['output'])

    print(f"PRODUCT DATA FOUND: {product_data} - end.")

    return product_data
