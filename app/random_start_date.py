import random
#skip days 29 - 31 for easy logic
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]

def generate_date():
    date_string = "2020-" + months[random.randint(0, 11)] + "-" + days[random.randint(0, 27)]
    return date_string