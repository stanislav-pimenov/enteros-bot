from src.enteros_bot import is_good_morning_nltk


def test_should_return_message_on_good_morning():
    assert is_good_morning_nltk('Доброго утра!')

def test_should_not_return_message_on_unknown_message():
    assert not is_good_morning_nltk('Брахмапутра!')
