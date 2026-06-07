# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
Use _collection.query() with:
  - query_texts : [query] — an indexed list containing the single query string
  - n_results   : n_results — 3 top results to return, passed from the function parameter
  - include     : ["documents", "metadatas", "distances"] — request chunk text, game metadata, and cosine distance scores
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
One item in the return list:
  {
    "text"     : the chunk text string — sourced from results["documents"][0][i]
    "game"     : the game name string  — sourced from results["metadatas"][0][i]["game"]
    "distance" : the cosine distance float — sourced from results["distances"][0][i]
  }
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
_collection.query() returns nested lists because it supports batching — you can pass
multiple query strings at once and get back one list of results per query. The outer
list has one entry per query in query_texts.

Since we always pass a single query (query_texts=[query]), we use index [0] on
documents, metadatas, and distances to get the flat list of results for our one query.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
Filter results to only include chunks with distance <= 0.5, keeping up to 3 relevant
chunks. Chunks above 0.5 are too dissimilar to be useful context.

Tradeoffs:
- Filtering here (chosen): removes noise before the LLM sees the prompt. Threshold of
  0.5 on cosine distance is a reasonable cutoff for meaningful similarity. Small chunks
  embed narrow meaning, so a relevant chunk phrased differently from the query may score
  poorly and get dropped incorrectly. Large chunks embed broader meaning and are less
  sensitive to phrasing, but a bad threshold could still discard the only chunk that
  contains the answer.
- No filtering: all n_results reach generator.py with their distance scores. The LLM
  can reason over weak matches and say "I don't know" rather than silently dropping
  context, but irrelevant chunks waste prompt space and can confuse the model.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: [your test query]
Top result game: [game name]
Distance score: [score]
Does it make sense? [yes / no / explain]
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
