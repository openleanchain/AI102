# Lab09-audio-chat: Develop an Audio-Enabled Chat App

## Learning Objective
By the end of this lab, you will:
- Learn how to build an **audio-enabled chat application** using Azure AI Foundry.
- Use the **multimodal** generative AI model to process audio and text.
- Summarize **voice messages** left by customers for a produce supplier company.
- Integrate the **Python OpenAI SDK** with Azure AI Foundry for multimodal interactions.

---

## What This Lab Is About
In this exercise, you will:

- Deploy the **Phi-4-multimodal-instruct** model in Azure AI Foundry.
- Configure a Python application to connect to your Azure AI Foundry project.
- Capture audio input (voice messages).

- Send text and audio input to the Phi-4-multimodal-instruct model hosted in Azure AI Foundry.
- Generate summaries and responses for customer messages.

---

## Files in This Lab  
### **audio_chat.py**  
- **Loads Azure credentials** for secure configuration.  
- **Uses**:  
  - `azure-ai-projects` to create an `AIProjectClient` and obtain an OpenAI-compatible client for interacting with the **Phi-4-multimodal-instruct** model.  
  - `openai` for sending chat completion requests.  
  - `requests` and `base64` for downloading and encoding audio files into Base64 format.  
- **Implements**:  
  - **Audio Input**: Downloads an MP3 file (e.g., `avocados.mp3` or `fresas.mp3`) and encodes it for API submission.  
  - **Multimodal Model Interaction**: Sends a chat request containing both text and audio input to the deployed model in Azure AI Foundry.  
  - **Summarization**: Processes the model’s response to generate a concise summary of the customer’s voice message, optionally assessing urgency.  

---

## Example Usage
### Sample prompt:
```
Can you summarize this customer's voice message?
```
Expected output:
- **Summary**: Parker from Fourth Coffee updates their order to include an additional 5 lbs of avocados.
- **Urgency**: No, it doesn't appear to be time-sensitive.
---

## Key Concepts
- **Azure AI Foundry**: A platform for deploying and managing AI models.
- **Phi-4-multimodal-instruct**: A multimodal generative AI model that supports text and audio input.
- **Azure AI Projects SDK**: Provides project and model management capabilities.
- **OpenAI Python SDK**: Enables chat completions with multimodal input.
- **Base64 Encoding**: Converts audio files into a format suitable for API requests.

---

## References
- https://microsoftlearning.github.io/mslearn-ai-language/Instructions/Labs/09-audio-chat.html
