from openai import OpenAI
from typing import Dict, Any

def sql_query_generator_tool(query: str) -> str:
    """
    Generates a SQL query from a natural language request using OpenAI's GPT model.
    
    This tool converts natural language queries into valid SQL statements while ensuring
    proper syntax, schema compliance, and query optimization. It handles various types
    of database operations including SELECT, INSERT, UPDATE, and DELETE statements.
    
    Args:
        query (str): A natural language description of the desired database query.
                    Example: "Find all employees in the IT department with a salary above 50000"
    
    Returns:
        str: A valid SQL query string that accomplishes the requested operation.
             The query will be properly formatted and include appropriate joins,
             where clauses, and other necessary SQL components.
    
    Raises:
        ValueError: If the input query is empty or cannot be processed
        OpenAIError: If there's an error in communicating with the OpenAI API
    
    Example:
        >>> query = "Find all employees in the IT department"
        >>> sql_query_generator_tool(query)
        SELECT e.employee_id, e.first_name, e.last_name
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id
        WHERE d.department_name = 'IT';
    """
    if not query.strip():
        raise ValueError("Query string cannot be empty")
        

    client =

    messages = [
        {
            "role": "system",
            "content": """You are a specialized SQL query generator. Your task is to:
1. Analyze the natural language request
2. Generate a syntactically correct SQL query
3. Ensure proper table relationships and joins
4. Implement appropriate filtering and sorting
5. Follow SQL best practices and optimization guidelines

Please generate clear, efficient, and secure SQL queries that:
- Use explicit column names (no SELECT *)
- Include appropriate table aliases
- Implement proper JOIN conditions
- Use efficient WHERE clauses
- Handle NULL values appropriately
- Follow consistent formatting"""
        },
        {"role": "user", "content": query}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        
        generated_query = response.choices[0].message.content
        return generated_query
        
    except Exception as e:
        raise Exception(f"Error generating SQL query: {str(e)}")
