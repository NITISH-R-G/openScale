import os
import json

def build_knowledge_graph():
    graph = {
        "nodes": [],
        "edges": []
    }

    # Static top-level structure based on known repo layout
    if os.path.exists("android_app"):
        graph["nodes"].append({"id": "android_app", "label": "Android App", "type": "module"})
        graph["edges"].append({"source": "root", "target": "android_app", "relation": "contains"})

    if os.path.exists("arduino_mcu"):
        graph["nodes"].append({"id": "arduino_mcu", "label": "Arduino MCU", "type": "module"})
        graph["edges"].append({"source": "root", "target": "arduino_mcu", "relation": "contains"})

    if os.path.exists("docs"):
        graph["nodes"].append({"id": "docs", "label": "Documentation", "type": "docs"})
        graph["edges"].append({"source": "root", "target": "docs", "relation": "documents"})

    # Check for bluetooth dependency in android app
    bt_path = "android_app/app/src/main/java/com/health/openscale/core/bluetooth"
    if os.path.exists(bt_path):
        graph["nodes"].append({"id": "bluetooth_core", "label": "Bluetooth Core", "type": "component"})
        graph["edges"].append({"source": "android_app", "target": "bluetooth_core", "relation": "implements"})

    os.makedirs(".github/data", exist_ok=True)
    with open(".github/data/knowledge_graph.json", "w") as f:
        json.dump(graph, f, indent=2)

    print("Knowledge graph built.")

if __name__ == "__main__":
    build_knowledge_graph()
