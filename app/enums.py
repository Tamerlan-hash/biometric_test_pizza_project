from enum import Enum


class Thickness(str, Enum):
    MEDIUM = "MEDIUM"   # Средняя толщина
    THIN = "THIN"       # Тонкая толщина
    THICK = "THICK"     # Толстая толщина


class Cheese(str, Enum):
    PARMEZAN = "PARMEZAN"
    MOZZARELLA = "MOZZARELLA"
