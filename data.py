import pandas as pd


data = pd.read_csv("common_knowledge_chatbot (1).csv")['answer'].tolist()

print(data)
