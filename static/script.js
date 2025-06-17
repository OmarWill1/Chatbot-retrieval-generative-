let messages = [];
let model = "Modèle 1";

const chatBox = document.getElementById('chat-box');
const chatModelName = document.getElementById('chat-model-name');
const userInput = document.getElementById('user-input');

// Affiche un message dans le chat
function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(sender === 'user' ? 'user-msg' : 'bot-msg');

    const iconDiv = document.createElement('div');
    iconDiv.classList.add('icon');
    iconDiv.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = text;

    if(sender === 'user') {
        msgDiv.appendChild(contentDiv);
        msgDiv.appendChild(iconDiv);
    } else {
        msgDiv.appendChild(iconDiv);
        msgDiv.appendChild(contentDiv);
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Affiche le message d'introduction "Comment puis-je vous aider ?"
function showWelcomeMessage() {
    addMessage("Comment puis-je vous aider ?", 'bot');
}

// Montre l'indicateur de saisie (trois points clignotants)
function showTypingIndicator() {
    const typing = document.createElement('div');
    typing.classList.add('message', 'bot-msg', 'typing-indicator');
    typing.id = 'typing-indicator';

    const dots = document.createElement('div');
    dots.innerHTML = `<span>.</span><span>.</span><span>.</span>`;

    typing.appendChild(dots);
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Supprime l'indicateur de saisie
function removeTypingIndicator() {
    const typing = document.getElementById('typing-indicator');
    if(typing) typing.remove();
}

// Envoie du message utilisateur et réponse simulée
async function sendMessage() {
    const text = userInput.value.trim();
    const selectedModel = model || "Modèle 1";

    if (text === '') return;

    addMessage(text, 'user');
    messages.push({ role: 'user', content: text });
    userInput.value = '';
    removeTypingIndicator();
    showTypingIndicator();

    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, model: selectedModel })
        });

        const data = await response.json();
        removeTypingIndicator();

        const reply = data.response;

        // Crée le conteneur pour le message du bot
        const messageContainer = document.createElement('div');
        messageContainer.className = 'message bot-msg';

        const icon = document.createElement('div');
        icon.className = 'icon';
        icon.textContent = '🤖';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = ''; // Commence vide

        messageContainer.appendChild(icon);
        messageContainer.appendChild(messageContent);
        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Tape lettre par lettre
        await typeText(messageContent, reply, 15); // Tu peux changer la vitesse ici

        messages.push({ role: 'bot', content: reply });

    } catch (error) {
        removeTypingIndicator();
        addMessage("Une erreur s'est produite lors de la communication avec le serveur.", 'bot');
        console.error("Erreur lors de l'envoi :", error);
    }
}



// Gérer envoi avec la touche Enter
function handleKey(event) {
    if(event.key === 'Enter') {
        sendMessage();
    }
}

// Vider la conversation
function refreshChat() {
    messages = [];
    chatBox.innerHTML = '';
    showWelcomeMessage();
}

// Changer le modèle de chat
function setModel(selectedModel) {
    model = selectedModel;
    chatModelName.textContent = selectedModel;
    //refreshChat();
}

window.onload = () => {
    showWelcomeMessage();
};

async function typeText(element, text, delay = 60) {
    for (let i = 0; i < text.length; i++) {
        element.textContent += text[i];
        await new Promise(resolve => setTimeout(resolve, delay));
    }
}
