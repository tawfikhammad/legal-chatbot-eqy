from sentence_transformers import SentenceTransformer, util
from database.db_utils import fetch_documents

from sentence_transformers import util

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def retrieve_by_title_similarity(question, top_k=1, threshold=0.85):
    docs = fetch_documents()
    
    if not docs:
        return None, None, None, None
    
    sub_titles = [doc['sub_title'] for doc in docs]
    
    sub_title_embeddings = model.encode(sub_titles, convert_to_tensor=True)
    question_embedding = model.encode(question, convert_to_tensor=True)

    hits = util.semantic_search(question_embedding, sub_title_embeddings, top_k=top_k)[0]
    
    # Filter based on threshold
    for hit in hits:
        if hit['score'] >= threshold:
            print(hit['score'])
            best_match = docs[hit['corpus_id']]  # Get the best match document
            return best_match
    
    return None


