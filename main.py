import chainlit as cl
from nlp.foreign_filter import is_foreign_law_question
from tools.vector_tool import vector_tool
from tools.web_tool import web_tool
from agents.legal_agent import llm

@cl.on_message
async def main(message: cl.Message):
    query = message.content.strip()

    if is_foreign_law_question(query):
        await cl.Message(
            content="⚠️ I'm trained only on **Pakistani law**. I cannot provide legal advice for other countries.",
            author="SmartLegalAgent"
        ).send()
        return

    vector_answer = vector_tool.func(query)
    web_answer = web_tool.func(query)

    system_prompt = f"""
You are SmartLegalAgent, a Pakistani legal assistant trained only on Pakistani law.

You are given:
- Text from Pakistan law documents (Vector DB)
- Text from recent web search (if any)

Your job:
- Understand both sources.
- Answer the user's question clearly, professionally, and concisely (in **2-4 lines**).
- **Always include the specific section and name of the law** (e.g., "Section 21 of PECA 2016").
- **Do not suggest third-party legal firms or say 'consult a lawyer'** unless absolutely necessary.
- Only reply if the question relates to Pakistani law. If it refers to foreign law, say: “⚠️ I’m trained only on Pakistani law.”
- Avoid vague language. Make your answers sound like a **real legal expert**.
- Never give generic advice. Be specific, legal, and authoritative.

--- LAW DOCUMENTS ---
{vector_answer}
--- INTERNET SEARCH ---
{web_answer}

Now provide a concise and authentic legal answer (in 2-4 lines):
"""

    final_response = await llm.ainvoke(system_prompt.strip())
    concise_answer = final_response.content.strip()

    if "section" not in concise_answer.lower() and "act" not in concise_answer.lower():
        updated_prompt = system_prompt + "\n\nNote: Make sure your answer includes at least one relevant Section or Act from Pakistani law."
        final_response = await llm.ainvoke(updated_prompt.strip())
        concise_answer = final_response.content.strip()

    await cl.Message(content=concise_answer, author="SmartLegalAgent").send()

@cl.on_chat_start
async def start():
    await cl.Message(
        author="",
        content="👋 Hello! I'm **SmartLegalAgent**, your legal assistant. Ask me anything about Pakistani law."
    ).send()
