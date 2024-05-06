import time
import chromadb

from functions import collect_data, add_to_db
from chromadb.utils import embedding_functions

key = <YOUR KEY>
urls = ["https://www.accel.com/",
        "https://matrix.vc/",
        "https://www.500.co/",
        "https://www.indexventures.com/",
        "https://www.sparkcapital.com/",
        "https://www.kleinerperkins.com/",
        "https://www.insightpartners.com/",
        "https://playground.vc/",
        "https://www.linsecapital.com/",
        "https://www.blockchaincapital.com/",
        "https://fifthwall.com/",
        "https://www.luxcapital.com/"]

data = []
for url in urls:
    collect_data(url, data)
    time.sleep(20)


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=key,
                model_name="text-embedding-3-small"
            )

# Create database
client = chromadb.PersistentClient(path="database")
collection = client.get_or_create_collection(
    name="DataBase", # name of the database
    embedding_function=openai_ef, # embedding function for creating vectors
    metadata={"hnsw:space": "cosine"} # similarity function is set cosine similarity
)

# Add items to database
for item in data:
    add_to_db(item, collection)
