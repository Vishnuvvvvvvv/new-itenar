import os
import httpx

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


load_dotenv()

# Disable SSL verification for enterprise environment
client = httpx.Client(
    verify=False
)

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