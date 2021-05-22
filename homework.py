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
        week_ago = today - dt.timedelta(days=7)
        return sum(i.amount for i in self.records if i.date >= week_ago)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self, limit):
        calories_limit = self.get_today_stats()
        if calories_limit <= limit:
            over_limit = limit - calories_limit
            return f'Сегодня можно съесть что-нибудь ещё, \
                но с общей калорийностью не более {over_limit} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 73.99
    EURO_RATE = 89.67

    def get_today_cash_remained(self, currency):
        self.currency = currency
        money_type = ''
        if currency.lower() == 'rub':
            money_type = 'руб'
            cash_remained = round(self.limit - self.get_today_stats())
            debt = abs(round(self.get_today_stats() - self.limit))
        elif currency.lower() == 'usd':
            money_type = 'USD'
            cash_remained = round((self.limit - self.get_today_stats())
                                  / self.USD_RATE)
            debt = abs(round((self.get_today_stats() - self.limit)
                             / self.USD_RATE, 2))
        elif currency.lower() == 'eur':
            money_type = 'Euro'
            cash_remained = round((self.limit - self.get_today_stats())
                                  / self.EURO_RATE)
            debt = abs(round((self.get_today_stats() - self.limit)
                             / self.EURO_RATE, 2))
        if self.get_today_stats() == 0:
            return 'Денег нет, держись'
        if self.get_today_stats() < round(self.limit):
            return f'На сегодня осталось {cash_remained} {money_type}'
        elif self.get_today_stats() == round(self.limit):
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {debt} {money_type}'


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
