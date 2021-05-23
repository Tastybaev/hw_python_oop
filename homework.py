import datetime as dt
from typing import Optional


class Record:
    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def add_record(self, record: Record):
        self.records.append(record)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_today_stats(self):
        return sum(i.amount for i in self.records
                   if i.date == dt.date.today())

    def get_week_stats(self):
        today = dt.date.today()
        tomorrow = today + dt.timedelta(days=1)
        week_ago = today - dt.timedelta(days=7)
        return sum(i.amount for i in self.records if i.date >= week_ago
                   and i.date < tomorrow)


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_limit = self.get_today_stats()
        if calories_limit <= self.limit:
            over_limit = self.limit - calories_limit
            return f'Сегодня можно съесть что-нибудь ещё,\
                но с общей калорийностью не более {over_limit} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 89.67
    USD_RATE = 73.99
    EXCHANGE_RATE = {
        'rub': 1,
        'usd': 73.99,
        'eur': 89.67,
    }

    CURRENCY_NAME = {
        'rub': 'руб',
        'usd': 'USD',
        'eur': 'Euro',
    }

    def get_today_cash_remained(self, currency):
        cur = currency.lower()
        cur_name = CashCalculator.CURRENCY_NAME[cur]
        rate = CashCalculator.EXCHANGE_RATE[cur]

        cash_remained = round(self.limit - self.get_today_stats(), 2)
        if rate != 1.0:
            cash_remained = round(cash_remained / rate, 2)

        if round(self.get_today_stats(), 2) < self.limit:
            return f'На сегодня осталось {cash_remained} {cur_name}'
        elif round(self.get_today_stats(), 2) == self.limit:
            return 'Денег нет, держись'
        else:
            debt = abs(round((self.get_today_stats(), 2)) - self.limit
                            / abs(round(rate, 2)))
            return f'Денег нет, держись: твой долг - {debt} {cur_name}'


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб
caloriescalculator = CaloriesCalculator(1000)
caloriescalculator.add_record(Record(amount=900,
            comment='Кусок тортика. И ещё один.',))
print(caloriescalculator.get_calories_remained())