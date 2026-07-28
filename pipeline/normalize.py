"""Shared text normalization so benefit names and document text are
matched on identical footing (lowercase, punctuation stripped, lemmatized).
"""
import re
import simplemma

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# simplemma mis-lemmatizes a handful of irregular plurals to a non-word
# output (confirmed: "lenses" -> "lense", which is never a correct English
# word on its own, so remapping it is unambiguous and safe). Deliberately
# NOT included: "diagnoses"/"analyses" also lemmatize wrong ("diagnose"/
# "analyse"), but those outputs ARE real words - the verb forms "diagnosed"/
# "diagnosing"/"analyzed"/"analyzing" lemmatize to the same string, so
# remapping "diagnose"->"diagnosis" would wrongly merge the noun ("a
# diagnosis") with the unrelated verb ("we diagnose/diagnosed X"). Only add
# a correction here when the broken output has no other legitimate meaning.
LEMMA_CORRECTIONS = {"lense": "lens"}


def tokenize_and_lemmatize(text):
    """Lowercase, extract alnum tokens, lemmatize each. Returns list of tokens."""
    text = text.lower()
    tokens = _TOKEN_RE.findall(text)
    lemmas = [simplemma.lemmatize(t, lang="en") for t in tokens]
    return [LEMMA_CORRECTIONS.get(lemma, lemma) for lemma in lemmas]


def normalized_key(text):
    """Normalized matching key for a benefit name or phrase: space-joined lemmas."""
    return " ".join(tokenize_and_lemmatize(text))
