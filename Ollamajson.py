import websocket
import uuid
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
import sys
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import OutputFixingParser
from typing import Annotated, List, Sequence, Tuple, TypedDict, Union
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
)
from text2image import call_text_to_imagen
from cambio import *
import operator
import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = "ls__6d685e614085499b93d8358895005721"


class Generar_prompt_new(BaseModel):
    prompt_new: str = Field(description="improved prompt")



parser_res = JsonOutputParser(pydantic_object=Generar_prompt_new)

llm = Ollama(model="eas/nous-hermes-2-solar-10.7b",temperature=0)
#llm = Ollama(model="dolphin-mixtral",temperature=0)
#llm = Ollama(model="nous-hermes2-mixtral")

enhance_prompt = PromptTemplate(
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
   
    User input: {input}

    the output is always in English even though the input is in Spanish
    condense all that information into a single medium-sized prompt
    only returns the improved prompt in english
    Answer a JSON object with the following format instructions: '{format_instructions}'

    """,
    input_variables=["input"],
    partial_variables={"format_instructions": parser_res.get_format_instructions()},
)
chain_enhance_prompt = enhance_prompt | llm | parser_res
def generar_prompt_new(input:str) -> Generar_prompt_new:
    res = chain_enhance_prompt.invoke({"input": input})
    return res
def generar_prompt_new_node(state):
    messages = state["messages"]
    last_message_content = messages[-1].content  # Asumiendo que last_message es una instancia de BaseMessage
    new_prompt = generar_prompt_new(last_message_content)
    new_message = HumanMessage(content=new_prompt["prompt_new"])
    return {"messages": [new_message]} 


"""
new= generar_prompt_new("retrato de un hombre deprimido pintado por david hume, lsd psicodelia horror, shok")
print(new)
print(new["prompt_new"])
"""

request_handler =PromptTemplate(
    template="""
    <|system|>
    - Detect intent based on user input to either enhance a message, generate an image from text, or convert an image into text.
    - Utilize specific keywords or prompts to identify user intent accurately.
    - Ensure the response concludes with one of the following directives: "enhance_prompt", "text_to_image", "image_to_image" or "Fallback".
    <|user|>
    Determine the primary user intent from the input: enhance a message, create an image from text, or describe an image in text. User input: "{input}"

    Intent guidelines:
        - "enhance_prompt": When the user seeks to add details or creativity to their message. Look for keywords: improve, enhance.
        - "text_to_image": If the user wants to generate an image based on their text. Triggered by the intent to create, crea or imagine.
        - "image_to_image": If the user wants to generate an image based on their image, indicated by an image path  (e.g., "C:\\path\\image.png")
        - "fallback": For queries that do not fit the other categories. This could include providing suggestions, answering questions, or any creative response not covered by the other directives.


    Actions:
        - Enhance messages for more creativity.
        - Generate images from text prompts.
        - Convert images into descriptive text.
        - Route any other intent to the fallback.

    For other queries, provide a creative response or suggestions for image generation.

    Always conclude the response with a directive: "enhance_prompt", "text_to_image", "image_to_image", or "fallback" . skip any comments, just return the keyword
    <|assistant|>
    """,
    input_variables=["input"],
)
chain_request_handler = request_handler | llm 

def generar_request_handler (input:str):
    res = chain_request_handler .invoke({"input": input})
    return res

def router_node (state):
    messages = state["messages"]
    last_message_content = messages[-1].content
    handler=generar_request_handler(last_message_content)
    print(handler)
    return {"sender": handler}

def router_aux (state):
    agente= state["sender"]
    
    if "text_to_image" in agente:
        return "text_to_image"
    elif "image_to_image" in agente:
        return "image_to_image"
    elif "enhance_prompt" in agente:
        return "enhance_prompt"
    elif "fallback" in agente:
        return "fallback"
    
def ocupado(state):
    agente = state.get("sender")  # Use .get() to safely access the dictionary
    if agente is None:
        return "router"  # Or any other appropriate handling
    elif "image_to_image" in agente:
        return "image_to_image"
    else:
        return "router"
    
def ocupado_node(state):
    agente= state["sender"]
    print(agente)
    return {"work":agente}



#print(generar_request_handler("create a cute cat"))


def text2image_node(state):
    messages = state["messages"]
    last_message_content = messages[-1].content
    new= generar_prompt_new(last_message_content)
    new2=new["prompt_new"]
    id=generate_random_15_digit_number()
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\image_{id}"
    limite= 1
    json_output_path = "output3.json"

    path_image=call_text_to_imagen(new2,directory_path,id,limite,json_output_path)
    new_message = HumanMessage(content=path_image)
    return {"messages": [new_message]} 

def fallback_node(state):
    new_message = HumanMessage(content="fallback")
    return {"messages": [new_message]} 

def pedir_descripcion_imagen():
    descripcion = input(pregunta="¿comó quieres cambiar a la persona? ")
    return descripcion

def pedir_descripcion_fondo():
    descripcion = input(pregunta2="¿qué fondo quieres para la imagen? ")
    return descripcion

def image_to_image(state):

    image_path = state['image_path']
    prompt_persona = state['prompt_persona']
    prompt_fondo = state['prompt_fondo']
    print(image_path)
    print(prompt_persona)
    print(prompt_fondo)
    
    # Comprobar y solicitar cada parámetro en secuencia.
    if image_path is None:
        messages = state["messages"]
        image_path  = messages[-1].content 
        return {"messages": ["¿Cómo quieres cambiar a la persona en la imagen?"],"sender":"image_to_image","image_path":image_path}
    
    if prompt_persona is None:
        messages = state["messages"]
        prompt_persona  = messages[-1].content 
        return {"messages": ["¿Qué fondo quieres para la imagen?"],"sender":"image_to_image","prompt_persona":prompt_persona}

    if prompt_fondo  is None:
        # Supone que el último mensaje contiene la descripción del fondo.
        messages = state["messages"]
        prompt_fondo  = messages[-1].content 
        # Aquí todos los parámetros necesarios están disponibles.
        # Esta es la llamada a la función final de transformación de imagen, que debe definirse en otro lugar.
        """
        new_prompt= generar_prompt_new(prompt_persona)
        new_prompt2=new_prompt["prompt_new"]
        new_prompt_fondo= generar_prompt_new(prompt_fondo)
        new_prompt2_fondo=new_prompt_fondo["prompt_new"]
        """
        
        id=generate_random_15_digit_number()
        resultado =cambio_multiples_caras(image_path,id,prompt_persona,prompt_fondo)
        print(resultado)
        resultado=resultado["1"]
        # Puedes decidir resetear el estado aquí si eso se ajusta a tu flujo de trabajo.
        return {"messages": [resultado],"sender":None,"prompt_fondo":prompt_fondo}

    # Si se alcanza este punto sin entrar en ninguna condición anterior, se asume que hay un error lógico.
    return {"messages": [ "Error inesperado. Todos los parámetros ya fueron proporcionados."]}




from langchain.tools.render import format_tool_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str
    work: str
    image_path: str
    prompt_persona: str
    prompt_fondo: str


workflow = StateGraph(AgentState)

workflow.add_node("ocupado", ocupado_node)
workflow.add_node("image_to_image", image_to_image)
workflow.add_node("fallback", fallback_node)

workflow.add_node("enhance_prompt", generar_prompt_new_node)
workflow.add_node("router", router_node)
workflow.add_node("text_to_image", text2image_node)
workflow.add_edge("enhance_prompt", END)
workflow.add_edge("text_to_image", END)
workflow.add_edge("image_to_image", END)
workflow.add_edge("fallback", END)
workflow.add_conditional_edges("router", router_aux, {
    "enhance_prompt": "enhance_prompt",
    "text_to_image": "text_to_image",
    "image_to_image": "image_to_image",
    "fallback": "fallback",
})
workflow.add_conditional_edges("ocupado", ocupado, {
    "image_to_image": "image_to_image",
    "router": "router",
})

workflow.set_entry_point("ocupado")

graph = workflow.compile()



from typing import List, Sequence, TypedDict, Annotated
from langchain_core.messages import HumanMessage, BaseMessage

# Asumiendo que todos los imports y configuraciones necesarias han sido realizados anteriormente

class ChatSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.workflow = workflow.compile()
        self.state = {"messages": [], "sender": None,"work":None,"image_path":None, "prompt_persona": None, "prompt_fondo": None}

    def handle_message(self, message,pendiente,image_path,prompt_persona,prompt_fondo):
        #self.state["messages"].append(HumanMessage(content=message))
        
        for new_state in self.workflow.stream(
            {
                "messages": [
                    HumanMessage(
                        content=message
                    )
                ],
                "sender":pendiente,
                "image_path":image_path,
                "prompt_persona":prompt_persona,
                "prompt_fondo":prompt_fondo,
            },
            {"recursion_limit": 150},
        ):
            print(new_state)
            print("----")
            self.state = new_state  
        
        if self.state and '__end__' in self.state:
            # Assuming all messages are either strings or have a .content attribute
            ultimo_mensaje = self.state['__end__']['messages'][-1]
            if isinstance(ultimo_mensaje, HumanMessage):  # Check if it's an instance of HumanMessage
                ultimo_mensaje = ultimo_mensaje.content
            elif not isinstance(ultimo_mensaje, str):  # Add more checks here if there are other possible types
                # Handle unexpected type
                print("Unexpected message type:", type(ultimo_mensaje))
                ultimo_mensaje = "Error: Unexpected message type."

            pendiente = self.state['__end__']['sender']
            image_path = self.state['__end__']['image_path']
            prompt_persona = self.state['__end__']['prompt_persona']
            prompt_fondo= self.state['__end__']['prompt_fondo']

            return ultimo_mensaje, pendiente, image_path,prompt_persona,prompt_fondo

active_sessions = {}

def get_session(user_id):
    if user_id not in active_sessions:
        active_sessions[user_id] = ChatSession(user_id)
    return active_sessions[user_id]

def chat_with_user(user_id, message, pendiente, image_path, prompt_persona, prompt_fondo):
    session = get_session(user_id)
    response, pendiente, image_path, prompt_persona, prompt_fondo = session.handle_message(message, pendiente, image_path, prompt_persona, prompt_fondo)
    return response, pendiente, image_path, prompt_persona, prompt_fondo

def call_graph(user_id, user_input, state):
    # Desempaqueta los valores del estado; si no existen, se inicializan como None
    pendiente = state.get('pendiente', None)
    image_path = state.get('image_path', None)
    prompt_persona = state.get('prompt_persona', None)
    prompt_fondo = state.get('prompt_fondo', None)
    
    # Suponiendo que chat_with_user devuelve los valores actualizados para estos parámetros
    response, pendiente, image_path, prompt_persona, prompt_fondo = chat_with_user(
        user_id, user_input, pendiente, image_path, prompt_persona, prompt_fondo
    )
    
    # Actualiza el estado con los nuevos valores
    state['pendiente'] = pendiente
    state['image_path'] = image_path
    state['prompt_persona'] = prompt_persona
    state['prompt_fondo'] = prompt_fondo
    
    print(f"pendiente {pendiente}")
    print(image_path)
    print(prompt_persona)
    print(prompt_fondo)
    
    print("Bot:", response or "Lo siento, no entendí tu solicitud.")
    
    # Devuelve la respuesta y el estado actualizado
    return response, state
if __name__ == "__main__":

    print(active_sessions)
    print("Bienvenido a la aplicación de chat. Escribe 'salir' para terminar.")

    user_id = "user1"
    estado_inicial = {}

    while True:
        user_input = input("Tú: ")
        a=call_graph(user_id,user_input,estado_inicial)
        print(a)
                

"""

for s in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="crea la imagen de un demonio satanico"
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 150},
):
    print(s)
    print("----")

"""

"""
user_workflows = {}

def handle_user_message(user_id, message):
    # Verifica si el usuario ya tiene un flujo de trabajo iniciado.
    if user_id not in user_workflows:
        # Si no, crea una nueva instancia del flujo de trabajo para este usuario.
        user_workflows[user_id] = workflow.compile()

    # Obtiene el flujo de trabajo del usuario.
    user_graph = user_workflows[user_id]

    # Define una variable para almacenar el último estado.
    ultimo_estado = None

    # Procesa el mensaje a través del flujo de trabajo del usuario.
    for state in user_graph.stream(
        {"messages": [HumanMessage(content=message)]},
        {"recursion_limit": 150},
    ):
        print(state)
        # Guarda el estado actual como el último estado procesado.
        ultimo_estado = state
        print("----")

    # Verifica si el último estado contiene mensajes y extrae el contenido del último mensaje.
    if ultimo_estado and '__end__' in ultimo_estado:
        ultimo_mensaje = ultimo_estado['__end__']['messages'][-1].content
        print("Mensaje final:", ultimo_mensaje)
    else:
        print("No se encontró el mensaje final.")

# Ejemplo de cómo manejar mensajes de diferentes usuarios.
handle_user_message("user_1", "crea la imagen de una criatura alien, en lsd, impresionista")
"""

"""
user_message = "Crea la imagen de un demonio satánico"
user_id = "user_123"  # Identificador único para el usuario.
response = chat_with_user(user_id, user_message)
print("Respuesta:", response)
"""

