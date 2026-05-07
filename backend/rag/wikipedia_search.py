import wikipedia


def search_wikipedia(query: str, n_results: int = 2, max_chars: int = 3000) -> str:
    """Search Wikipedia and return formatted results."""
    try:
        titles = wikipedia.search(query, results=n_results + 3)

        if not titles:
            return f"No Wikipedia results found for: {query}"

        retrieved = []
        for title in titles:
            if len(retrieved) >= n_results:
                break
            try:
                page = wikipedia.page(title, auto_suggest=False)
                content = page.content[:max_chars]
                retrieved.append(
                    f"Title: {page.title}\nURL: {page.url}\n\nContent:\n{content}"
                )
            except (
                wikipedia.exceptions.DisambiguationError,
                wikipedia.exceptions.PageError,
            ):
                continue

        if not retrieved:
            return f"Could not retrieve Wikipedia content for: {query}"

        return "Wikipedia Search Results for '{}':\n\n{}".format(
            query, "\n\n---\n\n".join(retrieved)
        )

    except Exception as e:
        return f"Wikipedia search error: {str(e)}"
