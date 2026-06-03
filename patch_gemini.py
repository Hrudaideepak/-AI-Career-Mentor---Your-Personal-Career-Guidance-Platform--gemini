import re

files = ["backend/app/services/openai_service.py", "backend/app/services/chroma_service.py"]
for f_name in files:
    with open(f_name, "r") as f:
        content = f.read()

    # Revert to google.generativeai and ignore warning for now, as google.genai migration is complex
    content = content.replace("from google import genai", "import google.generativeai as genai")

    with open(f_name, "w") as f:
        f.write(content)
