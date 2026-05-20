# Google AI Reference Ecosystem (`llls.md`)

This file catalogs active Google models, specialized tools, and agent structures. Rate limits are displayed in the standard format: **`Current Usage / Allotted Limit`**.

---

## 1. Text Generation Models (Core LLMs)

### Gemini 3 / 3.1 Family (Latest Generation)
* **Gemini 3.1 Pro**
  * *Category*: Text-out models
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `gemini-3.1-pro`
* **Gemini 3.1 Flash Lite**
  * *Category*: Text-out models
  * *Limits*: RPM: `4 / 15` | TPM: `6.98K / 250K` | RPD: `47 / 500`
  * *Exact Code Identifier*: `gemini-3.1-flash-lite`
* **Gemini 3 Flash**
  * *Category*: Text-out models
  * *Limits*: RPM: `3 / 5` | TPM: `743 / 250K` | RPD: `4/20`
  * *Exact Code Identifier*: `gemini-3-flash`

### Gemini 2 / 2.5 Family (Established Architecture)
* **Gemini 2.5 Pro**
  * *Category*: Text-out models
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `gemini-2.5-pro`
* **Gemini 2.5 Flash**
  * *Category*: Text-out models
  * *Limits*: RPM: `5 / 5` | TPM: `3.35K / 250K` | RPD: `23 / 20`
  * *Exact Code Identifier*: `gemini-2.5-flash`
* **Gemini 2.5 Flash Lite**
  * *Category*: Text-out models
  * *Limits*: RPM: `0 / 10` | TPM: `0 / 250K` | RPD: `0 / 20`
  * *Exact Code Identifier*: `gemini-2.5-flash-lite`
* **Gemini 2 Flash**
  * *Category*: Text-out models
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `gemini-2-flash`
* **Gemini 2 Flash Lite**
  * *Category*: Text-out models
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `gemini-2-flash-lite`

### Gemma Open Weights Series
* **Gemma 4 31B**
  * *Category*: Other models
  * *Limits*: RPM: `8 / 15` | TPM: `53.21K / Unlimited` | RPD: `134 / 1.5K`
  * *Exact Code Identifier*: `gemma-4-31b-it`
* **Gemma 4 26B**
  * *Category*: Other models
  * *Limits*: RPM: `0 / 15` | TPM: `0 / Unlimited` | RPD: `0 / 1.5K`
  * *Exact Code Identifier*: `gemma-4-26b-a4b-it`

---

## 2. Multi-Modal Generative Models (Image, Video, & Audio)

### Imagen Series (Image Generation)
* **Imagen 4 Ultra Generate**
  * *Limits*: RPD: `0 / 25` (RPM/TPM unlisted)
  * *Exact Code Identifier*: `imagen-4.0-ultra-generate-001`
* **Imagen 4 Generate**
  * *Limits*: RPD: `0 / 25` (RPM/TPM unlisted)
  * *Exact Code Identifier*: `imagen-4.0-generate-001`
* **Imagen 4 Fast Generate**
  * *Limits*: RPD: `0 / 25` (RPM/TPM unlisted)
  * *Exact Code Identifier*: `imagen-4.0-fast-generate-001`

### Nano Banana Models (Preview Multi-Modal Images)
* **Nano Banana 2 (Gemini 3.1 Flash Image)**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `nano-banana-2`
* **Nano Banana Pro (Gemini 3 Pro Image)**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `nano-banana-pro`
* **Nano Banana (Gemini 2.5 Flash Preview Image)**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `nano-banana`

### Veo Series (Video Synthesis)
* **Veo 3 Generate**
  * *Limits*: RPM: `0 / 0` | TPM: `-` | RPD: `0 / 0`
  * *Exact Code Identifier*: `veo-3.0-generate-001`
* **Veo 3 Fast Generate**
  * *Limits*: RPM: `0 / 0` | TPM: `-` | RPD: `0 / 0`
  * *Exact Code Identifier*: `veo-3.0-fast-generate-001`
* **Veo 3 Lite Generate**
  * *Limits*: RPM: `0 / 0` | TPM: `-` | RPD: `0 / 0`
  * *Exact Code Identifier*: `veo-3.0-lite-generate-001`

### Audio & Sound Generation (TTS & Lyria)
* **Gemini 3.1 Flash TTS**
  * *Limits*: RPM: `0 / 3` | TPM: `0 / 10K` | RPD: `0 / 10`
  * *Exact Code Identifier*: `gemini-3.1-flash-tts`
* **Gemini 2.5 Flash TTS**
  * *Limits*: RPM: `0 / 3` | TPM: `0 / 10K` | RPD: `0 / 10`
  * *Exact Code Identifier*: `gemini-2.5-flash-tts`
* **Gemini 2.5 Pro TTS**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `gemini-2.5-pro-tts`
* **Lyria 3 Pro**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `lyria-3-pro`
* **Lyria 3 Clip**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `lyria-3-clip`

---

## 3. Live API Models (Streaming Audio & Dialog)

* **Gemini 2.5 Flash Native Audio Dialog**
  * *Limits*: RPM: `0 / Unlimited` | TPM: `0 / 1M` | RPD: `0 / Unlimited`
  * *Exact Code Identifier*: `gemini-2.5-flash-audio-dialog`
* **Gemini 3 Flash Live**
  * *Limits*: RPM: `0 / Unlimited` | TPM: `0 / 65K` | RPD: `0 / Unlimited`
  * *Exact Code Identifier*: `gemini-3-flash-live`

---

## 4. Specialized Utility Models & Agents

### Embeddings
* **Gemini Embedding 2**
  * *Limits*: RPM: `0 / 100` | TPM: `0 / 30K` | RPD: `0 / 1K`
  * *Exact Code Identifier*: `text-embedding-005`
* **Gemini Embedding 1**
  * *Limits*: RPM: `0 / 100` | TPM: `0 / 30K` | RPD: `0 / 1K`
  * *Exact Code Identifier*: `text-embedding-004`

### Robotics & Physical Systems
* **Gemini Robotics ER 1.6 Preview**
  * *Limits*: RPM: `0 / 5` | TPM: `0 / 250K` | RPD: `0 / 20`
  * *Exact Code Identifier*: `gemini-robotics-er-1.6-preview`
* **Gemini Robotics ER 1.5 Preview**
  * *Limits*: RPM: `0 / 10` | TPM: `0 / 250K` | RPD: `0 / 20`
  * *Exact Code Identifier*: `gemini-robotics-er-1.5-preview`

### Previews & Agentic Execution
* **Computer Use Preview**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `computer-use-preview`
* **Deep Research Pro Preview**
  * *Limits*: RPM: `0 / 0` | TPM: `0 / 0` | RPD: `0 / 0`
  * *Exact Code Identifier*: `deep-research-pro-preview`

---

## 5. Tool Integrations & Grounding Overlays

These features are passed as properties inside the tools config file object rather than stand-alone model selections.

### Map Grounding Configuration
* *Object Code Config*: `{"google_maps_grounding": {}}`
* **Active Limits**:
  * `gemini-3.1-flash-lite`: RPD: `0 / 500`
  * `gemini-2.5-flash-lite`: RPD: `0 / 500`
  * `gemini-2.5-flash`: RPD: `0 / 500`
  * `gemini-3.1-flash-tts`: RPD: `0 / 500`
  * `gemini-robotics-er-1.6-preview`: RPD: `0 / 500`
  * `computer-use-preview`: RPD: `0 / 500`
  * `deep-research-pro-preview`: RPD: `0 / 500`
  * `gemini-3.1-pro`: RPD: `0 / 0`
  * `gemini-3-flash`: RPD: `0 / 0`
  * `gemini-2.5-pro`: RPD: `0 / 0`

### Search Grounding Configuration
* *Object Code Config*: `{"google_search_retrieval": {}}`
* **Active Limits**:
  * `default`: RPD: `0 / 1.5K`
  * `gemini-2-flash`: RPD: `0 / 1.5K`
  * `gemini-2.5-flash`: RPD: `0 / 1.5K`
  * `gemini-3-flash`: RPD: `0 / 0`