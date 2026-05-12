import re

# Simple prompt‑injection shield
# Returns a cleaned version of the user prompt or an empty string if it looks malicious.

def sanitize_prompt(prompt: str) -> str:
    """Remove dangerous patterns that could lead to prompt injection.
    The logic is intentionally conservative – anything that looks like code execution
    or attempts to break out of the intended context is rejected.
    """
    # Lower‑case for easier matching
    lowered = prompt.lower()

    # Very common attack vectors – block if they appear
    blacklists = [
        "import ",
        "os.",
        "sys.",
        "subprocess",
        "eval(",
        "exec(",
        "__import__",
        "`",  # backticks
        "$(",
        "|",
        ";",
        "&&",
        "||",
    ]
    for bad in blacklists:
        if bad in lowered:
            return ""  # reject completely

    # Remove any stray curly‑brace placeholders that could be used for jailbreaks
    # e.g. {{some_injection}}
    cleaned = re.sub(r"\{\{.*?\}\}", "", prompt)
    return cleaned.strip()
