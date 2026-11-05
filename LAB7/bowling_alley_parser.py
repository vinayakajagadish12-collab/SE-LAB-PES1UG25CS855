def format_player_name(name):
    """Return a title-cased, ten-character name; non-strings become empty."""
    return name.strip().title()[:10] if isinstance(name, str) else ""


def parse_frame(text):
    """Parse X, digit/spare, or two ASCII digits; invalid frames return None."""
    if not isinstance(text, str):
        return None
    text = text.strip().upper()
    if text == "X":
        return (10, 0)
    if len(text) != 2 or text[0] not in "0123456789":
        return None
    first = int(text[0])
    if text[1] == "/":
        return (first, 10 - first)
    if text[1] not in "0123456789":
        return None
    second = int(text[1])
    return (first, second) if first + second <= 10 else None


def parse_scoreboard(text):
    """Parse name:score pairs atomically; invalid input returns {}.

    Scores must be ASCII integers from 0 to 300. Empty or duplicate names
    are rejected, avoiding silent data loss. Whitespace is permitted.
    """
    if not isinstance(text, str) or not text.strip():
        return {}
    scores = {}
    for entry in text.split(","):
        parts = entry.split(":")
        if len(parts) != 2:
            return {}
        name, score = (part.strip() for part in parts)
        if not name or name in scores or not score or not all(c in "0123456789" for c in score):
            return {}
        # Remove leading zeros before conversion to avoid Python's digit limit.
        score = score.lstrip("0") or "0"
        if len(score) > 3 or int(score) > 300:
            return {}
        scores[name] = int(score)
    return scores


def main():
    print("==== Running format_player_name ====")
    value = input("Enter a player name for the scoreboard: ")
    print("Scoreboard name:", format_player_name(value))

    print("\n==== Running parse_frame ====")
    value = input("Enter a frame as X (strike), 7/ (spare) or two digits (e.g. 45): ")
    print("Pins (first roll, second roll):", parse_frame(value))

    print("\n==== Running parse_scoreboard ====")
    value = input("Enter scores as NAME:SCORE separated by commas (e.g. Asha:150,Ravi:132): ")
    print("Scoreboard:", parse_scoreboard(value))

if __name__ == "__main__":
    main()
