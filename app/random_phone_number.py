import random

area_codes = ["305", "516", "650", "301", "561", "713", "425", "914", "817", "631"]

def generate_subscriber_number():
    number = ""
    for i in range(0, 7):
        if (i == 0):
            number += str(random.randint(2, 9))
        if (i == 2):
            number += "-"
        else:
            number += str(random.randint(0, 9))
    return number

def generate_phone_number():
    phone_number = ""
    phone_number += str(area_codes[random.randint(0, 9)])
    phone_number += "-"
    phone_number += generate_subscriber_number()
    return phone_number

