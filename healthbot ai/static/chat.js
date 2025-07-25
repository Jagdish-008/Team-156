// SwasthyaBot Chat Interface JavaScript

let currentLanguage = 'en';
let isProcessing = false;

// Text translations for UI elements
const uiTranslations = {
    en: {
        'welcome-title': 'Welcome to SwasthyaBot',
        'welcome-subtitle': 'Your bilingual healthcare assistant for rural India. Get symptom guidance, health advice, and find nearby medical facilities.',
        'disclaimer-text': '<strong>Important:</strong> This is for informational purposes only and not a substitute for professional medical advice. For emergencies, call <strong>108</strong> immediately.',
        'chat-header': 'Health Consultation',
        'send-text': 'Send',
        'reset-text': 'New Chat',
        'loading-text': 'Processing...',
        'emergency-text': '<strong>Emergency:</strong> Call 108 for immediate medical assistance',
        'current-language': 'English',
        'message-placeholder': 'Type your message here...'
    },
    hi: {
        'welcome-title': 'स्वास्थ्यबॉट में आपका स्वागत है',
        'welcome-subtitle': 'ग्रामीण भारत के लिए आपका द्विभाषी स्वास्थ्य सहायक। लक्षण मार्गदर्शन, स्वास्थ्य सलाह प्राप्त करें और नजदीकी चिकित्सा सुविधाएं खोजें।',
        'disclaimer-text': '<strong>महत्वपूर्ण:</strong> यह केवल सूचनात्मक उद्देश्यों के लिए है और पेशेवर चिकित्सा सलाह का विकल्प नहीं है। आपातकाल के लिए तुरंत <strong>108</strong> पर कॉल करें।',
        'chat-header': 'स्वास्थ्य परामर्श',
        'send-text': 'भेजें',
        'reset-text': 'नई चैट',
        'loading-text': 'प्रसंस्करण...',
        'emergency-text': '<strong>आपातकाल:</strong> तत्काल चिकित्सा सहायता के लिए 108 पर कॉल करें',
        'current-language': 'हिंदी',
        'message-placeholder': 'यहाँ अपना संदेश टाइप करें...'
    }
};

// Initialize chat
function startChat() {
    addBotMessage(
        currentLanguage === 'en' 
            ? "Hello! I'm SwasthyaBot, your healthcare assistant. I can help you understand your symptoms and find nearby medical facilities.\n\n⚠️ Important: I'm not a replacement for professional medical advice. In case of emergency, please call 108 immediately.\n\nTo get started, could you please tell me your age?"
            : "नमस्ते! मैं स्वास्थ्यबॉट हूं, आपका स्वास्थ्य सहायक। मैं आपके लक्षणों को समझने और नजदीकी चिकित्सा सुविधाएं खोजने में मदद कर सकता हूं।\n\n⚠️ महत्वपूर्ण: मैं पेशेवर चिकित्सा सलाह का विकल्प नहीं हूं। आपातकाल की स्थिति में कृपया तुरंत 108 पर कॉल करें।\n\nशुरू करने के लिए, कृपया मुझे अपनी उम्र बताएं?"
    );
}

// Send message function
function sendMessage() {
    if (isProcessing) return;
    
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    messageInput.value = '';
    
    // Show loading indicator
    showLoading(true);
    isProcessing = true;
    
    // Send message to server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        isProcessing = false;
        
        if (data.error) {
            addBotMessage(`Error: ${data.error}`, 'error');
        } else {
            // Handle language switch
            if (data.language) {
                currentLanguage = data.language;
                updateUILanguage();
            }
            
            // Add bot response
            addBotMessage(data.message, data.emergency ? 'emergency' : 'normal');
            
            // Handle diagnosis results
            if (data.diagnosis) {
                displayDiagnosisResults(data.diagnosis, data.hospitals);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showLoading(false);
        isProcessing = false;
        addBotMessage(
            currentLanguage === 'en' 
                ? 'Sorry, I encountered an error. Please try again.'
                : 'क्षमा करें, मुझे एक त्रुटि का सामना करना पड़ा। कृपया पुनः प्रयास करें।',
            'error'
        );
    });
}

// Add user message to chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message user';
    
    messageDiv.innerHTML = `
        <div class="message-bubble user">
            ${escapeHtml(message)}
        </div>
        <div class="message-time text-end">
            ${getCurrentTime()}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message, type = 'normal') {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message bot';
    
    let bubbleClass = 'message-bubble bot';
    if (type === 'emergency') {
        bubbleClass += ' emergency';
    }
    
    messageDiv.innerHTML = `
        <div class="${bubbleClass}">
            ${formatMessage(message)}
        </div>
        <div class="message-time">
            <i data-feather="bot" class="me-1" style="width: 12px; height: 12px;"></i>
            SwasthyaBot • ${getCurrentTime()}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    
    // Re-initialize feather icons for new elements
    feather.replace();
    
    scrollToBottom();
}

// Format message with basic HTML support
function formatMessage(message) {
    return message
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/(📞|🚨|⚠️|🩺|🏥|📋|👨‍⚕️|💬|📍)/g, '<span class="me-1">$1</span>');
}

// Display diagnosis results
function displayDiagnosisResults(diagnosis, hospitals) {
    if (diagnosis.conditions && diagnosis.conditions.length > 0) {
        const chatMessages = document.getElementById('chat-messages');
        
        // Add a structured diagnosis card
        const diagnosisCard = document.createElement('div');
        diagnosisCard.className = 'chat-message bot mt-3';
        
        let cardContent = `
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h6 class="mb-0">
                        <i data-feather="clipboard" class="me-2"></i>
                        ${currentLanguage === 'en' ? 'Diagnosis Summary' : 'निदान सारांश'}
                    </h6>
                </div>
                <div class="card-body">
        `;
        
        // Add conditions
        diagnosis.conditions.forEach((condition, index) => {
            const name = condition[`name_${currentLanguage}`] || condition.name_en;
            const advice = condition[`advice_${currentLanguage}`] || condition.advice_en;
            
            cardContent += `
                <div class="mb-3 ${index > 0 ? 'border-top pt-3' : ''}">
                    <h6 class="text-primary">${index + 1}. ${name}</h6>
                    <p class="small mb-0">${advice}</p>
                </div>
            `;
        });
        
        cardContent += '</div></div>';
        diagnosisCard.innerHTML = cardContent;
        
        chatMessages.appendChild(diagnosisCard);
        feather.replace();
        scrollToBottom();
    }
}

// Handle key press in message input
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Show/hide loading indicator
function showLoading(show) {
    const loadingIndicator = document.getElementById('loading-indicator');
    const messageInput = document.getElementById('message-input');
    
    if (show) {
        loadingIndicator.style.display = 'block';
        messageInput.disabled = true;
    } else {
        loadingIndicator.style.display = 'none';
        messageInput.disabled = false;
        messageInput.focus();
    }
}

// Change language
function changeLanguage(language) {
    fetch('/set_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: language })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentLanguage = language;
            updateUILanguage();
            addBotMessage(
                language === 'en' 
                    ? 'Language switched to English. How can I help you with your health concerns today?'
                    : 'भाषा हिंदी में बदल दी गई। आज मैं आपकी स्वास्थ्य संबंधी चिंताओं में कैसे सहायता कर सकता हूं?'
            );
        }
    })
    .catch(error => {
        console.error('Error changing language:', error);
    });
}

// Update UI language
function updateUILanguage() {
    const translations = uiTranslations[currentLanguage];
    
    Object.keys(translations).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            if (key === 'disclaimer-text' || key === 'emergency-text') {
                element.innerHTML = translations[key];
            } else {
                element.textContent = translations[key];
            }
        }
    });
    
    // Update placeholder
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.placeholder = translations['message-placeholder'];
    }
}

// Reset chat
function resetChat() {
    fetch('/reset_chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Clear chat messages
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';
        
        // Add welcome message
        addBotMessage(data.message);
    })
    .catch(error => {
        console.error('Error resetting chat:', error);
        // Fallback: reload page
        location.reload();
    });
}

// Utility functions
function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Auto-focus on message input when page loads
document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.focus();
    }
});

window.addEventListener('online', function() {
    addBotMessage(
        currentLanguage === 'en' 
            ? '✅ Connection restored. You can continue chatting.'
            : '✅ कनेक्शन बहाल हो गया। आप चैट जारी रख सकते हैं।',
        'normal'
    );
});

window.addEventListener('offline', function() {
    addBotMessage(
        currentLanguage === 'en' 
            ? '⚠️ No internet connection. Please check your network and try again.'
            : '⚠️ इंटरनेट कनेक्शन नहीं है। कृपया अपना नेटवर्क जांचें और पुनः प्रयास करें।',
        'error'
    );
});
