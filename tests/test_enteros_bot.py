from src.enteros_bot import is_good_morning_nltk
from src.enteros_bot import lemminized_morning
from src.enteros_bot import prepare_response

def test_should_return_message_on_good_morning():
    assert is_good_morning_nltk('Доброго утра!')

def test_should_return_parsed_lemmas():
    parse = lemminized_morning('Всех с добром утром и счастливого Нового Года!')
    assert parse is not None
    response = prepare_response(parse)
    assert response == 'хуютром!'

def test_should_return_parsed_lemmas_for_adjectives():
    parse = lemminized_morning('Без утреннего кофе жизнь день по бороде')
    assert parse is not None
    response = prepare_response(parse)
    assert response == 'хуютреннего!'

def test_should_return_parsed_lemmas_for_adverb():
    parse = lemminized_morning('Вышел рано утром')
    assert parse is not None
    response = prepare_response(parse)
    assert response == 'хуютром!'

def test_should_not_return_message_on_unknown_message():
    assert not is_good_morning_nltk('Брахмапутра!')
