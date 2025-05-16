from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Конвертуємо вхідні дані у об'єкти dataclass
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)
    
    # Сортуємо завдання за пріоритетом (1 - найвищий, 3 - найнижчий)
    jobs.sort(key=lambda x: x.priority)
    
    # Створюємо групи (батчі) для одночасного друку з урахуванням обмежень
    batches = []
    current_batch = []
    current_volume = 0
    
    for job in jobs:
        # Якщо додавання цього завдання перевищує обмеження, починаємо новий батч
        if (len(current_batch) >= printer.max_items or 
            current_volume + job.volume > printer.max_volume):
            if current_batch:  # Додаємо тільки непорожні батчі
                batches.append(current_batch)
            current_batch = [job]
            current_volume = job.volume
        else:
            current_batch.append(job)
            current_volume += job.volume
    
    # Додаємо останній батч, якщо він не порожній
    if current_batch:
        batches.append(current_batch)
    
    # Розраховуємо порядок друку та загальний час
    print_order = []
    total_time = 0
    
    for batch in batches:
        for job in batch:
            print_order.append(job.id)
        
        # Час друку для батчу - це максимальний час серед усіх моделей у батчі
        batch_time = max(job.print_time for job in batch)
        total_time += batch_time
    
    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()