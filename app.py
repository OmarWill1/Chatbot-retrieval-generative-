from flask import Flask, render_template, request, jsonify
from model import find_similaire_answer, data
from dialogpt_finetuning import generative_answer
from blenderbot import personalize_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    model = request.json.get('model')
    print(model)
    if model == 'Modèle 1':
        answer = find_similaire_answer(user_message, data=data)
        
    else :
        #dialogpt 
        #answer = generative_answer(user_message)
        answer = personalize_response(user_message)
        
        
    # Pour le moment, utilise find_similaire_answer
    '''answer = find_similaire_answer(user_message, data=data)
    answer = generative_answer(user_message)'''
    # Exemple : tu peux adapter la logique ici selon le modèle choisi
    response = f"{answer}"  # ou ajouter le modèle si besoin

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)


