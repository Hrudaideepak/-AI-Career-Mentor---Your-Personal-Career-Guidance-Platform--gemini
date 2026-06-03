import re

with open("backend/app/schemas.py", "r") as f:
    content = f.read()

content = content.replace("from pydantic import BaseModel", "from pydantic import BaseModel, ConfigDict")
content = re.sub(r"\s*class Config:\s*from_attributes = True", "\n    model_config = ConfigDict(from_attributes=True)", content)

with open("backend/app/schemas.py", "w") as f:
    f.write(content)
