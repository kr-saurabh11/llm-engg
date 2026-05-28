import re
import html

def sanitize_llm_response(text: str) -> str:
    if not text:
        return ""
    # Decode escaped HTML entities
    text = html.unescape(text)
    # Remove reasoning / internal tags
    text = re.sub(
        r"<(thought|think|analysis|reasoning).*?>.*?</\1>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    # Remove XML / HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )
    return text.strip()