from src.enteros_bot import is_good_morning_nltk
from src.enteros_bot import lemminized_morning
from src.enteros_bot import prepare_response

def test_should_return_message_on_good_morning():
    assert is_good_morning_nltk('Доброго утра!')

def test_should_return_parsed_lemmas():
    parse = lemminized_morning('Всех с добром утром и счастливого Нового Года!')
    print("normalize_form", parse)
    assert parse is not None
    response = prepare_response(parse)
    assert response == 'хуютром!'

def test_should_not_return_message_on_unknown_message():
    assert not is_good_morning_nltk('Брахмапутра!')
