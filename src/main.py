import masks

number_card = input("Ведите номер карты. 16 чисел")

print(masks.get_mask_card_number(number_card))

print(masks.get_mask_account(number_card))
