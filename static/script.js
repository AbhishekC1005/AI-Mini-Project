const API_URL = '/ask-reception';
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Handle Enter key press
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Send message function
async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    userInput.value = '';

    // Disable send button
    sendBtn.disabled = true;

    // Show loading indicator
    const loadingId = addMessage('Thinking', 'bot', true);

    try {
        // Call API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_query: message
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('API Response:', data);

        // Remove loading indicator
        removeMessage(loadingId);

        // Add bot response
        if (data && data.response) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('No response received from server.', 'bot');
        }

    } catch (error) {
        // Remove loading indicator
        removeMessage(loadingId);

        // Show error message with details
        console.error('Full Error:', error);
        addMessage(`Sorry, I encountered an error: ${error.message}. Please check the console for details.`, 'bot');
    } finally {
        // Re-enable send button
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender, isLoading = false) {
    const messageDiv = document.createElement('div');
    const messageId = 'msg-' + Date.now();
    messageDiv.id = messageId;
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (isLoading) {
        contentDiv.innerHTML = `<span class="loading">${text}</span>`;
    } else {
        // Format the text (preserve line breaks and lists)
        contentDiv.innerHTML = formatMessage(text);
    }

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageId;
}

// Remove message from chat
function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

// Format message text
function formatMessage(text) {
    // Remove markdown bold (**text** or __text__)
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/__(.*?)__/g, '<strong>$1</strong>');
    
    // Remove markdown headers (### text)
    formatted = formatted.replace(/^###\s+(.+)$/gm, '<strong>$1</strong>');
    formatted = formatted.replace(/^##\s+(.+)$/gm, '<strong>$1</strong>');
    formatted = formatted.replace(/^#\s+(.+)$/gm, '<strong>$1</strong>');
    
    // Convert markdown lists (- item or * item)
    formatted = formatted.replace(/^[\-\*]\s+(.+)$/gm, '• $1');
    
    // Convert numbered lists (1. item)
    formatted = formatted.replace(/^\d+\.\s+(.+)$/gm, '• $1');
    
    // Convert line breaks to <br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Convert bullet points
    formatted = formatted.replace(/•/g, '&bull;');
    
    return formatted;
}

// Quick question function
function askQuestion(question) {
    userInput.value = question;
    sendMessage();
}

// Focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});
