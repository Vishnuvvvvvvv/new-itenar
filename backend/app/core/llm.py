import os
import httpx

from dotenv import load_dotenv

try:
    from langchain_openai import ChatOpenAI
except Exception:
    ChatOpenAI = None


load_dotenv()

# Disable SSL verification for enterprise environment
client = httpx.Client(
    verify=False
)

class UnavailableLLM:
    def invoke(self, prompt):
        raise RuntimeError(
            "LLM client is unavailable. Install langchain-openai and configure GENAI_API_KEY."
        )


if ChatOpenAI:
    llm = ChatOpenAI(

        base_url="https://genailab.tcs.in",

        model=(
            "azure_ai/genailab-maas-DeepSeek-V3-0324"
        ),

        api_key=os.getenv(
            "GENAI_API_KEY"
        ),

        temperature=0,

        http_client=client
    )
else:
    llm = UnavailableLLM()
