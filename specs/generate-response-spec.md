# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Each chunk is formatted as a Markdown header with the game name, followed by the
chunk text:

  ## Catan
  <chunk text>

  ## Pandemic
  <chunk text>

Chunks are separated by a blank line. The Markdown header makes the source
visually distinct so the model can correctly attribute its answer to the right
game. Distance scores are not included — they are an internal retrieval metric
already used for filtering in retrieve() and have no meaningful interpretation
for the LLM.
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are a board game rules assistant. Answer ONLY using the rule text provided in the context below.

Present your answer in this format: "Here is what I found in the [Game Name] rulebook: [exact quote from context]". Use the game name from the context header (## GameName). Do not restate or paraphrase the quote — let it speak for itself. Every sentence in your response must come directly from the provided context — nothing else.

Rules:
- Do not use any knowledge of board games from your training data.
- Do not complete, infer, or extend beyond what the retrieved text explicitly states.
- Do not resolve ambiguous language using knowledge of similar games.
- If the context does not contain a direct answer, respond with exactly: "That rule isn't in the loaded rulebooks. Try rephrasing your question or asking about a specific game."
- When in doubt, use the fallback. A confident wrong answer is worse than an honest I don't know.
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
[your answer here]
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
[your answer here]
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
[your answer here]
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: What happens when you run out of disease cubes in Pandemic?
Response: Here is what I found in the rulebook: "players lose immediately if: ...
          any color of disease cubes runs out when a cube must be placed"
Correctly grounded? Yes — answer comes directly from the retrieved chunk with no added knowledge.
Cited the right game? Yes — Pandemic chunks were retrieved and the answer is specific to Pandemic.
```

**One thing you changed from your original spec after seeing the actual output:**

```
Changed the response format from "quote first, then restate the answer" to
"Here is what I found in the rulebook: [quote]" — the original format was
redundant since the quote and the answer said the same thing. The new format
lets the quote speak for itself without repetition.
```
