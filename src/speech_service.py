import os
import azure.cognitiveservices.speech as speechsdk

class SpeechService:
    def __init__(self):
        self.speech_key = os.environ.get('SPEECH_KEY')
        self.speech_region = os.environ.get('SPEECH_REGION')
        
        if not self.speech_key or not self.speech_region:
            raise ValueError("Please set SPEECH_KEY and SPEECH_REGION environment variables.")

        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.speech_region)
        self.speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural' # Example voice

    def listen_and_transcribe(self):
        """
        Listens to the microphone and transcribes the speech to text.
        Returns the recognized text or None if no speech was recognized.
        """
        # Usage of the default microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        print("Listening...")
        result = speech_recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized: {result.text}")
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return None

    def speak(self, text):
        """
        Synthesizes text to speech and plays it through the default speaker.
        """
        audio_config = speechsdk.audio.AudioConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)

        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized to speaker for text [{text}]")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
