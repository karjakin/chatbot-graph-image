from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
import sys
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = "ls__6d685e614085499b93d8358895005721"
template = """
Identify the Central Theme: Determine the main subject of the original prompt.

Add Specific Details: Enrich the prompt with specific details about the main subjects, such as color, shape, activity, expression.

Introduce Context Elements: Add background or context elements that complement the scene without diverting attention from the main subject.

Vary Perspective and Composition: Suggest different camera angles, focal lengths or compositions to give a new dimension to the prompt.

Maintain Style Consistency: Make sure the added details align with the style and tone of the original prompt (e.g., realistic, whimsical, abstract).

Avoid Changing the Original Theme: Do not alter the central theme of the prompt, only enrich what is already present.

Include Diversification and Avoid Biases: Make sure that representations of people are diverse and avoid stereotypes or biases.

Respect Ethical and Legal Guidelines: Avoid adding elements that may be offensive, problematic 

With these instructions, any language model can improve simple prompts for image generation, making them more detailed, rich, and visually interesting.
the output is always in English even though the input is in Spanish
condense all that information into a single medium-sized prompt
only returns the improved prompt in english
User input: {input}
"""
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_template(template)
llm = Ollama(model="command-r:latest")
#llm = Ollama(model="nous-hermes2-mixtral")
chain = ({"input": RunnablePassthrough()}
    | prompt 
    | llm
    | output_parser
         ) 
print(chain.invoke("un doctor en la jungla"))
# Call the function to stream the response
#stream_ollama_response(query)
