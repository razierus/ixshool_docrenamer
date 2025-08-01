#!/bin/bash

# Скрипт для сборки DocRenamer с поддержкой tkinter

echo "Добавляем PyInstaller в PATH..."
export PATH=$PATH:/home/alxndrnklvch/.local/bin

echo "Сборка версии с папкой (быстрый запуск)..."
pyinstaller --noconfirm DocRenamer.spec

echo "Сборка единого исполняемого файла (медленный запуск, но удобнее распространять)..."
# Переименовываем папочную версию временно
if [ -d "dist/DocRenamer" ]; then
    mv dist/DocRenamer dist/DocRenamer_folder
fi
pyinstaller --noconfirm DocRenamer_onefile.spec
# Переименовываем единый файл и возвращаем папочную версию
if [ -f "dist/DocRenamer" ]; then
    mv dist/DocRenamer dist/DocRenamer_single
fi
if [ -d "dist/DocRenamer_folder" ]; then
    mv dist/DocRenamer_folder dist/DocRenamer
fi

echo "Готово!"
echo "Версия с папкой: dist/DocRenamer/"
echo "Единый файл: dist/DocRenamer_single"

# Показываем размеры файлов
echo ""
echo "Размеры файлов:"
ls -lh dist/DocRenamer/DocRenamer 2>/dev/null && echo "^ Папочная версия (исполняемый файл)" || echo "Папочная версия не найдена"
ls -lh dist/DocRenamer_single 2>/dev/null && echo "^ Единый исполняемый файл" || echo "Единый файл не найден"
