import os
import json
import re

def update_readme():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        return

    # Load analysis data
    try:
        with open(".github/data/repo_analysis.json", "r") as f:
            analysis = json.load(f)
    except Exception:
        analysis = {"languages": [], "frameworks": [], "build_tools": []}

    try:
        with open(".github/data/ai_documentation.json", "r") as f:
            ai_doc = json.load(f)
    except Exception:
        ai_doc = {"repository_summary": "", "architectural_insights": ""}

    try:
        with open("docs/architecture/architecture.mmd", "r") as f:
            mermaid_arch = f.read()
    except Exception:
        mermaid_arch = ""

    # Build the injected content
    injected_content = "\n## 🤖 Auto-Generated Repository Status\n\n"
    injected_content += "> This section is automatically maintained by the repository AI agent.\n\n"

    injected_content += "### 📊 Technology Stack\n"
    injected_content += f"- **Languages:** {', '.join(analysis.get('languages', []))}\n"
    injected_content += f"- **Frameworks:** {', '.join(analysis.get('frameworks', []))}\n"
    injected_content += f"- **Build Tools:** {', '.join(analysis.get('build_tools', []))}\n\n"

    injected_content += "### 🧠 AI Repository Summary\n"
    injected_content += f"{ai_doc.get('repository_summary', '')}\n\n"
    injected_content += f"**Architectural Insights:** {ai_doc.get('architectural_insights', '')}\n\n"

    injected_content += "### 🗺️ System Architecture\n"
    if mermaid_arch:
        injected_content += f"```mermaid\n{mermaid_arch}\n```\n"

    # Read original README
    with open(readme_path, "r") as f:
        content = f.read()

    # Define markers
    start_marker = "<!-- AUTODOC_START -->"
    end_marker = "<!-- AUTODOC_END -->"

    if start_marker in content and end_marker in content:
        # Replace existing section
        pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
        new_content = pattern.sub(f"{start_marker}\n{injected_content}\n{end_marker}", content)
    else:
        # Append to end of README
        new_content = content + f"\n\n{start_marker}\n{injected_content}\n{end_marker}\n"

    # Write back
    with open(readme_path, "w") as f:
        f.write(new_content)

    print("README updated successfully.")

if __name__ == "__main__":
    update_readme()
