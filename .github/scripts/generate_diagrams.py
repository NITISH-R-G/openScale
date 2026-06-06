import os
import json

def generate_diagrams():
    kg_file = ".github/data/knowledge_graph.json"
    if not os.path.exists(kg_file):
        print("Knowledge graph file not found. Run knowledge_graph.py first.")
        return

    with open(kg_file, "r") as f:
        graph = json.load(f)

    # 1. Generate Architecture Overview dynamically from knowledge graph
    mermaid_arch = "```mermaid\ngraph TD;\n"
    mermaid_arch += "    root[Repository];\n"

    # Add nodes
    for node in graph["nodes"]:
        mermaid_arch += f"    {node['id']}[{node['label']}];\n"

    # Add edges
    for edge in graph["edges"]:
        mermaid_arch += f"    {edge['source']} -->|{edge['relation']}| {edge['target']};\n"

    mermaid_arch += "\n    %% Clickable Links\n"
    for node in graph["nodes"]:
        if "path" in node:
            mermaid_arch += f"    click {node['id']} href \"./{node['path']}\"\n"

    mermaid_arch += "```"

    # 2. Generate CI/CD Workflow Diagram
    mermaid_ci = "```mermaid\ngraph LR;\n"
    mermaid_ci += "    Push[Code Push] --> Tests[Run Tests];\n"
    mermaid_ci += "    Tests --> Lint[Run Linting];\n"
    mermaid_ci += "    Lint --> Deps[Dependency Audit];\n"
    mermaid_ci += "    Deps --> Analysis[Analyze Repo];\n"
    mermaid_ci += "    Analysis --> Graph[Update Knowledge Graph];\n"
    mermaid_ci += "    Graph --> Diagrams[Generate Diagrams];\n"
    mermaid_ci += "    Diagrams --> AI[AI Documentation Agent];\n"
    mermaid_ci += "    AI --> Readme[Update README];\n"
    mermaid_ci += "    Readme --> Commit[Commit Changes];\n"
    mermaid_ci += "```"

    # Save diagrams to files
    os.makedirs("docs/architecture", exist_ok=True)
    with open("docs/architecture/architecture.mmd", "w") as f:
        f.write(mermaid_arch.replace("```mermaid\n", "", 1).replace("```", ""))

    with open("docs/architecture/cicd.mmd", "w") as f:
        f.write(mermaid_ci.replace("```mermaid\n", "", 1).replace("```", ""))

    print("Dynamic diagrams generated successfully.")

if __name__ == "__main__":
    generate_diagrams()
