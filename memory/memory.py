from mcp.server.fastmcp import FastMCP

from .mem.database import Database

mcp = FastMCP("Memory")
db = Database()


@mcp.tool()
def memorize(text: str) -> str:
    """Memorize a text"""
    db.memorize(text)
    return "Text memorized!"


@mcp.tool()
def recall(query: str, n_results: int = 1):
    """Recall a text"""
    results = db.recall(query, n_results)
    if not results:
        return "No results found."

    return results
