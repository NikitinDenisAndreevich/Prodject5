from src.widget import get_date, mask_account_card

number_card = input("Ведите номер карты. 16 чисел")

print(mask_account_card(number_card))
date = input("введите дату.")
get_date(date)
