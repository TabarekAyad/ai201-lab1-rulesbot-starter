from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    context = "\n\n".join(
        f"## {chunk['game']}\n{chunk['text']}" for chunk in retrieved_chunks
    )

    system_message = (
        "You are a board game rules assistant. Answer ONLY using the rule text provided in the context below.\n\n"
        "Present your answer in this format: \"Here is what I found in the [Game Name] rulebook: [exact quote from context]\". "
        "Use the game name from the context header (## GameName). "
        "Do not restate or paraphrase the quote — let it speak for itself. "
        "Every sentence in your response must come directly from the provided context — nothing else.\n\n"
        "Rules:\n"
        "- Do not use any knowledge of board games from your training data.\n"
        "- Do not complete, infer, or extend beyond what the retrieved text explicitly states.\n"
        "- Do not resolve ambiguous language using knowledge of similar games.\n"
        "- If the context does not contain a direct answer, respond with exactly: "
        "\"That rule isn't in the loaded rulebooks. Try rephrasing your question or asking about a specific game.\"\n"
        "- When in doubt, use the fallback. A confident wrong answer is worse than an honest I don't know."
    )

    user_message = f"Here are the relevant rule excerpts:\n\n{context}\n\nQuestion: {query}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
