from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    translated_content = translated_content.lower()
    assert "chinese" in translated_content and "message" in translated_content and "this" in translated_content


def test_spanish():
    is_english, translated_content = translate_content("Este es un mensaje en espanol")
    assert is_english == False
    translated_content = translated_content.lower()
    assert "spanish" in translated_content and "message" in translated_content and "this" in translated_content


def test_french():
    is_english, translated_content = translate_content("Ceci est un message en francais")
    assert is_english == False
    translated_content = translated_content.lower()
    assert "french" in translated_content and "message" in translated_content and "this" in translated_content


def test_japanese():
    is_english, translated_content = translate_content("これは日本語のメッセージです")
    assert is_english == False
    translated_content = translated_content.lower()
    assert "japanese" in translated_content and "message" in translated_content and "this" in translated_content

def test_llm_normal_response():
    is_english, translated_content = translate_content("Je parle en francais, donc beaucoup de ces exemples seront en francais.")
    assert is_english == False
    translated_content = translated_content.lower()
    assert "french" in translated_content and "these examples" in translated_content

def test_llm_gibberish_response():
    is_english, translated_content = translate_content("efghwoepjfbwejn")
    assert is_english == False
    assert translated_content == "efghwoepjfbwejn"