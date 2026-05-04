import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Файл для хранения данных
DATA_FILE = 'expenses.json'

# Изначальные данные
expenses = []

# Загрузка данных из файла
def load_data():
    global expenses
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []

# Сохранение данных в файл
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

# Проверка корректности ввода
def validate_input():
    try:
        amount = float(entry_amount.get())
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Введите положительное число для суммы.")
        return False
    
    date_str = entry_date.get()
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
        return False
    
    if not combo_category.get():
        messagebox.showerror("Ошибка", "Выберите категорию.")
        return False
    return True

# Добавление расхода
def add_expense():
    if not validate_input():
        return
    expense = {
        "sum": float(entry_amount.get()),
        "category": combo_category.get(),
        "date": entry_date.get()
    }
    expenses.append(expense)
    refresh_table()
    clear_entries()

# Очистка полей ввода
def clear_entries():
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    combo_category.set('')

# Обновление таблицы
def refresh_table(filtered_expenses=None):
    for row in tree.get_children():
        tree.delete(row)
    display_expenses = filtered_expenses if filtered_expenses is not None else expenses
    for exp in display_expenses:
        tree.insert('', tk.END, values=(exp["sum"], exp["category"], exp["date"]))
    calculate_total()

# Фильтр по категориям и датам
def filter_expenses():
    category_filter = combo_filter_category.get()
    date_from = entry_filter_date_from.get()
    date_to = entry_filter_date_to.get()

    def in_range(exp):
        if category_filter != "Все" and exp["category"] != category_filter:
            return False
        try:
            date_obj = datetime.strptime(exp["date"], '%Y-%m-%d')
            if date_from:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                if date_obj < date_from_obj:
                    return False
            if date_to:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                if date_obj > date_to_obj:
                    return False
            return True
        except:
            return False

    filtered = [exp for exp in expenses if in_range(exp)]
    refresh_table(filtered)

# Подсчет суммы по текущему отображению
def calculate_total():
    total = 0
    for item in tree.get_children():
        val = float(tree.item(item, 'values')[0])
        total += val
    label_total.config(text=f"Общая сумма: {total:.2f}")

# Сохранение данных при закрытии
def on_closing():
    save_data()
    root.destroy()

# Основное окно
root = tk.Tk()
root.title("Expense Tracker")

load_data()

# Ввод данных для расхода
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

tk.Label(frame_input, text="Сумма").grid(row=0, column=0)
entry_amount = tk.Entry(frame_input)
entry_amount.grid(row=0, column=1)

tk.Label(frame_input, text="Категория").grid(row=1, column=0)
categories = ['Еда', 'Транспорт', 'Развлечения', 'Другое']
combo_category = ttk.Combobox(frame_input, values=categories)
combo_category.grid(row=1, column=1)

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД)").grid(row=2, column=0)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=2, column=1)
entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))

btn_add = tk.Button(frame_input, text="Добавить расход", command=add_expense)
btn_add.grid(row=3, column=0, columnspan=2, pady=5)

# Таблица расходов
columns = ('Сумма', 'Категория', 'Дата')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10)

refresh_table()

# Фильтр
frame_filter = tk.Frame(root)
frame_filter.pack(padx=10, pady=5)

tk.Label(frame_filter, text="Фильтр по категории").grid(row=0, column=0)
combo_filter_category = ttk.Combobox(frame_filter, values=["Все"] + categories)
combo_filter_category.current(0)
combo_filter_category.grid(row=0, column=1)

tk.Label(frame_filter, text="Дата с").grid(row=0, column=2)
entry_filter_date_from = tk.Entry(frame_filter)
entry_filter_date_from.grid(row=0, column=3)

tk.Label(frame_filter, text="по").grid(row=0, column=4)
entry_filter_date_to = tk.Entry(frame_filter)
entry_filter_date_to.grid(row=0, column=5)

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=filter_expenses)
btn_filter.grid(row=0, column=6, padx=5)

# Общая сумма
label_total = tk.Label(root, text="Общая сумма: 0.00")
label_total.pack()

# Обновлять сумму при фильтре
def update_filter():
    filter_expenses()

btn_filter.config(command=update_filter)

# Обработка закрытия
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()