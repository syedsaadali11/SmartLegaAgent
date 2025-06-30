# 🤖 SmartLegalAgent 🇵🇰

SmartLegalAgent is an AI-powered legal assistant specialized in **Pakistani law**.  
It uses **LangChain**, **ChromaDB**, **LLMs**, and **Chainlit** to provide concise, authoritative legal responses based on:

- Pakistan law documents (via embeddings)
- Web search results (via Tavily)
- NLP-powered foreign law detection

---

## 🚀 Features

- ✅ Answers legal questions about Pakistani law  
- 🔍 Uses **Chroma VectorDB** for document retrieval  
- 🌐 Web search via **Tavily API**  
- 🧠 Smart filtering using **spaCy** to detect foreign law questions  
- 🧵 Chainlit-based interactive chat interface  
- 🔐 API key management with `.env`

---

## 🧠 Tech Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| 🧠 LLM       | Mistral via OpenRouter      |
| 🧰 Embeddings| HuggingFace (`MiniLM`)     |
| 📚 Vector DB | ChromaDB                    |
| 🌍 Search    | Tavily                      |
| 💬 Chat UI   | Chainlit                    |
| 📦 Framework | LangChain                   |
| 🧪 NLP       | spaCy (`en_core_web_sm`)    |

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/syedsaadali11/SmartLegaAgent.git
cd SmartLegaAgent

# 2. Install requirements
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Create .env file and add your keys
# OPENROUTER_API_KEY=your_openrouter_api_key
# TAVILY_API_KEY=your_tavily_api_key

# 4. Run the app
chainlit run main.py
