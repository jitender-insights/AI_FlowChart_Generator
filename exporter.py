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
    graph_code = dot_code
    if fmt == "png":
        # Inject DPI setting into DOT code for higher quality PNG
        lines = dot_code.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("graph") or line.strip().startswith("digraph"):
                # Insert dpi after opening bracket
                if "{" in line:
                    idx = line.index("{") + 1
                    lines[i] = line[:idx] + "\ngraph [dpi=200];" + line[idx:]
                else:
                    lines[i] = line + " {\ngraph [dpi=200];"
                break
        graph_code = "\n".join(lines)
    graph = Source(graph_code)
    graph.format = fmt
    if fmt == "png":
        png_path = path + ".png"
        png_bytes = graph.pipe(format="png")
        with open(png_path, "wb") as f:
            f.write(png_bytes)
        return png_path
    return graph.render(path, cleanup=True)
