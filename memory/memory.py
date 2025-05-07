from mcp.server.fastmcp import FastMCP

from .database import Database

mcp = FastMCP(
    name="Long-Term Memory",
    instructions="""
    This service manages the AI's persistent memory system. It allows storing and retrieving information across conversations and sessions.

    Use this service when you need to:
    - Store important information the AI should remember for future interactions
    - Retrieve previously stored memories that are relevant to the current conversation

    The memory system uses semantic search to find relevant information based on meaning,
    not just keywords. Information stored here persists beyond the current session.
    """
)
db = Database()


@mcp.tool()
def memorize(content: str, description: str | None = None) -> bool:
    """Store a new memory in the AI's long-term memory database.

    This function creates a persistent memory by storing the provided content
    in a vector database for later retrieval. Each memory can optionally include
    a description to aid in organization and recall.

    Parameters
    ----------
    content : str
        The main text content to be remembered (e.g., facts, observations,
        conversations, or other information worth preserving)
    description : str, optional
        A short summary or label for this memory to aid in organization

    Returns
    -------
    bool
        Confirmation status indicating whether the memory was successfully stored

    Examples
    --------
    >>> memorize("The user prefers dark mode in all applications")
    "Memory successfully stored!"

    >>> memorize("User's birthday is May 15", "Personal preference")
    "Memory successfully stored!"
    """
    if description:
        memory_text = f"{description}: {content}"
    else:
        memory_text = content

    db.memorize(memory_text)
    return True


@mcp.tool()
def recall(query: str, limit: int = 10) -> list:
    """Retrieve memories from the AI's long-term memory database.

    This function searches the memory database for content that semantically matches
    the provided query. It returns the most relevant memories based on vector similarity,
    allowing the AI to access previously stored information.

    Parameters
    ----------
    query : str
        The search query describing the memories you want to retrieve
        (e.g., "user's birthday" or "preferences about UI design")
    limit : int, default=10
        Maximum number of memories to retrieve

    Returns
    -------
    list
        A list of memories that match the query.
        If no memories are found, returns empty list.

    Examples
    --------
    >>> recall("user preferences")
    ['User prefers dark mode in all applications', 'User likes to be addressed as Sam']

    >>> recall("meeting schedule", limit=5)
    ['Weekly team meeting every Monday at 10am', 'Project deadline meeting scheduled for June 15']
    """
    memories = db.recall(query, n_results=limit)
    return memories
