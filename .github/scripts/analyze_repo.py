import os
import json
from pathlib import Path

def analyze_repo(root_dir="."):
    analysis = {
        "directories": [],
        "languages": set(),
        "frameworks": set(),
        "build_tools": set(),
        "key_files": []
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore hidden dirs like .git and .github
        if any(part.startswith('.') for part in Path(dirpath).parts):
            continue

        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path != ".":
            analysis["directories"].append(rel_path)

        for file in filenames:
            ext = os.path.splitext(file)[1].lower()

            # Simple language detection
            if ext in ['.py']: analysis["languages"].add("Python")
            if ext in ['.java']: analysis["languages"].add("Java")
            if ext in ['.kt', '.kts']: analysis["languages"].add("Kotlin")
            if ext in ['.js', '.ts']: analysis["languages"].add("JavaScript/TypeScript")
            if ext in ['.ino', '.cpp', '.c', '.h']: analysis["languages"].add("C/C++ (Arduino)")
            if ext in ['.rb']: analysis["languages"].add("Ruby")
            if ext in ['.yml', '.yaml']: analysis["languages"].add("YAML")
            if ext in ['.xml']: analysis["languages"].add("XML")
            if ext in ['.md']: analysis["languages"].add("Markdown")

            # Framework/tool detection
            if file == "build.gradle" or file == "build.gradle.kts":
                analysis["build_tools"].add("Gradle")
                analysis["frameworks"].add("Android")
            if file == "pom.xml": analysis["build_tools"].add("Maven")
            if file == "package.json": analysis["build_tools"].add("npm/yarn")
            if file == "requirements.txt": analysis["build_tools"].add("pip")
            if file == "Gemfile": analysis["build_tools"].add("Bundler")
            if file == "Fastfile": analysis["build_tools"].add("Fastlane")

            # Key files
            if file in ["README.md", "LICENSE", "CONTRIBUTING.md", "Dockerfile", "docker-compose.yml"]:
                analysis["key_files"].append(os.path.join(rel_path, file))

    analysis["languages"] = list(analysis["languages"])
    analysis["frameworks"] = list(analysis["frameworks"])
    analysis["build_tools"] = list(analysis["build_tools"])

    return analysis

if __name__ == "__main__":
    print("Running repository analysis...")
    data = analyze_repo()

    os.makedirs(".github/data", exist_ok=True)
    with open(".github/data/repo_analysis.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Analysis saved to .github/data/repo_analysis.json")
