import os
import sys
import time
from dotenv import load_dotenv

# Ensure the src directory is in the path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from speech_service import SpeechService
from chat_service import ChatService

def main():
    # Load environment variables from .env file
    load_dotenv()

    print("Initializing Office Object Chatbot...")
    
    try:
        speech_service = SpeechService()
        chat_service = ChatService()
    except Exception as e:
        print(f"Failed to initialize services: {e}")
        return

    print("Ready to chat! Press Ctrl+C to stop.")
    
    # Simple continuous loop
    while True:
        try:
            # 1. Listen and Transcribe
            user_text = speech_service.listen_and_transcribe()
            
            if user_text:
                # 2. Get Response from LLM
                response_text = chat_service.get_response(user_text)
                
                # 3. Speak Response
                if response_text:
                    print(f"Assistant: {response_text}")
                    speech_service.speak(response_text)
            
            # Small delay to prevent tight loop if audio config is weird
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"An error occurred in the loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
