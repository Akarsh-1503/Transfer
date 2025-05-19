from swarm import Swarm, Agent
from openai import OpenAI
from typing import Dict, Any
import json



# Initialize OpenAI client
openai_client =

# Initialize Swarm client with OpenAI client
client = Swarm(openai_client)


class InterfaceAgent:
    
    def __init__(self):
        self.query = ""
        self.db_schema = """"
        {
            "tables": {
                "employees": {
                    "columns": {
                        "employee_id": "INTEGER PRIMARY KEY",
                        "first_name": "VARCHAR(50)",
                        "last_name": "VARCHAR(50)", 
                        "email": "VARCHAR(100)",
                        "hire_date": "DATE",
                        "department_id": "INTEGER",
                        "position_id": "INTEGER",
                        "salary": "DECIMAL(10,2)",
                        "manager_id": "INTEGER"
                    }
                },
                "departments": {
                    "columns": {
                        "department_id": "INTEGER PRIMARY KEY",
                        "department_name": "VARCHAR(100)",
                        "location": "VARCHAR(100)",
                        "budget": "DECIMAL(15,2)"
                    }
                },
                "positions": {
                    "columns": {
                        "position_id": "INTEGER PRIMARY KEY", 
                        "title": "VARCHAR(100)",
                        "min_salary": "DECIMAL(10,2)",
                        "max_salary": "DECIMAL(10,2)",
                        "level": "INTEGER"
                    }
                },
                "employee_skills": {
                    "columns": {
                        "employee_id": "INTEGER",
                        "skill_id": "INTEGER",
                        "proficiency_level": "INTEGER",
                        "date_acquired": "DATE"
                    }
                },
                "skills": {
                    "columns": {
                        "skill_id": "INTEGER PRIMARY KEY",
                        "skill_name": "VARCHAR(100)",
                        "category": "VARCHAR(50)"
                    }
                }
            },
            "relationships": [
                {
                    "from": "employees.department_id",
                    "to": "departments.department_id"
                },
                {
                    "from": "employees.position_id", 
                    "to": "positions.position_id"
                },
                {
                    "from": "employees.manager_id",
                    "to": "employees.employee_id"
                },
                {
                    "from": "employee_skills.employee_id",
                    "to": "employees.employee_id"
                },
                {
                    "from": "employee_skills.skill_id",
                    "to": "skills.skill_id"
                }
            ]
        }
        """
   
        self.agent = Agent(
            name="Interface Agent",
            instructions=f"""You are a sql query generator agent. Use the tool sql_query_generator_tool to generate a SQL query.
            """,
            model="gpt-4o",
            tools=[self.sql_query_generator_tool]
        )
        
    async def generate_agent_response(self, query):
        # Generate a response from the agent
        self.query = query
        response = client.run(
            agent=self.agent,
            messages=[{"role": "user", "content": query}],
            debug= True
        )
        print("response.messages[-1]['content']", response.messages[-1]['content'])
        return response.messages[-1]['content']

    def sql_query_generator_tool(self, query: str) -> str:
        """
        Use this tool to generate a SQL query.
        Args:
            query (str): User request which is regarding interaction with the database.
        """
        # Parse the schema
        schema = json.loads(self.db_schema.strip())
        
        # Generate SQL query using OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"""You are a SQL query generator. Generate SQL queries based on the following schema:
                {json.dumps(schema, indent=2)}
                
                Follow these rules:
                1. Use explicit column names (no SELECT *)
                2. Use proper JOIN syntax based on the relationships
                3. Use clear table aliases
                4. Return ONLY the SQL query, no explanations"""},
                {"role": "user", "content": query}
            ]
        )
        
        return response.choices[0].message.content.strip()



    # Use this agent to generate SQL queries based on natural language requests
    # This agent is responsible for converting natural language queries into valid SQL statements
    # while ensuring compliance with the database schema and relationships


    def transfer_to_sql_query_generator_agent(self):
        """
        Use this tool to transfer the query to the sql_query_generator_agent.
        """
        print("We are in transfer_to_sql_query_generator_agent")
        return self.sql_query_generator_agent
