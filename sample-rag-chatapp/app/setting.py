import os
from enum import Enum

from dotenv import load_dotenv


load_dotenv()

OPENAI_API_MODEL = os.environ["OPENAI_API_MODEL"]
OPENAI_API_TEMPERATURE = float(os.environ["OPENAI_API_TEMPERATURE"])


class Mode(Enum):
    AGENT = "agent"
    RAG = "rag"
    AUTO = "auto"


MODE = Mode.AUTO
