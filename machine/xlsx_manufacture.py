import os
import random
import sys
import json
import openpyxl
import time
import tkinter as tk
import concurrent.futures
import psutil
from tkinter import messagebox
from datetime import date, timedelta, datetime

card_numbers_path = os.path.join(os.path.dirname(__file__), f"./dict/card_numbers.json")

if card_numbers_path:
    pass
else:
    open(card_numbers_path, 'w')

    
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def generate_and_save_cards(number_of_cards):
    output_file_path = os.path.join(os.path.dirname(__file__), f"./dict/card_numbers.json")
    
    def generate_unique_card_list():
        card_list = set()
        while len(card_list) < number_of_cards:
            power = random.choice([15, 16, 17, 18])
            card = random.randint(10 ** power, 10 ** (power + 1) - 1)

            card_str = str(random.choice([2, 3, 4, 5])) + str(card)

            # Check if the card is already in the list
            if card_str not in card_list:
                card_list.add(card_str)

        return list(card_list)

    try:
        card_list = generate_unique_card_list()

        # Check if the generated list is not empty
        if not card_list:
            raise ValueError("Generated card list is empty.")

        with open(output_file_path, 'w') as f:
            json.dump(card_list, f)

    except ValueError as e:
        print(f"Error: {e}")

    restart_program()
    
def load_json_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error: Unable to load JSON from file {file_path}. {e}")
        return None
    
file_path_shop = os.path.join('.', 'machine', 'dict', 'shop.json')
file_path_cathegories = os.path.join('.', 'machine', 'dict', 'cathegories.json')
file_path_brand = os.path.join('.', 'machine', 'dict', 'brand.json')
file_path_card_numbers = os.path.join('.', 'machine', 'dict', 'card_numbers.json')

shop = load_json_file(file_path_shop)
cathegories = load_json_file(file_path_cathegories)
brand = load_json_file(file_path_brand)
card_numbers = load_json_file(file_path_card_numbers)

def generate_entry(card_numbers, card_usage_counts, shop, cathegories, brand):
    random_shop_index = random.choice(list(shop.keys()))
    shop_info = shop[str(random_shop_index)]
    name_of_shop, coordinates, work_start_time, work_end_time = shop_info

    # Date
    start_date = date(2020, 1, 22)
    end_date = date(2023, 11, 5)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    # Time
    work_start_hour, work_start_minute = map(int, work_start_time.split(':'))
    work_end_hour, work_end_minute = map(int, work_end_time.split(':'))

    random_hour = random.randint(work_start_hour, work_end_hour)
    random_minute = random.randint(
        work_start_minute if random_hour == work_start_hour else 0,
        work_end_minute if random_hour == work_end_hour else 59
    )
    random_time = f"{random_hour:02d}:{random_minute:02d}"
    # Place
    place = coordinates
    cathegory_of_item = random.choice(cathegories)
    item_brand = random.choice(brand)
    # Card Numbers
    max_attempts = min(len(card_numbers), 10)  # Ensure max_attempts is not greater than the available card numbers
    selected_cards = random.sample(card_numbers, max_attempts)

    for card_number in selected_cards:
        if card_usage_counts[card_number] < 5:
            card_usage_counts[card_number] += 1
            break
    else:
        raise ValueError("Unable to find a suitable card number.")

    number_of_items = random.randint(1, 5)
    price = 100 * (random.randint(10, 1000))

    return [
        name_of_shop,
        random_date,
        random_time,
        place,
        cathegory_of_item,
        item_brand,
        card_number,
        number_of_items,
        price
    ]

def generate_data():
    start_time = time.time()

    number_of_purchases = int(entry2.get())

    if len(card_numbers) * 5 < number_of_purchases:
        messagebox.showerror("Ошибка", "Недостаточно уникальных карт. Увеличьте количество уникальных карт в файле card_numbers.json.")
        return

    card_usage_counts = {card_number: 0 for card_number in card_numbers}

    # Set the number of worker threads based on the number of physical cores
    num_physical_cores = psutil.cpu_count(logical=False)
    num_threads = min(num_physical_cores, 4)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(
            generate_entry,
            [card_numbers] * number_of_purchases,
            [card_usage_counts.copy()] * number_of_purchases,
            [shop] * number_of_purchases,
            [cathegories] * number_of_purchases,
            [brand] * number_of_purchases
        ))

        json_data = []

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for data_entry in results:
            sheet.append(data_entry)
            json_data.append({
                "name_of_shop": data_entry[0],
                "date": data_entry[1].strftime("%Y-%m-%d"),
                "time": data_entry[2],
                "place": data_entry[3],
                "cathegory_of_item": data_entry[4],
                "item_brand": data_entry[5],
                "card_number": data_entry[6],
                "number_of_items": data_entry[7],
                "price": data_entry[8]
            })

        # Close the workbook before writing to JSON
        workbook.close()
        # Save data to JSON
        time_now = datetime.now()
        time_now = str(time_now)
        time_now = time_now[:time_now.rfind(".")]
        time_now = time_now.replace(":", "-")
        json_output_path = f'./machine/result/{time_now}.json'
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    end_time = time.time()
    execution_time = end_time - start_time
    time_label.config(text=f"Время выполнения: {execution_time:.2f} секунд")

# GUI
app = tk.Tk()
app.title("Генератор данных")

label1 = tk.Label(app, text="Какое количество карт для генерации?")
label1.pack()

entry1 = tk.Entry(app)
entry1.pack()

generate_button1 = tk.Button(app, text="Сгенерировать карты", command=lambda: generate_and_save_cards(int(entry1.get())))
generate_button1.pack()

label2 = tk.Label(app, text="Какой размер финального списка?")
label2.pack()

entry2 = tk.Entry(app)
entry2.pack()

generate_button2 = tk.Button(app, text="Сгенерировать данные", command=generate_data)
generate_button2.pack()

time_label = tk.Label(app, text="Время выполнения: ")
time_label.pack()

app.mainloop()