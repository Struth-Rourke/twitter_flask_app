# twitter_app/services/basilica_service.py

import os
from basilica import Connection
from dotenv import load_dotenv
load_dotenv()

# API_KEY stored in .env
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY")

# Making an API connection and printing the type 
basilica_conn = Connection(BASILICA_API_KEY)
print(type(basilica_conn)) #> <class 'basilica.Connection'>


## Basilica Function
# def basilica_api_client():
#     connection = basilica.Connection(API_KEY)
#     print(type(connection)) #> <class 'basilica.Connection'>
#     return connection

# if __name__ == "__main__":

    # # Sentences
    # sentences = [
    #     "This is a sentence!",
    #     "This is a similar sentence!",
    #     "I don't think this sentence is very similar at all...",
    # ]

    # # Embeddings 
    # embeddings = list(conn.embed_sentences(sentences))
    # for embed in embeddings:
    #     print("-----")
    #     print(embed)


# if __name__ == "__main__":

#     print("---------")
#     connection = basilica_api_client()

#     print("---------")
#     sentence = "Hello again"
#     sent_embeddings = connection.embed_sentence(sentence)
#     print(list(sent_embeddings))

#     print("---------")
#     sentences = ["Hello world!", "How are you?"]
#     print(sentences)
#     # it is more efficient to make a single request for all sentences...
#     embeddings = connection.embed_sentences(sentences)
#     print("EMBEDDINGS...")
#     print(type(embeddings))
#     print(list(embeddings))