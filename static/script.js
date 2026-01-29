// ==================== CONFIGURATION ====================
const API_BASE_URL = 'http://localhost:8000';

// ==================== DOM ELEMENTS ====================
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');
const welcomeMessage = document.getElementById('welcome-message');

// ==================== STATE ====================
let isProcessing = false;

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
    // Focus on input
    userInput.focus();

    // Add event listeners
    userInput.addEventListener('keypress', handleKeyPress);
    sendBtn.addEventListener('click', sendMessage);

    console.log('🚀 Crypto Agent Frontend Initialized');
});

// ==================== UTILITY FUNCTIONS ====================
function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function scrollToBottom() {
    chatMessages.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function hideWelcomeMessage() {
    if (welcomeMessage) {
        welcomeMessage.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        welcomeMessage.style.opacity = '0';
        welcomeMessage.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            welcomeMessage.remove();
        }, 300);
    }
}

// ==================== MESSAGE RENDERING ====================
function addMessage(text, isUser = false) {
    hideWelcomeMessage();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = text;

    const time = document.createElement('span');
    time.className = 'message-time';
    time.textContent = getCurrentTime();

    bubble.appendChild(messageText);
    bubble.appendChild(time);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    chatMessages.appendChild(messageDiv);
    scrollToBottom();

    return messageDiv;
}

function showErrorMessage(errorText) {
    hideTypingIndicator();

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <strong>⚠️ Error</strong><br>
        ${errorText}
    `;

    chatMessages.appendChild(errorDiv);
    scrollToBottom();

    setTimeout(() => {
        errorDiv.style.transition = 'opacity 0.3s ease';
        errorDiv.style.opacity = '0';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// ==================== API COMMUNICATION ====================
async function sendMessageToAPI(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Server error occurred');
        }

        const data = await response.json();
        return data.response;

    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==================== MESSAGE SENDING ====================
async function sendMessage() {
    if (isProcessing) return;

    const message = userInput.value.trim();
    if (!message) return;

    // Disable input and button
    isProcessing = true;
    sendBtn.disabled = true;
    userInput.disabled = true;

    // Add user message
    addMessage(message, true);

    // Clear input
    userInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send to API
        const response = await sendMessageToAPI(message);

        // Hide typing indicator
        hideTypingIndicator();

        // Add AI response
        addMessage(response, false);

    } catch (error) {
        hideTypingIndicator();
        showErrorMessage(
            error.message || 'Failed to get response from the server. Please try again.'
        );
    } finally {
        // Re-enable input and button
        isProcessing = false;
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ==================== EXAMPLE QUERIES ====================
function sendExample(exampleText) {
    userInput.value = exampleText;
    userInput.focus();
    sendMessage();
}

// ==================== HEALTH CHECK ====================
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('✅ API Health:', data);
    } catch (error) {
        console.error('❌ API Health Check Failed:', error);
        showErrorMessage('Backend server is not running. Please start the server.');
    }
}

// Check API health on load
checkAPIHealth();
