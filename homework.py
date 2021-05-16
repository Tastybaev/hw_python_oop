import datetime as dt
from typing import Optional


class Record:
    def __init__(self, amount: float, comment: str, \
        date: Optional[str] = None) -> None:
            self.amount = amount
            self.comment = comment
            if date is None:
                self.date = dt.datetime.today().date()
            else:
                self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def add_record(self, record: Record):
        self.records.append(record)


    def __init__(self, limit):
        self.limit = limit
        self.records= []


    def get_today_stats(self):
        return sum(i.amount for i in self.records \
            if i.date == dt.datetime.today().date())


    def get_week_stats(self):
        day_week_ago = dt.datetime.today().date() - dt.timedelta(days=7)
        return sum(i.amount for i in self.records if i.date >= day_week_ago)


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

        cash_remained = self.limit - self.get_today_stats()
        if rate != 1.0:
            cash_remained = round(cash_remained/rate, 2)

        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {cash_remained} {cur_name}'
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        else:
            debt = abs(round((self.get_today_stats() - self.limit)/rate, 2))
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
 