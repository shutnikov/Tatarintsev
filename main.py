import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.entries = []
        self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0,a padx=5, pady=5)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(root, variable=self.rain_var).grid(row=3, column=1, sticky="w")

        # Кнопка добавления
        tk.Button(root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Rain"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Rain", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Фильтры
        tk.Label(root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по температуре (>):").grid(row=7, column=0, padx=5, pady=5)
        self.filter_temp_entry = tk.Entry(root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=10)

        # Кнопки сохранения/загрузки
        tk.Button(root, text="Сохранить в JSON", command=self.save_data).grid(row=9, column=0, pady=5)
        tk.Button(root, text="Загрузить из JSON", command=self.load_data).grid(row=9, column=1, pady=5)

    def add_entry(self):
        try:
            date = self.date_entry.get()
            datetime.strptime(date, "%Y-%m-%d")  # Проверка формата даты
            temp = float(self.temp_entry.get())
            desc = self.desc_entry.get().strip()
            if not desc:
                raise ValueError("Описание не может быть пустым")
            rain = self.rain_var.get()

            entry = {"date": date, "temp": temp, "desc": desc, "rain": rain}
            self.entries.append(entry)
            self.update_table()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set(False)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temp']}°C",
                entry["desc"],
                "Да" if entry["rain"] else "Нет"
            ))

    def save_data(self):
        with open("weather_data.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Успех", "Данные сохранены в weather_data.json")

    def load_data(self):
        if os.path.exists("weather_data.json"):
            with open("weather_data.json", "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            self.update_table()

    def apply_filters(self):
        filtered = self.entries
        date_filter = self.filter_date_entry.get()
        if date_filter:
            filtered = [e for e in filtered if e["date"] == date_filter]
        temp_filter = self.filter_temp_entry.get()
        if temp_filter:
            temp_filter = float(temp_filter)
            filtered = [e for e in filtered if e["temp"] > temp_filter]
        # Обновляем таблицу только отфильтрованными данными
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in filtered:
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temp']}°C",
                entry["desc"],
                "Да" if entry["rain"] else "Нет"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
