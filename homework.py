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
        today = dt.date.today()
        return sum(i.amount for i in self.records
                   if i.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        return sum(i.amount for i in self.records
                   if today >= i.date >= week_ago)

    def get_balance(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_limit = self.get_today_stats()
        if calories_limit <= self.limit:
            over_limit = self.get_balance()
            return ''.join(['Сегодня можно съесть что-нибудь ещё, ',
                           f'но с общей калорийностью не более {over_limit}'
                            ' кКал'])
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 73.99
    EURO_RATE = 89.67

    def get_today_cash_remained(self, currency):
        currency_info = {
            'rub': (self.RUB_RATE, 'руб',),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }

        cash_remained = self.get_balance()
        if cash_remained == 0:
            return 'Денег нет, держись'

        rate, title = currency_info[currency.lower()]
        if rate != 1.0:
            cash_remained = round(cash_remained / rate, 2)

        if cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {title}'
        debt = abs(cash_remained)
        return f'Денег нет, держись: твой долг - {debt} {title}'
