import os
from openai import AzureOpenAI

class ChatService:
    def __init__(self):
        self.api_key = os.environ.get('AZURE_OPENAI_KEY')
        self.api_base = os.environ.get('AZURE_OPENAI_ENDPOINT')
        self.deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
        self.api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        self.system_prompt = os.environ.get('SYSTEM_PROMPT', 'You are a helpful AI assistant.')

        if not all([self.api_key, self.api_base, self.deployment_name]):
             raise ValueError("Please set AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables.")

        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base
        )
        
        self.history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def get_response(self, user_text):
        """
        Sends user text to Azure OpenAI and returns the assistant's response.
        """
        self.history.append({"role": "user", "content": user_text})

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=self.history,
                max_tokens=800,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )

            assistant_response = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": assistant_response})
            return assistant_response

        except Exception as e:
            print(f"Error getting response from OpenAI: {e}")
            return "I'm sorry, I'm having trouble connecting to my brain right now."
