# Lab01-analyze-text: Analyze Text with Azure AI Language


## Learning Objective
By the end of this lab, you will:
- Learn how to use **Azure AI Language** to analyze text for insights.
- Perform operations such as:
  - **Language Detection**
  - **Sentiment Analysis**
  - **Key Phrase Extraction**
  - **Entity Recognition** (identify people, organizations, locations, etc.)
- Understand how to call Azure AI Language services using Python.

---

## What This Lab Is About
This lab demonstrates how to:
- Connect to the **Azure AI Language** service.
- Submit text for analysis using the **Text Analytics API**.
- Interpret results for language detection, sentiment, key phrases, and named entities.

---

## Files in This Lab
### **analyze_text.py**
- Loads Azure credentials from `.env`.
- Uses the `azure-ai-textanalytics` SDK.
- Implements:
  - **Language Detection**: Identify the language of input text.
  - **Sentiment Analysis**: Determine if text is positive, negative, or neutral.
  - **Key Phrase Extraction**: Extract important phrases from text.
  - **Entity Recognition**: Detect entities like names, organizations, and locations.

---

## Example Usage
### Sample text:

```
Microsoft was founded by Bill Gates and Paul Allen in the United States.
```
Expected output:
- **Language**: English
- **Sentiment**: Neutral
- **Key Phrases**: ["Microsoft", "Bill Gates", "Paul Allen"]
- **Entities**:
  - Organization: Microsoft
  - Person: Bill Gates
  - Person: Paul Allen
  - Location: United States

---
## Key Concepts
- **Azure AI Language**: A cloud-based service for natural language processing.
- **Text Analytics API**: Provides prebuilt models for:
  - Language Detection
  - Sentiment Analysis
  - Key Phrase Extraction
  - Entity Recognition

---

## References
- https://microsoftlearning.github.io/mslearn-ai-language/Instructions/Labs/01-analyze-text.html
- https://learn.microsoft.com/azure/ai-services/language-service/overview
  