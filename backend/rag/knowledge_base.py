import re
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "dhivya_profile.md"


def load_knowledge_base() -> list[dict]:
    """Load and chunk the knowledge base markdown file into sections."""
    if not DATA_PATH.exists():
        return []

    content = DATA_PATH.read_text(encoding="utf-8")
    return _chunk_by_sections(content)


def _chunk_by_sections(content: str) -> list[dict]:
    """Split markdown into header-delimited chunks."""
    sections = re.split(r"\n(?=#{1,3} )", content)
    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split("\n")
        title = lines[0].lstrip("#").strip() if lines[0].startswith("#") else "General"
        body = "\n".join(lines[1:]).strip()

        if body or title != "General":
            chunks.append(
                {
                    "title": title,
                    "content": section,
                    "keywords": _extract_keywords(section),
                }
            )

    return chunks


def _extract_keywords(text: str) -> set:
    """Extract meaningful lowercase words (3+ chars) from text."""
    stop_words = {
        "the", "and", "for", "are", "with", "that", "this", "from",
        "have", "has", "been", "was", "will", "her", "she", "his",
        "him", "they", "their", "also", "all", "can", "any", "not",
        "but", "you", "your", "who", "what", "how", "when", "where",
    }
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", text.lower())
    return set(words) - stop_words


def _score_chunk(chunk: dict, query_keywords: set) -> float:
    """BM25-inspired overlap score between query keywords and chunk keywords."""
    if not query_keywords or not chunk["keywords"]:
        return 0.0
    overlap = len(query_keywords & chunk["keywords"])
    # Normalize by query length to prefer more specific matches
    return overlap / max(len(query_keywords), 1)


def search_knowledge_base(query: str, top_k: int = 4) -> str:
    """Search the personal knowledge base for information about Dhivya."""
    chunks = load_knowledge_base()

    if not chunks:
        return (
            "The personal knowledge base is not yet configured. "
            "Please update backend/data/dhivya_profile.md with profile information."
        )

    query_keywords = _extract_keywords(query)
    scored = sorted(
        [(chunk, _score_chunk(chunk, query_keywords)) for chunk in chunks],
        key=lambda x: x[1],
        reverse=True,
    )

    # Include chunks with score > 0, or fall back to all top-k chunks
    top = [chunk for chunk, score in scored[:top_k] if score > 0]
    if not top:
        top = [chunk for chunk, _ in scored[:top_k]]

    results = [f"[{c['title']}]\n{c['content']}" for c in top]
    return "Personal Knowledge Base Results:\n\n" + "\n\n---\n\n".join(results)
