# Office Object Chatbot Framework

This project allows you to turn a Raspberry Pi (or any computer) into a conversational "Office Object" using Azure Cognitive Services and Azure OpenAI.

## Prerequisites

- **Hardware**:
  - Raspberry Pi (3B+ or 4 recommended) or a PC/Mac.
  - USB Microphone.
  - Speaker/Headphones.
- **Azure Subscription**:
  - Azure Speech Service resource.
  - Azure OpenAI Service resource.

## Setup Instructions

1. **Clone the repository** (or copy these files to your Raspberry Pi).

2. **Install system dependencies** (Raspberry Pi / Linux):

   ```bash
   sudo apt-get update
   sudo apt-get install libasound2-dev libssl-dev build-essential
   ```

3. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   - Copy the template file:

     ```bash
     cp .env.template .env
     ```

   - Open `.env` and fill in your Azure keys and endpoints.
   - (Optional) Update `SYSTEM_PROMPT` to change the personality of your object.

5. **Run**:

   ```bash
   python main.py
   ```

## Troubleshooting

- **No Audio Input**: Ensure your microphone is set as the default recording device in your OS settings or `raspi-config`.
- **Azure Errors**: Double-check your keys, regions, and endpoint URLs in the `.env` file.
