from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type


class UnsupportedTypeTraining(Exception):
    """Исключение для неподдерживаемых типов тренировки."""
    pass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Не определен тип тренировки")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79
    MIN_IN_H: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    height — рост спортсмена"""

    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[int] = 100
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        height_in_meters = self.height / self.CM_IN_M
        speed_in_ms = self.get_mean_speed() * self.KMH_IN_MSEC
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (speed_in_ms ** 2 / height_in_meters)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание.
    length_pool - длина бассейна в метрах;
    count_pool - сколько раз пользователь переплыл бассейн;
    LEN_STEP - один гребок"""

    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[int] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость пловца в км/ч."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                 'RUN': Running,
                                                 'WLK': SportsWalking,
                                                 }
    if workout_type not in training_types.keys():
        raise NotImplementedError("Не определен тип тренировки")
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
