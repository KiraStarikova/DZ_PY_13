# Возьмите 1-3 задачи из тех, что были на прошлых семинарах или в домашних заданиях.
# Напишите к ним классы исключения с выводом подробной информации.
# Поднимайте исключения внутри основного кода.


import csv
from functools import reduce
from pathlib import Path
from apply_exceptions import *


class Validate:

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def __delete__(self, instance):
        raise AttributeError(f'Свойство "{self.param_name}" нельзя удалять')

    def validate(self, value):
        if not isinstance(value, str):
            raise StrException(value)
        if not value.isalpha() or not value.istitle():
            raise TextException(value)


class Student:
    name = Validate()
    second_name = Validate()
    surname = Validate()
    _lessons = None

    def __init__(self, name: str, second_name: str, surname: str, lessons: Path):
        self.name = name
        self.second_name = second_name
        self.surname = surname
        self.lessons = lessons

    @property
    def lessons(self):
        return self._lessons

    @lessons.setter
    def lessons(self, less: Path):
        if self.lessons is not None:
            raise AttributeError(f'Список предметов уже определён')
        self._lessons = {"lessons": {}}
        with open(less, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self._lessons["lessons"][row[0]] = {"estimates": [],
                                                    "tests": [],
                                                    "middle_estimate_test": None}
        self._lessons["middle_estimate"] = None

    def new_estimate(self, name_of_lesson: str, number: int, type_est: str = "less"):
        if name_of_lesson not in self.lessons["lessons"].keys():
            raise LessonsException(name_of_lesson)
        if type_est == "less":
            if number < 2 or number > 5:
                raise EstimateException(number, 2, 5)
            self.lessons["lessons"][name_of_lesson]["estimates"].append(number)
            self.lessons["middle_estimate"] = self.middle_estimate(self.lessons)
        elif type_est == "test":
            if number < 0 or number > 100:
                raise EstimateException(number, 0, 100)
            self.lessons["lessons"][name_of_lesson]["tests"].append(number)
            self.lessons["lessons"][name_of_lesson]["middle_estimate_test"] = \
                reduce(lambda x, y: x + y, self.lessons["lessons"][name_of_lesson]["tests"]) / \
                len(self.lessons["lessons"][name_of_lesson]["tests"])

    @staticmethod
    def middle_estimate(lessons: dict):
        all_estimates = []
        [all_estimates.extend(lessons["lessons"][name]["estimates"]) for name in lessons["lessons"]]
        return reduce(lambda x, y: x + y, all_estimates) / len(all_estimates)

    def __repr__(self):
        result = f'''Средние баллы студента: 
        полное имя = "{self.name} {self.second_name} {self.surname}",
        средний балл = {self.lessons["middle_estimate"]}\n'''
        for key, value in self.lessons["lessons"].items():
            result += f' средний балл по тестам {key} =  {value["middle_estimate_test"]}\n'

        return result


if __name__ == '__main__':
    info = Student("Ivan", "Ivanovich", "Ivanov", Path('lessons.csv'))
    info.new_estimate("русский язык", 3)
    info.new_estimate("русский язык", 5)
    info.new_estimate("математика", 4)
    info.new_estimate("информатика", 4)
    info.new_estimate("математика", 5)
    info.new_estimate("русский язык", 5)
    info.new_estimate("информатика", 3)
    info.new_estimate("математика", 5)
    info.new_estimate("русский язык", 3)
    info.new_estimate("математика", 4)
    info.new_estimate("математика", 68, "test")
    info.new_estimate("математика", 99, "test")
    info.new_estimate("русский язык", 29, "test")
    info.new_estimate("русский язык", 100, "test")
    info.new_estimate("русский язык", 18, "test")
    info.new_estimate("информатика", 74, "test")
    info.new_estimate("информатика", 39, "test")

    print(info)
