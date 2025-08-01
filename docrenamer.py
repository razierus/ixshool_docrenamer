#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iXshool DocRenamer - Приложение для переименования файлов
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import sys

class FileRenameRow:
    """Класс для представления одной строки переименования файла"""
    
    def __init__(self, parent_frame, row_number, on_file_select_callback):
        self.parent_frame = parent_frame
        self.row_number = row_number
        self.on_file_select_callback = on_file_select_callback
        self.file_path = None
        self.original_filename = ""
        self.is_renamed = False
        
        # Создаем фрейм для этой строки
        self.frame = ttk.Frame(parent_frame, relief='raised', borderwidth=1)
        self.frame.grid(row=row_number, column=0, sticky='ew', padx=5, pady=2)
        
        # Настраиваем расширение колонок
        for i in range(7):
            self.frame.columnconfigure(i, weight=1)
        
        # Создаем элементы управления
        self.create_widgets()
        
    def create_widgets(self):
        """Создание элементов управления в строке"""
        
        # Кнопка выбора файла
        self.file_button = ttk.Button(
            self.frame, 
            text="Выбрать файл", 
            command=self.select_file,
            width=15
        )
        self.file_button.grid(row=0, column=0, padx=2, pady=5, sticky='ew')
        
        # 1. Неизменяемое поле "рабочая_программа"
        self.field1 = ttk.Entry(self.frame, state='readonly')
        self.field1.insert(0, "рабочая_программа")
        self.field1.grid(row=0, column=1, padx=2, pady=5, sticky='ew')
        
        # 2. Название предмета
        self.field2 = ttk.Entry(self.frame)
        self.field2.insert(0, "")
        self.field2.bind('<FocusIn>', lambda e: self.clear_placeholder(self.field2, "название предмета"))
        self.field2.bind('<FocusOut>', lambda e: self.set_placeholder(self.field2, "название предмета"))
        self.set_placeholder(self.field2, "название предмета")
        self.field2.grid(row=0, column=2, padx=2, pady=5, sticky='ew')
        
        # 3. Класс/параллель (максимум 4 символа)
        self.field3 = ttk.Entry(self.frame)
        self.field3.insert(0, "")
        self.field3.bind('<FocusIn>', lambda e: self.clear_placeholder(self.field3, "класс/параллель"))
        self.field3.bind('<FocusOut>', lambda e: self.set_placeholder(self.field3, "класс/параллель"))
        self.field3.bind('<KeyRelease>', lambda e: self.limit_length(self.field3, 4))
        self.set_placeholder(self.field3, "класс/параллель")
        self.field3.grid(row=0, column=3, padx=2, pady=5, sticky='ew')
        
        # 4. Автор
        self.field4 = ttk.Entry(self.frame)
        self.field4.insert(0, "")
        self.field4.bind('<FocusIn>', lambda e: self.clear_placeholder(self.field4, "автор"))
        self.field4.bind('<FocusOut>', lambda e: self.set_placeholder(self.field4, "автор"))
        self.set_placeholder(self.field4, "автор")
        self.field4.grid(row=0, column=4, padx=2, pady=5, sticky='ew')
        
        # 5. Неизменяемое поле "гбоу_сш_№9_мариуполь"
        self.field5 = ttk.Entry(self.frame, state='readonly')
        self.field5.insert(0, "гбоу_сш_№9_мариуполь")
        self.field5.grid(row=0, column=5, padx=2, pady=5, sticky='ew')
        
        # 6. Год (по умолчанию текущий год)
        self.field6 = ttk.Entry(self.frame)
        current_year = str(datetime.now().year)
        self.field6.insert(0, current_year)
        self.field6.bind('<FocusIn>', lambda e: self.clear_placeholder(self.field6, "год"))
        self.field6.bind('<FocusOut>', lambda e: self.set_placeholder(self.field6, "год"))
        self.field6.grid(row=0, column=6, padx=2, pady=5, sticky='ew')
        
        # Метка для отображения выбранного файла
        self.file_label = ttk.Label(self.frame, text="Файл не выбран", foreground='gray')
        self.file_label.grid(row=1, column=0, columnspan=7, padx=2, pady=2, sticky='w')
        
        # Метка для предварительного просмотра имени файла
        self.preview_label = ttk.Label(self.frame, text="", foreground='blue', font=('Arial', 9, 'italic'))
        self.preview_label.grid(row=2, column=0, columnspan=7, padx=2, pady=2, sticky='w')
        
        # Привязываем обновление предварительного просмотра к изменениям в полях
        self.field2.bind('<KeyRelease>', lambda e: self.update_preview())
        self.field3.bind('<KeyRelease>', lambda e: self.update_preview())
        self.field4.bind('<KeyRelease>', lambda e: self.update_preview())
        self.field6.bind('<KeyRelease>', lambda e: self.update_preview())
        self.field2.bind('<FocusOut>', lambda e: [self.set_placeholder(self.field2, "название предмета"), self.update_preview()])
        self.field3.bind('<FocusOut>', lambda e: [self.set_placeholder(self.field3, "класс/параллель"), self.update_preview()])
        self.field4.bind('<FocusOut>', lambda e: [self.set_placeholder(self.field4, "автор"), self.update_preview()])
        self.field6.bind('<FocusOut>', lambda e: [self.set_placeholder(self.field6, "год"), self.update_preview()])
        
    def select_file(self):
        """Выбор файла для переименования"""
        file_types = [
            ('Все поддерживаемые файлы', '*.pdf *.doc *.docx *.xls *.xlsx *.ppt *.pptx'),
            ('PDF файлы', '*.pdf'),
            ('Word документы', '*.doc *.docx'),
            ('Excel таблицы', '*.xls *.xlsx'),
            ('PowerPoint презентации', '*.ppt *.pptx'),
            ('Все файлы', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(
            title=f"Выберите файл для переименования (строка {self.row_number + 1})",
            filetypes=file_types
        )
        
        if file_path:
            self.file_path = file_path
            self.original_filename = os.path.basename(file_path)
            self.file_label.config(text=f"Файл: {self.original_filename}", foreground='blue')
            self.file_button.config(text="Изменить файл")
            
            # Вызываем callback
            if self.on_file_select_callback:
                self.on_file_select_callback()
                
            # Обновляем предварительный просмотр
            self.update_preview()
    
    def clear_placeholder(self, entry, placeholder):
        """Очистка placeholder при фокусе"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')
    
    def set_placeholder(self, entry, placeholder):
        """Установка placeholder при потере фокуса"""
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground='gray')
    
    def limit_length(self, entry, max_length):
        """Ограничение длины текста в поле"""
        text = entry.get()
        if len(text) > max_length:
            entry.delete(max_length, tk.END)
            
    def update_preview(self):
        """Обновление предварительного просмотра имени файла"""
        if not self.file_path:
            self.preview_label.config(text="")
            return
            
        new_name = self.get_new_filename()
        if new_name:
            self.preview_label.config(
                text=f"Предварительный просмотр: {new_name}", 
                foreground='green'
            )
        else:
            self.preview_label.config(
                text="Необходимо заполнить хотя бы одно из полей: предмет, класс, автор", 
                foreground='red'
            )
    
    def get_new_filename(self):
        """Получение нового имени файла"""
        if not self.file_path:
            return None
            
        # Получаем значения полей
        field1_val = "рабочая_программа"
        field2_val = self.field2.get().strip()
        field3_val = self.field3.get().strip()
        field4_val = self.field4.get().strip()
        field5_val = "гбоу_сш_№9_мариуполь"
        field6_val = self.field6.get().strip()
        
        # Проверяем, что поля не содержат placeholder
        if field2_val == "название предмета":
            field2_val = ""
        if field3_val == "класс/параллель":
            field3_val = ""
        if field4_val == "автор":
            field4_val = ""
        if field6_val == "год":
            field6_val = str(datetime.now().year)
        
        # Заменяем пустые поля на placeholder
        if not field2_val:
            field2_val = "предмет"
        if not field3_val:
            field3_val = "класс"
        if not field4_val:
            field4_val = "автор"
        if not field6_val:
            field6_val = str(datetime.now().year)
            
        # Создаем новое имя файла - все поля всегда присутствуют
        parts = [field1_val, field2_val, field3_val, field4_val, field5_val, field6_val]
        
        # Проверяем, что хотя бы основные поля заполнены (не являются placeholder'ами)
        has_subject = field2_val and field2_val != "предмет"
        has_class = field3_val and field3_val != "класс"
        has_author = field4_val and field4_val != "автор"
        
        if not (has_subject or has_class or has_author):
            return None  # Хотя бы одно из основных полей должно быть заполнено
            
        # Получаем расширение оригинального файла
        _, ext = os.path.splitext(self.original_filename)
        
        # Создаем новое имя
        new_name = "_".join(parts) + ext
        
        # Убираем недопустимые символы для имени файла
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            new_name = new_name.replace(char, '_')
            
        return new_name
    
    def mark_as_renamed(self):
        """Отметить строку как переименованную"""
        self.is_renamed = True
        # Меняем цвет фона всех полей на зеленый
        style = ttk.Style()
        
        # Создаем новый стиль для переименованных полей
        style.configure('Renamed.TEntry', fieldbackground='lightgreen')
        
        self.field1.config(style='Renamed.TEntry')
        self.field2.config(style='Renamed.TEntry')
        self.field3.config(style='Renamed.TEntry')
        self.field4.config(style='Renamed.TEntry')
        self.field5.config(style='Renamed.TEntry')
        self.field6.config(style='Renamed.TEntry')
        
        self.file_label.config(text=f"✓ Переименован: {self.original_filename}", foreground='green')


class DocRenamerApp:
    """Главное приложение"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("iXshool DocRenamer")
        self.root.geometry("1200x600")
        
        # Список строк для переименования
        self.rename_rows = []
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Добавляем первую строку
        self.add_rename_row()
        
    def create_widgets(self):
        """Создание основного интерфейса"""
        
        # Главный фрейм с прокруткой
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Фрейм для прокрутки
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Настраиваем расширение колонки
        self.scrollable_frame.columnconfigure(0, weight=1)
        
        # Фрейм для кнопок
        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack(fill='x', padx=10, pady=5)
        
        # Кнопка добавления новой строки
        self.add_button = ttk.Button(
            self.buttons_frame,
            text="+ Добавить файл",
            command=self.add_rename_row
        )
        self.add_button.pack(side='left', padx=5)
        
        # Кнопка переименования
        self.rename_button = ttk.Button(
            self.buttons_frame,
            text="ПЕРЕИМЕНОВАТЬ",
            command=self.rename_files,
            style='Accent.TButton'
        )
        self.rename_button.pack(fill='x', expand=True, padx=5)
        
        # Настраиваем стиль для кнопки переименования
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 12, 'bold'))
        
        # Привязываем колесо мыши к прокрутке
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """Обработка прокрутки колесом мыши"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def add_rename_row(self):
        """Добавление новой строки для переименования"""
        row_number = len(self.rename_rows)
        new_row = FileRenameRow(
            self.scrollable_frame, 
            row_number, 
            self.on_file_selected
        )
        self.rename_rows.append(new_row)
        
        # Обновляем область прокрутки
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_file_selected(self):
        """Callback при выборе файла"""
        # Можно добавить дополнительную логику при выборе файла
        pass
        
    def get_output_directory(self):
        """Получение директории для сохранения переименованных файлов"""
        # Находим первый файл в списке для определения родительской директории
        first_file = None
        for row in self.rename_rows:
            if row.file_path:
                first_file = row.file_path
                break
                
        if first_file:
            parent_dir = os.path.dirname(first_file)
            default_output = os.path.join(parent_dir, "Переименованные_файлы")
        else:
            default_output = os.path.expanduser("~/Переименованные_файлы")
            
        # Спрашиваем пользователя о директории
        output_dir = filedialog.askdirectory(
            title="Выберите папку для сохранения переименованных файлов",
            initialdir=os.path.dirname(default_output)
        )
        
        if not output_dir:
            # Если пользователь отменил выбор, используем директорию по умолчанию
            output_dir = default_output
            
        return output_dir
        
    def rename_files(self):
        """Переименование всех файлов"""
        # Проверяем, что есть файлы для переименования
        files_to_rename = [row for row in self.rename_rows if row.file_path and not row.is_renamed]
        
        if not files_to_rename:
            messagebox.showwarning("Предупреждение", "Нет файлов для переименования!")
            return
            
        # Проверяем корректность новых имен
        invalid_rows = []
        for i, row in enumerate(files_to_rename):
            new_name = row.get_new_filename()
            if not new_name:
                invalid_rows.append(i + 1)
                
        if invalid_rows:
            messagebox.showerror(
                "Ошибка", 
                f"Не все поля заполнены корректно в строках: {', '.join(map(str, invalid_rows))}"
            )
            return
            
        # Получаем директорию для сохранения
        output_dir = self.get_output_directory()
        
        # Создаем директорию если её нет
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать директорию: {e}")
            return
            
        # Переименовываем файлы
        success_count = 0
        errors = []
        
        for row in files_to_rename:
            try:
                new_name = row.get_new_filename()
                if new_name:
                    new_path = os.path.join(output_dir, new_name)
                    
                    # Проверяем, что файл с таким именем не существует
                    counter = 1
                    base_name, ext = os.path.splitext(new_name)
                    while os.path.exists(new_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        new_path = os.path.join(output_dir, new_name)
                        counter += 1
                    
                    # Копируем файл с новым именем
                    shutil.copy2(row.file_path, new_path)
                    row.mark_as_renamed()
                    success_count += 1
                    
            except Exception as e:
                errors.append(f"{row.original_filename}: {e}")
                
        # Показываем результат
        if errors:
            error_msg = "\n".join(errors)
            messagebox.showerror(
                "Ошибки при переименовании", 
                f"Успешно переименовано: {success_count}\nОшибки:\n{error_msg}"
            )
        else:
            messagebox.showinfo(
                "Успех", 
                f"Успешно переименовано {success_count} файл(ов)\nФайлы сохранены в: {output_dir}"
            )
            
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


def main():
    """Главная функция"""
    try:
        app = DocRenamerApp()
        app.run()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
