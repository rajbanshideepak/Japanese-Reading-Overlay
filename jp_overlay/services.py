import requests
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()


def katakana_to_hiragana(text: str) -> str:
    result = []
    for ch in text:
        code = ord(ch)
        if 0x30A1 <= code <= 0x30F6:
            result.append(chr(code - 0x60))
        else:
            result.append(ch)
    return "".join(result)

def get_furigana(text):
    words = []
    for token in tokenizer.tokenize(text):
        surface = token.surface
        reading = getattr(token, "reading", "*")

        if reading and reading != "*":
            hira = katakana_to_hiragana(reading)
            words.append(hira)
        else:
            words.append(surface)

    # Join with spaces
    return " ".join(words)

# def get_furigana(text: str) -> str:
    result = []
    for token in tokenizer.tokenize(text):
        surface = token.surface
        reading = getattr(token, "reading", "*")
        if reading and reading != "*":
            result.append(reading)
        else:
            result.append(surface)
    katakana = "".join(result)
    return katakana_to_hiragana(katakana)

# def translate_ja_to_en(text):
    try:
        r = requests.post(
            "https://libretranslate.de/translate",
            data={
                "q": text,
                "source": "ja",
                "target": "en",
                "format": "text",
                "api_key": ""
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        r.raise_for_status()
        return r.json().get("translatedText", "[No translation returned]")
    except Exception as e:
        return f"[Translation error: {e}]"
    

def translate_ja_to_en(text):
    try:
        r = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": "ja|en"
            },
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        return data.get("responseData", {}).get("translatedText", "[No translation returned]")
    except Exception as e:
        return f"[Translation error: {e}]"