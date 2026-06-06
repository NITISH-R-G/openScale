import os
import json
from pathlib import Path

def build_knowledge_graph():
    graph = {
        "nodes": [],
        "edges": []
    }

    root_dir = "."
    module_dirs = []

    # Dynamically find top-level modules based on build files or significant directories
    for entry in os.scandir(root_dir):
        if entry.is_dir() and not entry.name.startswith('.'):
            # Check if directory has build files or is a known source dir
            has_build_files = any(os.path.exists(os.path.join(entry.path, f)) for f in ["build.gradle", "build.gradle.kts", "CMakeLists.txt", "Makefile"])
            is_significant = entry.name in ["docs", "fastlane", "arduino_mcu"]

            if has_build_files or is_significant:
                module_dirs.append(entry.name)

                node_type = "module"
                if entry.name == "docs": node_type = "docs"
                if entry.name == "fastlane": node_type = "deployment"

                graph["nodes"].append({
                    "id": entry.name,
                    "label": entry.name.replace("_", " ").title(),
                    "type": node_type,
                    "path": os.path.relpath(entry.path, root_dir).replace('\\', '/')
                })

                relation = "documents" if node_type == "docs" else "contains"
                graph["edges"].append({
                    "source": "root",
                    "target": entry.name,
                    "relation": relation
                })

    # Dynamically search for deeper components (e.g., core packages, libraries)
    for mod in module_dirs:
        for dirpath, dirnames, filenames in os.walk(mod):
            # Skip hidden and build dirs
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['build', 'tmp', 'schemas']]

            # Identify components by looking for specific directory names that indicate architecture
            path_parts = Path(dirpath).parts
            if "core" in path_parts or "libraries" in path_parts:
                comp_name = path_parts[-1]
                # Avoid adding too many nodes, only add top-level core components
                if len(path_parts) > 1 and path_parts[-2] in ["core", "libraries"]:
                    comp_id = f"{mod}_{comp_name}"
                    graph["nodes"].append({
                        "id": comp_id,
                        "label": comp_name.title() + " Component",
                        "type": "component",
                        "path": os.path.relpath(dirpath, root_dir).replace('\\', '/')
                    })
                    graph["edges"].append({
                        "source": mod,
                        "target": comp_id,
                        "relation": "implements"
                    })

    os.makedirs(".github/data", exist_ok=True)
    with open(".github/data/knowledge_graph.json", "w") as f:
        json.dump(graph, f, indent=2)

    print("Dynamic knowledge graph built.")

if __name__ == "__main__":
    build_knowledge_graph()
