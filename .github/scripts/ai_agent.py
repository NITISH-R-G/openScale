import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

def generate_ai_documentation():
    # If there's an API key, we could use OpenAI or similar.
    # But since this is a self-maintaining script that needs to work robustly,
    # we will generate deterministic AI-like summaries and structure if no API key is present.
    # In a real environment with the key, we'd hit the API here.

    analysis_file = ".github/data/repo_analysis.json"
    if not os.path.exists(analysis_file):
        return

    with open(analysis_file, "r") as f:
        analysis = json.load(f)

    # Mock AI generation based on detected frameworks
    summary = f"This repository contains a multi-component project primarily using {', '.join(analysis['languages'])}. "
    if "Android" in analysis["frameworks"]:
        summary += "It features an Android application component. "
    if "C/C++ (Arduino)" in analysis["languages"]:
        summary += "It includes Arduino firmware and microcontroller code. "

    ai_doc = {
        "generated_at": datetime.now().isoformat(),
        "repository_summary": summary,
        "architectural_insights": "The system is decoupled into client applications and hardware integrations.",
        "onboarding_guide": "To get started, check the Android and Arduino directories. Build the Android app using Gradle and flash the Arduino using standard C++ toolchains."
    }

    # Attempt to use OpenAI if key is present
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("OPENAI_API_KEY detected, calling LLM API...")
        try:
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": "gpt-3.5-turbo",
                    "messages": [{
                        "role": "user",
                        "content": f"Based on this repo analysis: {json.dumps(analysis)}, write a short repository summary and an architectural insight paragraph."
                    }]
                }).encode("utf-8")
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                llm_text = result["choices"][0]["message"]["content"]

                # Update heuristic fallback with real response
                ai_doc["repository_summary"] = "AI Summary: " + llm_text[:200] + "..." # Simplified parsing for example
                ai_doc["architectural_insights"] = "For full details, see the generated insights."
                print("Successfully retrieved AI summary.")
        except Exception as e:
            print(f"Error calling OpenAI API: {e}. Falling back to heuristics.")
    else:
        print("No OPENAI_API_KEY found, using heuristic generation.")

    os.makedirs(".github/data", exist_ok=True)
    with open(".github/data/ai_documentation.json", "w") as f:
        json.dump(ai_doc, f, indent=2)

if __name__ == "__main__":
    generate_ai_documentation()
