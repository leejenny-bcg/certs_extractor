"""Shared text normalization so benefit names and document text are
matched on identical footing (lowercase, punctuation stripped, lemmatized).
"""
import re
import simplemma

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize_and_lemmatize(text):
    """Lowercase, extract alnum tokens, lemmatize each. Returns list of tokens."""
    text = text.lower()
    tokens = _TOKEN_RE.findall(text)
    return [simplemma.lemmatize(t, lang="en") for t in tokens]


def normalized_key(text):
    """Normalized matching key for a benefit name or phrase: space-joined lemmas."""
    return " ".join(tokenize_and_lemmatize(text))
