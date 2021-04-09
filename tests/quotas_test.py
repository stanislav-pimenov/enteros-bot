from src.quotas import quota_exceeded

def test_should_not_exceed_quotas():
    user_id = 123
    assert quota_exceeded(user_id) is None
    assert quota_exceeded(user_id) is None
    assert quota_exceeded(user_id) is None
    assert quota_exceeded(user_id) is None
    assert quota_exceeded(user_id) is None
    assert quota_exceeded(user_id).startswith("Ssory")
