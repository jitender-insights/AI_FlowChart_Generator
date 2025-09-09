import os
import uuid
from graphviz import Source
import os
from dotenv import load_dotenv
load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_dot_file(dot_code: str) -> str:
    path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}.dot")
    with open(path, "w") as f:
        f.write(dot_code)
    return path

def render_dot(dot_code: str, fmt: str = "png") -> str:
    base_name = f"{uuid.uuid4().hex}"
    path = os.path.join(OUTPUT_DIR, base_name)
    graph = Source(dot_code)
    graph.format = fmt
    return graph.render(path, cleanup=True)
