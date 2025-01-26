import os
import subprocess
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from static.prompts import sql_prompt_template, non_sql_prompt_template, code_prompt_template, non_sql_code_prompt_template
from static.urls import URL

load_dotenv()

class Plotter:
    def __init__(self):

        self.model = ChatOpenAI(model='gpt-3.5-turbo', api_key=os.getenv('OPENAI_API_KEY'))
                                        
        self.sql_prompt = PromptTemplate.from_template(sql_prompt_template)
        self.sql_chain = self.sql_prompt | self.model
            
        self.code_prompt = PromptTemplate.from_template(code_prompt_template)
        self.code_chain = self.code_prompt | self.model


    # ========================= PUBLIC METHODS ========================= #
    def generate_sql_query(self, question: str, database: str, dbms: str) -> str:

        if dbms.startswith('Mongo'):
            schema = self._fetch_metadata(f'existing/{database}/metadata.txt')
        else:
            schema = self._fetch_metadata(f'existing/{database}/metadata.sql')
        self.update_plotter_templates(dbms)


        sql_query = self.sql_chain.invoke({
            'question': question,
            'schema': schema,
            'dbms': dbms


            
        }).content

        if dbms.startswith('Oracle'):
            return sql_query.replace(';', '').strip(' ')
        else:
            return sql_query

        # return sql_query if not dbms.startswith('Oracle') else sql_query.replace(';', '').strip(' ')

    def generate_code(self, question: str, sql_query: str, dbms: str) -> str:

        if dbms.startswith('Mongo'):
            query = sql_query.replace('```python', '').replace('```', '')
        else:
            query = sql_query.replace('```sql', '').replace('```', '').replace('\n', ' ')

        code = self.code_chain.invoke({
            'question': question,
            'query': query,
            'url': URL[dbms]
        })

        return code.content
    
    def execute_code(self, file_path: str, code_template: str, sql_query: str, code: str, database: str, dbms:str) -> None:

        if dbms.startswith('Mongo'):
            query = sql_query.replace('```python', '').replace('```', '')
        else:
            query = sql_query.replace('```sql', '').replace('```', '').replace('\n', ' ').replace('         ', ' ')

        code_template = code_template.format(
            query=query,
            code=code.replace('```python', '').replace('```', ''),
            database=database,
            url=URL[dbms]
        )

        print(code_template)
        with open(file_path, 'w') as f:
            f.write(code_template)

        # result = subprocess.run(['python', file_path], stderr=subprocess.PIPE)
        # Using venv python
        result = subprocess.run(["../../venv/Scripts/python.exe", 'plot.py'], stderr=subprocess.PIPE)
        main
        os.remove(file_path)

        print(result.stderr.decode('windows-1252'))

        return result.stderr, len(result.stderr)

    
    # ========================= PRIVATE METHODS ========================= #

    def update_plotter_templates(self, dbms: str) -> None:
        if dbms.startswith('Mongo'):
            self.sql_prompt = PromptTemplate.from_template(non_sql_prompt_template)
            self.sql_chain = self.sql_prompt | self.model

            self.code_prompt = PromptTemplate.from_template(non_sql_code_prompt_template)
            self.code_chain = self.code_prompt | self.model
        else:
            self.sql_prompt = PromptTemplate.from_template(sql_prompt_template)
            self.sql_chain = self.sql_prompt | self.model

            self.code_prompt = PromptTemplate.from_template(code_prompt_template)
            self.code_chain = self.code_prompt | self.model

    def _fetch_metadata(self, file_path: str) -> str:
        with open(file_path, 'r') as f:
            return f.read()

    