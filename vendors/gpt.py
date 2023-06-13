import openai

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from config import settings


chat = ChatOpenAI(
    temperature=.7,
    openai_api_key=settings.openai_api_key,
    model_name='gpt-4'
)


class GPTAPI:
    def __init__(self):
        pass
                
    def get_sql_query(self, question: str, database_schema: dict):
        # How you would like your reponse structured. This is basically a fancy prompt template
        response_schemas = [
            ResponseSchema(name="sql_query", description="SQL query that counts user question"),
        ]
        # How you would like to parse your output
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        messages = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template('''
You are ChartWizard, AI assistant helping with creating SQL queries.
Here is postgres database schema in json:
```json
{database_schema}
```
Your task is provide sql that will answer user question.
Include all necessary table joins.
            '''),
            HumanMessagePromptTemplate.from_template('''
{format_instructions}

% USER INPUT:
{question}
            ''')
        ]).format_prompt(
            database_schema=database_schema,
            question=question,
            format_instructions=output_parser.get_format_instructions()
        ).to_messages()
        resp = chat(messages)
        return output_parser.parse(resp.content)['sql_query']