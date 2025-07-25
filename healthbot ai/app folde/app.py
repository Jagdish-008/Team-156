import os
import logging
import json
from flask import Flask, render_template, request, jsonify, session
from bot import TelegramBot
from diagnosis import DiagnosisEngine
from translations import TranslationManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "swasthya_bot_secret_key")

# Initialize components
telegram_bot = TelegramBot()
diagnosis_engine = DiagnosisEngine()
translation_manager = TranslationManager()

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from web interface"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        language = session.get('language', 'en')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
            
        # Initialize conversation state if not exists
        if 'conversation_state' not in session:
            session['conversation_state'] = {
                'step': 'greeting',
                'symptoms': [],
                'age': None,
                'severity': None,
                'duration': None,
                'location': None
            }
        
        response = process_message(message, session['conversation_state'], language)
        session.modified = True
        
        return jsonify(response)
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/set_language', methods=['POST'])
def set_language():
    """Set user's preferred language"""
    try:
        data = request.get_json()
        language = data.get('language', 'en')
        
        if language not in ['en', 'hi']:
            return jsonify({'error': 'Invalid language'}), 400
            
        session['language'] = language
        return jsonify({'success': True, 'language': language})
        
    except Exception as e:
        logging.error(f"Error setting language: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    """Reset conversation state"""
    try:
        session.pop('conversation_state', None)
        language = session.get('language', 'en')
        
        greeting_msg = translation_manager.get_text('greeting', language)
        return jsonify({
            'message': greeting_msg,
            'type': 'bot'
        })
        
    except Exception as e:
        logging.error(f"Error resetting chat: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """Handle Telegram webhook updates"""
    try:
        update = request.get_json()
        telegram_bot.process_update(update)
        return '', 200
        
    except Exception as e:
        logging.error(f"Error processing Telegram webhook: {str(e)}")
        return '', 500

def process_message(message, state, language):
    """Process user message and return appropriate response"""
    try:
        message_lower = message.lower()
        
        # Handle language switching
        if any(word in message_lower for word in ['hindi', 'हिंदी', 'english', 'अंग्रेजी']):
            if 'hindi' in message_lower or 'हिंदी' in message_lower:
                language = 'hi'
            else:
                language = 'en'
            
            return {
                'message': translation_manager.get_text('language_switched', language),
                'type': 'bot',
                'language': language
            }
        
        # Emergency keywords
        emergency_keywords = ['emergency', 'urgent', 'help', 'dying', 'आपातकाल', 'मदद', 'तुरंत']
        if any(keyword in message_lower for keyword in emergency_keywords):
            return {
                'message': translation_manager.get_text('emergency_response', language),
                'type': 'bot',
                'emergency': True
            }
        
        # Process based on conversation step
        if state['step'] == 'greeting':
            state['step'] = 'age'
            return {
                'message': translation_manager.get_text('ask_age', language),
                'type': 'bot'
            }
            
        elif state['step'] == 'age':
            try:
                age = int(''.join(filter(str.isdigit, message)))
                if 1 <= age <= 120:
                    state['age'] = age
                    state['step'] = 'main_symptom'
                    return {
                        'message': translation_manager.get_text('ask_main_symptom', language),
                        'type': 'bot'
                    }
                else:
                    return {
                        'message': translation_manager.get_text('invalid_age', language),
                        'type': 'bot'
                    }
            except:
                return {
                    'message': translation_manager.get_text('invalid_age', language),
                    'type': 'bot'
                }
                
        elif state['step'] == 'main_symptom':
            state['symptoms'].append(message)
            state['step'] = 'severity'
            return {
                'message': translation_manager.get_text('ask_severity', language),
                'type': 'bot'
            }
            
        elif state['step'] == 'severity':
            severity_keywords = {
                'mild': ['mild', 'light', 'हल्का', 'कम'],
                'moderate': ['moderate', 'medium', 'मध्यम', 'साधारण'],
                'severe': ['severe', 'heavy', 'bad', 'गंभीर', 'तेज', 'बहुत']
            }
            
            for level, keywords in severity_keywords.items():
                if any(keyword in message_lower for keyword in keywords):
                    state['severity'] = level
                    break
            else:
                state['severity'] = 'moderate'  # default
            
            state['step'] = 'duration'
            return {
                'message': translation_manager.get_text('ask_duration', language),
                'type': 'bot'
            }
            
        elif state['step'] == 'duration':
            state['duration'] = message
            state['step'] = 'location'
            return {
                'message': translation_manager.get_text('ask_location', language),
                'type': 'bot'
            }
            
        elif state['step'] == 'location':
            state['location'] = message
            state['step'] = 'diagnosis'
            
            # Generate diagnosis and recommendations
            diagnosis_result = diagnosis_engine.analyze_symptoms(
                symptoms=state['symptoms'],
                age=state['age'],
                severity=state['severity'],
                duration=state['duration']
            )
            
            hospitals = diagnosis_engine.get_nearby_hospitals(state['location'])
            
            response_text = translation_manager.format_diagnosis_response(
                diagnosis_result, hospitals, language
            )
            
            # Reset state for new conversation
            state['step'] = 'greeting'
            state['symptoms'] = []
            
            return {
                'message': response_text,
                'type': 'bot',
                'diagnosis': diagnosis_result,
                'hospitals': hospitals
            }
            
        else:
            return {
                'message': translation_manager.get_text('default_response', language),
                'type': 'bot'
            }
            
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return {
            'message': translation_manager.get_text('error_response', language),
            'type': 'bot'
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)