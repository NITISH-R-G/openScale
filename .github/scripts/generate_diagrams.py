import os
import json

def generate_diagrams():
    analysis_file = ".github/data/repo_analysis.json"
    if not os.path.exists(analysis_file):
        print("Analysis file not found. Run analyze_repo.py first.")
        return

    with open(analysis_file, "r") as f:
        analysis = json.load(f)

    # 1. Generate Architecture Overview (Mermaid)
    mermaid_arch = "```mermaid\ngraph TD;\n"
    mermaid_arch += "    Repo[Repository] --> Docs[Documentation];\n"

    if "Android" in analysis["frameworks"]:
        mermaid_arch += "    Repo --> AndroidApp[Android App];\n"
        mermaid_arch += "    AndroidApp --> UI[UI Layer];\n"
        mermaid_arch += "    AndroidApp --> Core[Core Layer];\n"
        mermaid_arch += "    Core --> DB[Database];\n"
        mermaid_arch += "    Core --> BT[Bluetooth];\n"

    if "C/C++ (Arduino)" in analysis["languages"]:
        mermaid_arch += "    Repo --> Arduino[Arduino MCU];\n"
        mermaid_arch += "    Arduino --> Scales[OpenScale MCU];\n"
        mermaid_arch += "    Arduino --> Libs[Libraries];\n"

    mermaid_arch += "```"

    # 2. Generate CI/CD Workflow Diagram
    mermaid_ci = "```mermaid\ngraph LR;\n"
    mermaid_ci += "    Push[Code Push] --> Tests[Run Tests];\n"
    mermaid_ci += "    Push --> Analysis[Analyze Repo];\n"
    mermaid_ci += "    Analysis --> Graph[Update Knowledge Graph];\n"
    mermaid_ci += "    Graph --> Diagrams[Generate Diagrams];\n"
    mermaid_ci += "    Diagrams --> AI[AI Documentation Agent];\n"
    mermaid_ci += "    AI --> Readme[Update README];\n"
    mermaid_ci += "    Readme --> Commit[Commit Changes];\n"
    mermaid_ci += "```"

    # Save diagrams to files
    os.makedirs("docs/architecture", exist_ok=True)
    with open("docs/architecture/architecture.mmd", "w") as f:
        f.write(mermaid_arch.strip("`mermaid\n").strip("`"))

    with open("docs/architecture/cicd.mmd", "w") as f:
        f.write(mermaid_ci.strip("`mermaid\n").strip("`"))

    print("Diagrams generated successfully.")

if __name__ == "__main__":
    generate_diagrams()
