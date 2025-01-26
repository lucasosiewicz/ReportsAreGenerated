sql_prompt_template = """
### Task
Generate a SQL query for {dbms} to answer [QUESTION]{question}[/QUESTION]

### Instructions
- Generate only SELECT queries. ABSOLUTELY DO NOT GENERATE ALTER, INSERT, DROP etc. queries
- Before You return the query, make sure that all tables are initialized.
- As an answer, return only the code.
- If you are not sure about the answer with the available database schema, return 'I do not know'.

### Database Schema
The query will run on a database with the following schema:
{schema}


### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
"""

non_sql_prompt_template = """
### Task
Generate a python code for {dbms} to answer[QUESTION]{question}[/QUESTION]

### Instructions
- Generate only queries which reads data. ABSOLUTELY DO NOT GENERATE queries which can alter or remove any data in database
- As an answer, return only the code.
- Answer MUST contain only part of code which responsible for extracting requested data from database
- Answer should not contain any connection string or imports
- Answer MUST contain pipeline and answer variable in form of pandas df
- Answer MUST use db as access point to database
- If you are not sure about the answer with the available database schema, return 'I do not know'.


### Database Schema
The query will run on a database with the following structure:
{schema}


### Answer
Given the database structure, here is the query that answers [QUESTION]{question}[/QUESTION]
"""

code_template = """
import os
import sys
print("Python executable being used:")
print(sys.executable)
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sqlalchemy import create_engine



load_dotenv('existing/{database}/.env', override=True, verbose=True)

USERNAME = os.getenv('PGUSERNAME')
PASSWORD = os.getenv('PGPASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
SERVER = os.getenv('SERVER')
DATABASE = os.getenv('NAME').replace('"', '')
URL = f'{url}'

engine = create_engine(URL)

df = pd.read_sql("{query}", engine)

{code}
"""

non_sql_code_template = """
import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from pymongo import MongoClient


load_dotenv('existing/{database}/.env', override=True, verbose=True)

USERNAME = os.getenv('PGUSERNAME')
PASSWORD = os.getenv('PGPASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
SERVER = os.getenv('SERVER')
DATABASE = os.getenv('NAME').replace('"', '')
URL = f'{url}'

client = MongoClient(URL)
db = client[DATABASE]
{query}

{code}
"""

code_prompt_template = """
### Task
Assume You are expirieced data visualisation engineer.
Write a Python code which will handle following question: [QUESTION]{question}[/QUESTION]

### Instructions
- Before You return the code, make sure that all variables are defined and you are using the correct columns and datatypes.
- Use only matplotlib for plotting.
- IN PANDAS ALWAYS USE LOWER CASES FOR COLUMN NAMES AS A KEYS!
- Always use plt.tight_layout() after plotting to ensure that the plot is not cut off.
- Always save the plot as 'plot.png' in the current directory.
- Always add legend to the plot.
- Don't show plot in the end.
- You must finish following code:
```python
import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

load_dotenv()

USERNAME = os.getenv('PGUSERNAME')
PASSWORD = os.getenv('PGPASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
SERVER = os.getenv('SERVER')
DATABASE = os.getenv('DATABASE')
URL = f'{url}'

engine = create_engine(URL)

df = pd.read_sql('{query}', engine)

# Finish your code here
```
- Don't change anything in the code above.
- Return ONLY code!

### Answer
Here is the Python code that answers [QUESTION]{question}[/QUESTION]

Begin!
"""

non_sql_code_prompt_template = """
### Task
Assume You are expirieced data visualisation engineer.
Write a Python code which will handle following question: [QUESTION]{question}[/QUESTION]

### Instructions
- Before You return the code, make sure that all variables are defined and you are using the correct columns and datatypes.
- Use only matplotlib for plotting.
- IN PANDAS ALWAYS USE LOWER CASES FOR COLUMN NAMES AS A KEYS!
- ALWAYS ENSURE that used data is numeric if such expected, if not convert to needed format
- Always use plt.tight_layout() after plotting to ensure that the plot is not cut off.
- Always save the plot as 'plot.png' in the current directory.
- Always save the plot at the end of code
- Always add legend to the plot.
- Always add title to the plot.
- If there is big amount of data increase plot size
- Don't show plot in the end.
- You must finish following code:
```python
import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from pymongo import MongoClient

load_dotenv()

USERNAME = os.getenv('PGUSERNAME')
PASSWORD = os.getenv('PGPASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
SERVER = os.getenv('SERVER')
DATABASE = os.getenv('DATABASE')
URL = f'{url}'

client = MongoClient(URL)
db = client[DATABASE]
{query}
# Finish your code here
```
- Don't change anything in the code above.
- Return ONLY code!

### Answer
Here is the Python code that answers [QUESTION]{question}[/QUESTION]

Begin!
"""