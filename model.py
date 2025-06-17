from transformers import AutoTokenizer
import pandas as pd


tokenizer = AutoTokenizer.from_pretrained("gpt2")


import pandas as pd

data = {
    "Question": [
        "What is Artificial Intelligence?",
        "How does a neural network work?",
        "What is supervised learning?",
        "What is overfitting?",
        "What is Python?" , 
        "hey"
    ],
    "Answer": [
        "Artificial Intelligence is the simulation of human intelligence in machines.",
        "Neural networks mimic the human brain by using layers of nodes to process data.",
        "It’s a machine learning task where models learn from labeled data.",
        "When a model learns training data too well, including noise, and performs poorly on new data.",
        "Python is a popular high-level programming language used for many applications." , 
        "hey there , how I can I assist you "
    ]
}

df = pd.DataFrame(data)
df


from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

question_embedded  = model.encode(df['Question'])
answer_embedded = model.encode(df["Answer"])

# Create a new list by zipping the original questions, answers, and their embeddings
data = [(q_text, a_text, q_emb, a_emb) for q_text, a_text, q_emb, a_emb in zip(df['Question'], df['Answer'], question_embedded, answer_embedded)]

def encoding (text):

  text_encodign = model.encode(text)
  return text_encodign

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 


def find_similaire_answer(query , data):

  query_emb = model.encode(query).reshape(1 , -1 )
  embeddings_answers = np.vstack(list(  item[3] for item in data))

  
  similarities = cosine_similarity(query_emb , embeddings_answers)[0] 

  best_indx = similarities.argmax().tolist()
  answer  = df["Answer"].iloc[best_indx]


  return answer
answer = find_similaire_answer("How does a neural network work?	", data=data)



print(f"Bot : {answer}")



