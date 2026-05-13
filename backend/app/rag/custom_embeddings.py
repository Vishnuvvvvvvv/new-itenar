import os
import httpx

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class GenAIEmbeddings:

    def __init__(self):

        # Disable SSL verification
        http_client = httpx.Client(
            verify=False
        )

        self.client = OpenAI(

            api_key=os.getenv(
                "GENAI_API_KEY"
            ),

            base_url=
            "https://genailab.tcs.in",

            http_client=http_client
        )

        self.model = (
            "azure/genailab-maas-text-embedding-3-large"
        )

    def embed_documents(self, texts):

        embeddings = []

        for text in texts:

            response = (
                self.client.embeddings.create(

                    model=self.model,

                    input=text
                )
            )

            embeddings.append(
                response.data[0].embedding
            )

        return embeddings

    def embed_query(self, text):

        response = (
            self.client.embeddings.create(

                model=self.model,

                input=text
            )
        )

        return response.data[0].embedding