#!/usr/bin/env python3

# Load model directly
import scipy
from ctransformers import AutoModelForCausalLM

from db_scripts.upload_data import model as embedding_model

llm = AutoModelForCausalLM.from_pretrained(
    "models/Wizard-Vicuna-7B-Uncensored.Q4_K_M.gguf", model_type="llama", gpu_layers=50
)


def get_response(query: str, context: str):
    # split the context into chunks of tokens to fit in the model context window
    tokenized_context = llm.tokenize(context)
    token_step = 128
    # since we can't fit this into the model's context window (which is quite small)
    # I chose to duplicate some work here and re-use the same embedding_model to identify
    # which chunk of the context is most similar to the query
    # this is a naive approach and can be improved
    # by chunking before uploading to the pgvector store.
    # For now, storing all the context in the pgvector store and then
    # chunking it here allows more rapid iteration on model selection
    context_chunks = [
        llm.detokenize(tokenized_context[i : i + token_step])
        for i in range(0, len(tokenized_context), token_step)
    ]
    context_embeds = list(map(embedding_model.encode, context_chunks))
    query_embed = embedding_model.encode(query)

    # using scipy to calculate the cosine similarity between the query and each chunk of the context
    distances = [
        scipy.spatial.distance.cosine(query_embed, context_embed)
        for context_embed in context_embeds
    ]
    most_similar_chunk = context_chunks[distances.index(min(distances))]
    llm.reset()
    naive_response = llm(query + "\n")
    response = llm(
        f"Add any relevant details from this snippet {most_similar_chunk} to {naive_response} and return it in a well-formatted paragraph without any citation marks or extra information.\nQuestion:{query}\nReponse:\n"
    )

    return response
