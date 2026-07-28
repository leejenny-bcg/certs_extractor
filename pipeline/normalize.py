"""Shared text normalization so benefit names and document text are
matched on identical footing (lowercase, punctuation stripped, lemmatized).

spaCy branch: uses spaCy's POS-aware lemmatizer instead of simplemma's
context-free dictionary lookup. Motivation, found empirically (not just
theorized) while investigating why "Contact Lenses" and "contact lens"
weren't merging: simplemma lemmatizes "lenses" -> "lense" (not a real
word) in every context, and separately can't distinguish "diagnoses" the
plural noun ("a history of diagnoses" -> should be "diagnosis") from
"diagnoses" the verb ("the doctor diagnoses X" -> should stay "diagnose"),
because it has no part-of-speech information to disambiguate. spaCy tags
POS first, then lemmatizes based on that tag, so it gets both right:

    "Contact Lenses"                     -> lens (NOUN)
    "The diagnoses of a condition"       -> diagnosis (NOUN)
    "The doctor diagnoses the condition" -> diagnose (VERB)

Caveat, also found empirically: spaCy's small model can still mistag short,
context-poor noun phrases (exactly the shape of our candidate names) - e.g.
"Laboratory analyses" alone gets tagged as a VERB, giving the wrong lemma.
So this is a real improvement over simplemma, not a guaranteed-perfect fix.
LEMMA_CORRECTIONS is kept as a cheap safety net for any such residual
errors found by testing, the same role it played for simplemma's "lense" bug.

Requires: pip install spacy && python -m spacy download en_core_web_sm
"""
import re

import spacy

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# parser and ner are not needed for lemmatization/POS and roughly halve
# per-call latency when disabled; tok2vec/tagger/attribute_ruler stay
# because the lemmatizer's rules key off the POS tag they produce.
_NLP = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Found by testing (not theorized): spaCy's tagger, with no sentence
# context, mistags a bare "lens" as plural (NNS) and its lemmatizer then
# strips a wrong "s"-like suffix, landing on "len" - never a real word, so
# remapping it back is unambiguous and safe, same rule as simplemma's
# "lense" bug. Also keeping "lense" itself: the Topic Tree's own raw data
# contains that literal misspelling ("Aphakic lense", "Blended lense"),
# and spaCy - correctly - has no rule to "fix" a misspelling that isn't a
# real inflected form, so it passes through unchanged. Remapping it here
# isn't lemmatization fixing a typo; it's this pipeline choosing to treat
# the tree's known misspelling as equivalent to the correctly-spelled word,
# the same normalization outcome simplemma produced by accident.
LEMMA_CORRECTIONS = {"len": "lens", "lense": "lens"}


def tokenize_and_lemmatize(text):
    """Lowercase, extract alnum tokens, lemmatize each via spaCy (POS-aware).
    Returns list of tokens."""
    text = text.lower()
    if not _TOKEN_RE.search(text):
        return []
    doc = _NLP(text)
    lemmas = [tok.lemma_ for tok in doc if _TOKEN_RE.fullmatch(tok.text)]
    return [LEMMA_CORRECTIONS.get(lemma, lemma) for lemma in lemmas]


def normalized_key(text):
    """Normalized matching key for a benefit name or phrase: space-joined lemmas."""
    return " ".join(tokenize_and_lemmatize(text))
