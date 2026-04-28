# Talk to Me

Turn a Raspberry Pi (or any computer with a mic and speaker) into a conversational object. Speak to it, and it speaks back — powered by Azure Speech and Azure OpenAI.

Drop it inside a 3D-printed lamp, a stuffed animal, a stapler, anything. Change the `SYSTEM_PROMPT` and the object takes on a personality.

## How it works

```
   ┌────────┐   speech    ┌──────────────────┐   text    ┌──────────────┐
   │  You   │ ──────────▶ │  Azure Speech    │ ────────▶ │ Azure OpenAI │
   │ 🎤 mic │             │   (recognize)    │           │   (chat)     │
   └────────┘             └──────────────────┘           └──────┬───────┘
                                                                │
                                                                │ reply
                                                                ▼
   ┌────────┐   audio     ┌──────────────────┐   text    ┌──────────────┐
   │  You   │ ◀────────── │  Azure Speech    │ ◀──────── │   History    │
   │ 🔊 spk │             │   (synthesize)   │           │  (in-memory) │
   └────────┘             └──────────────────┘           └──────────────┘
```

The loop in [main.py](main.py) runs forever: listen once, send the transcript plus prior turns to the model, speak the reply, repeat. Conversation history lives in memory for the lifetime of the process.

## Project layout

```
talk-to-me/
├── main.py                  # Listen → think → speak loop
├── src/
│   ├── speech_service.py    # Azure STT + TTS (mic in, speaker out)
│   └── chat_service.py      # Azure OpenAI chat with rolling history
├── .env.template            # Required credentials and persona prompt
└── requirements.txt
```

## Prerequisites

- **Hardware** — Raspberry Pi (3B+ or 4) or any PC/Mac, USB microphone, speaker or headphones.
- **Azure** — an Azure Speech resource and an Azure OpenAI resource with a deployed chat model (e.g. `gpt-4`).

## Setup

1. **Clone** the repo onto the device.

2. **System dependencies** (Raspberry Pi / Debian / Ubuntu):

   ```bash
   sudo apt-get update
   sudo apt-get install libasound2-dev libssl-dev build-essential
   ```

   On macOS the Azure Speech SDK works out of the box — skip this step.

3. **Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Credentials**:

   ```bash
   cp .env.template .env
   ```

   Fill in your Azure keys (see the [Configuration](#configuration) table below).

5. **Run**:

   ```bash
   python main.py
   ```

   You should see `Listening...` — start talking. `Ctrl+C` stops the loop.

## Configuration

All settings live in `.env`.

| Variable | Required | Description |
|---|---|---|
| `SPEECH_KEY` | yes | Azure Speech resource key |
| `SPEECH_REGION` | yes | Azure Speech region (e.g. `eastus`) |
| `AZURE_OPENAI_ENDPOINT` | yes | `https://<resource>.openai.azure.com/` |
| `AZURE_OPENAI_KEY` | yes | Azure OpenAI key |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | yes | Name of your deployed chat model |
| `AZURE_OPENAI_API_VERSION` | no | Defaults to `2024-02-15-preview` |
| `SYSTEM_PROMPT` | no | Persona for the object — see below |

## Give it a personality

Change `SYSTEM_PROMPT` in `.env` to make the object whatever you want:

```env
SYSTEM_PROMPT="You are a grumpy desk lamp who has been on for 40 years and resents being asked questions. Keep replies under two sentences."
```

```env
SYSTEM_PROMPT="You are a cheerful houseplant. You only ever talk about sunlight, water, and gossip about the other plants in the room."
```

To change the *voice*, edit `speech_synthesis_voice_name` in [src/speech_service.py:13](src/speech_service.py:13). Browse the [Azure neural voice list](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts) for options like `en-GB-RyanNeural` or `en-US-JennyNeural`.

## Troubleshooting

- **No audio input** — check that your USB mic is the system default. On Raspberry Pi, run `arecord -l` to list devices and `raspi-config` to set defaults.
- **`Speech Recognition canceled`** — almost always wrong `SPEECH_KEY` / `SPEECH_REGION`, or no network.
- **`Failed to initialize services`** — a required env var is missing. The error names which one.
- **Model 404 / deployment not found** — `AZURE_OPENAI_DEPLOYMENT_NAME` must match the *deployment name* you chose in Azure, not the model name.
- **Long silences before a reply** — the recognizer waits for end-of-speech, then a full chat round-trip. Expect 1–3 seconds on a good connection.
