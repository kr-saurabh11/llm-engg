import re
import html

# Pre‑compile regex patterns for performance – they are reused on every call
_REASONING_RE = re.compile(r"<(thought|think|analysis|reasoning).*?>.*?</\1>", flags=re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")

def sanitize_llm_response(text: str) -> str:
    """Clean LLM output.

    * Decode HTML entities.
    * Strip any reasoning / internal tags (e.g. <thought>...</thought>).
    * Remove any remaining HTML/XML tags.
    * Return a trimmed string.
    """
    if not text:
        return ""
    # Decode escaped HTML entities – cheap operation, always safe
    text = html.unescape(text)
    # Remove reasoning / internal tags using the pre‑compiled pattern
    text = _REASONING_RE.sub("", text)
    # Remove any other HTML/XML tags
    text = _TAG_RE.sub("", text)
    return text.strip()