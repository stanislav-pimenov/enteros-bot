from datetime import date

quotas = {}
LIMIT_PER_DAY = 5


class Quota:
    def __init__(self, user_id):
        self.user_id = user_id
        self.counter = 1
        self.current_date = date.today()

    def inc(self):
        self.counter += 1

    def __repr__(self):
        return 'User: ' + str(self.user_id) + ' date: ' + self.current_date.strftime("%d.%m.%Y") + ' counter: ' + str(
            self.counter)


def quota_exceeded(from_id: int):
    quota = quotas.get(from_id)
    if quota:
        today = date.today()
        if quota.current_date < today:
            quotas[from_id] = Quota(from_id)
        else:
            if quota.counter >= LIMIT_PER_DAY:
                return "Ssory, Больше 5ти титек на пользователя в день не положено"
            else:
                quota.inc()
    else:
        quotas[from_id] = Quota(from_id)