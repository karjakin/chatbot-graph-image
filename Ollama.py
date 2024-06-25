from langchain_community.llms import Ollama
import sys

def stream_ollama_response(query):
    """
    Streams the response from an Ollama model for a given query in real-time.
    
    Each chunk of the response is printed as soon as it's received, allowing the user to read the response
    continuously as it's being generated. Each chunk is printed on the same line to maintain
    a continuous flow of text.
    
    Parameters:
        query (str): The user input or question to send to the model.
    """
    # Initialize the Ollama model, specify the model name if necessary
    llm = Ollama(model="command-r")
    
    # Stream the response from the model
    for chunk in llm.stream(query):
        # Print each chunk immediately without adding a new line at the end.
        # 'flush=True' ensures that each chunk is printed to the console immediately.
        print(chunk, end='', flush=True)

# Define the query
query = """
tools = [
    {
        "name": "query_daily_sales_report",
        "description": "Connects to a database to retrieve overall sales volumes and sales information for a given day.",
        "parameter_definitions": {
            "day": {
                "description": "Retrieves sales data for this day, formatted as YYYY-MM-DD.",
                "type": "str",
                "required": True
            }
        }
    },
    {
        "name": "query_product_catalog",
        "description": "Connects to a a product catalog with information about all the products being sold, including categories, prices, and stock levels.",
        "parameter_definitions": {
            "category": {
                "description": "Retrieves product information data for all products in this category.",
                "type": "str",
                "required": True
            }
        }
    }
]preamble =
## Task & Context
You help people answer their questions and other requests interactively. You will be asked a very wide array of requests on all kinds of topics. You will be equipped with a wide range of search engines or similar tools to help you, which you use to research your answer. You should focus on serving the user's needs as best you can, which will be wide-ranging.

## Style Guide
Unless the user asks for a different style of answer, you should answer in full sentences, using proper grammar and spelling.

# user request
message = "Can you provide a sales summary for 29th September 2023, and also give me some details about the products in the 'Electronics' category, for example their prices and stock levels?"


"""


# Call the function to stream the response
stream_ollama_response(query)
