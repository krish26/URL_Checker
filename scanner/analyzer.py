import re
from urllib.parse import urlparse

def analyze_url(url):
    reasons = []
    score = 0

    parsed = urlparse(url)
    domain = parsed.netloc

    # Rule 1: Keywords
    keywords = ["login", "verify", "secure", "account", "bank"]
    if any(word in url.lower() for word in keywords):
        reasons.append("Contains phishing-related keywords")
        score += 1

    # Rule 2: Long URL
    if len(url) > 75:
        reasons.append("Unusually long URL")
        score += 1

    # Rule 3: IP instead of domain
    if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
        reasons.append("Uses IP address instead of domain")
        score += 2

    # Rule 4: Too many subdomains
    if domain.count('.') > 3:
        reasons.append("Too many subdomains")
        score += 1

    # Rule 5: No HTTPS
    if parsed.scheme != "https":
        reasons.append("Not using HTTPS")
        score += 1

    # Risk level
    if score == 0:
        level = "Safe"
    elif score <= 2:
        level = "Low Risk"
    else:
        level = "High Risk"

    return {
        "is_suspicious": score > 0,
        "risk_level": level,
        "score": score,
        "reasons": reasons
    }