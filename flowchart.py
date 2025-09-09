from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


prompt = PromptTemplate.from_template("""
You are an expert system that converts natural language descriptions of processes or workflows into Graphviz DOT code for generating flowcharts. Your output must be valid Graphviz DOT code, strictly adhering to these guidelines:

1. Graph Structure:
   - Use a directed graph (digraph) named Flowchart unless a different name is specified in the description.
   - Set the rank direction to LR (left-to-right) unless specified otherwise.
   - Apply consistent styling:
     - Graph: bgcolor="#f7f7f7", fontname="Arial", fontsize="12".
     - Nodes: shape="box", style="filled", fillcolor="#e0e0e0", fontname="Arial", fontsize="10", margin="0.2,0.1", ranksep="1.5", nodesep="0.5", fontcolor="#333333", penwidth="1.5", color="#333333".
     - Edges: fontname="Arial", fontsize="8", fontcolor="#666666", color="#666666".
   - Use cylinder shape for nodes representing final outputs (e.g., exported files like PNG, PDF).

2. Subgraphs:
   - Always group related nodes into subgraphs (clusters) when the description implies distinct modules, components, or stages (e.g., UI, backend, processing, input/output).
   - Assign each subgraph a unique name with a cluster_ prefix (e.g., cluster_ui, cluster_backend) and a descriptive label (e.g., "User Interface", "Backend Processing").
   - Use distinct fillcolor values for each subgraph to visually differentiate them:
     - User Interface (UI) or input-related: fillcolor="#d9f3ff".
     - Backend or processing-related: fillcolor="#fff0e0".
     - Output or export-related: fillcolor="#e6ffe6".
     - Other modules: Choose a distinct color (e.g., #f0e6ff, #ffe6f0) or cycle through these colors for additional subgraphs.
   - Ensure each subgraph has style="filled" to apply the background color.

3. Nodes and Edges:
   - Create nodes for each step, component, or entity in the process.
   - Use concise, descriptive labels for nodes (e.g., "User Input", "Generate Code"), keeping text short to fit within boxes.
   - Define edges to represent the flow of the process, adding labels to describe actions or transitions (e.g., "Sends", "Generates").
   - Ensure nodes and edges reflect the sequence and relationships described in the input.

4. Output Handling:
   - For export or output steps (e.g., "export as PNG", "save as PDF"), create nodes with shape="cylinder" and appropriate labels (e.g., "Exported PNG").
   - Connect these nodes to the relevant process step with labeled edges (e.g., label="PNG").

5. Input Interpretation:
   - Carefully analyze the description to identify distinct steps, components, or modules and their relationships.
   - If the description is vague, infer logical modules (e.g., input, processing, output) and group them into subgraphs with appropriate fillcolor values.
   - If specific styling or structural preferences (e.g., colors, shapes, or rank direction) are mentioned, incorporate them; otherwise, follow the default guidelines.
   - For complex descriptions, prioritize clarity by creating a simple, logical flowchart.

6. Example:
   Input: "A user enters a process description in a web interface. The system uses an LLM to generate DOT code. The DOT code is rendered as a flowchart. The user can export the flowchart as PNG or PDF."
   Expected Output:
User Description:
{user_input}

Output:
Provide only the valid Graphviz DOT code, enclosed in a code block (```), without additional explanations or comments unless requested.
""")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Create the chain using LCEL (LangChain Expression Language)
chain = prompt | llm | StrOutputParser()

# ai-flowchart-generator
def generate_dot_code(user_input: str) -> str:
    raw_output = chain.invoke({"user_input": user_input})
    # Remove Markdown code fences if present
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]  # Get content between first pair of ```
        # Optionally, remove 'dot' language tag if present
        if cleaned.strip().startswith("dot"):
            cleaned = cleaned.strip()[3:].strip()
    return cleaned