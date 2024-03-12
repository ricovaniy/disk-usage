import os
import sys
from datetime import datetime
from tqdm import tqdm


class DiskAnalyser:

    def __init__(self, max_size=None, min_size=None, extension=None, date=None, nested_level=None):
        self.conditions = [lambda file_path: not max_size or os.path.getsize(file_path) <= max_size,
                           lambda file_path: not min_size or os.path.getsize(file_path) >= min_size,
                           lambda file_path: not extension or file_path.endswith(extension),
                           lambda file_path: not date or
                                             date.date() == datetime.fromtimestamp(os.path.getctime(file_path)).date(),
                           lambda file_path: not nested_level or self.calc_nested_level(file_path) == nested_level]

    @staticmethod
    def calc_nested_level(path):
        path = os.path.normpath(path)
        return len(path.split(os.sep)) - 1

    def check_file(self, file_path):
        return all(condition(file_path) for condition in self.conditions if condition is not None)

    @staticmethod
    def count_files(directory):
        size = 0
        files_list = []
        for root, dirs, files in tqdm(os.walk(directory), desc = f"Считаю файлы в {directory}", file = sys.stdout):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size += os.path.getsize(file_path)
                    files_list.append(file_path)
                except FileNotFoundError:
                    continue
        return size, files_list

    def calc_with_filters(self, directory):
        size = 0
        files = self.count_files(directory)[1]
        for file in tqdm(files, desc = "Считаю размер с фильтрами", file = sys.stdout):
            if self.check_file(file):
                size += os.path.getsize(file)
        return size


def main():
    while True:
        disk_path = input("Введите путь до файла: ")
        max_size = input("Введите максимальный размер файлов, которые надо считать (оставьте пустым, если не хотите): ")
        if max_size and (not max_size.isdigit() or int(max_size) <= 0):
            print("Вводите данные корректно")
            continue
        min_size = input("Введите минимальный размер файлов, которые надо считать (оставьте пустым, если не хотите): ")
        if min_size and (not min_size.isdigit() or int(min_size) <= 0):
            print("Вводите данные корректно")
            continue
        extension = input("Введите расширение файлов, которые надо считать (только 1 расширение, с точкой в начале, "
                          "оставьте пустым, если не хотите): ")
        if not extension.startswith('.') and extension:
            print("Вводите данные корректно")
            continue

        date = input("Введите дату создания файла в формате ДД-ММ-ГГГГ (оставьте пустым, если не хотите): ")
        try:
            if date:
                date = datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            print("Вводите данные корректно")
            continue

        nested_level = input("Введите уровень вложенности (оставьте пустым, если не хотите): ")
        if (not nested_level.isdigit() or int(nested_level) <= 0) and nested_level:
            print("Вводите данные корректно")
            continue
        break

    analyser = DiskAnalyser(int(max_size) if max_size else None, int(min_size) if min_size else None, extension, date,
                            int(nested_level) if nested_level else None)
    size = analyser.calc_with_filters(disk_path)
    print(f"Size of all files in directory = {size} bytes")


if __name__ == "__main__":
    main()
