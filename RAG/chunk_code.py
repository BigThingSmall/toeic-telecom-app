import ast
import os

def extract_chunks_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    lines = source.splitlines()

    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = node.end_lineno

            code = "\n".join(lines[start:end])

            chunks.append({
                "code": code,
                "name": node.name,
                "type": type(node).__name__,
                "file": filepath
            })

    return chunks


def load_project(folder):
    all_chunks = []

    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                all_chunks.extend(extract_chunks_from_file(path))

    return all_chunks