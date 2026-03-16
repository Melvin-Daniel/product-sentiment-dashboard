"""
Keyword extraction utilities used by analytics and insights services.
"""
import re
from collections import Counter
from typing import Iterable, List, Dict

# Simple English stopwords for keyword extraction
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "is", "it", "this", "that", "are", "was", "were",
    "been", "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "can", "i", "you", "he", "she",
    "we", "they", "my", "your", "very", "not", "no", "just", "so", "as", "if",
}


def _tokenize(text: str) -> List[str]:
    """Lowercase and extract normalized word tokens (letters only, no numbers)."""
    if not text:
        return []
    lowered = (text or "").lower()
    # keep only alphabetic sequences
    words = re.findall(r"[a-z]+", lowered)
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]


def extract_keywords(texts: Iterable[str], top_n: int = 10) -> List[Dict[str, object]]:
    """Return top N keywords from an iterable of texts."""
    all_words = []
    for t in texts:
        all_words.extend(_tokenize(t or ""))
    counts = Counter(all_words)
    return [{"word": w, "count": c} for w, c in counts.most_common(top_n)]

