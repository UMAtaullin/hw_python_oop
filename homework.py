class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str(),
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = self.get_distance() / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        self.message = InfoMessage
        self.info = InfoMessage(self.__class__.__name__,
                                self.duration,
                                self.get_distance(),
                                self.get_mean_speed(),
                                self.get_spent_calories()
                                )
        return self.info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        """Получить дистанцию бегуна в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость бега в км/ч."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных при беге в ккал."""
        MIN = self.duration * self.MIN_IN_H
        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                         / self.M_IN_KM * MIN)
        return self.calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    height — рост спортсмена"""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        """Получить дистанцию при ходьбе в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость ходьбы в км/ч."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе в ккал."""
        MIN = self.duration * self.MIN_IN_H
        height_in_meters = self.height / self.CM_IN_M

        speed_in_ms = self.get_mean_speed() * self.KMH_IN_MSEC
        self.calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + (speed_in_ms ** 2 / height_in_meters)
                         * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                         * MIN)
        return self.calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание.
    length_pool - длина бассейна в метрах;
    count_pool - сколько раз пользователь переплыл бассейн;
    LEN_STEP - один гребок"""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию плавца в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость пловца в км/ч."""
        self.mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                           / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании в ккал."""
        self.calories = ((self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         * self.duration)
        return self.calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: list[tuple[str, list[int]]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking,
                                                   }
    training: Training = training_types[workout_type](*data)
    return training


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
