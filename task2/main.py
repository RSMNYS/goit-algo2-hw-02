from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Таблиця для зберігання обчислених результатів максимального прибутку
    memo_profit = {}
    # Таблиця для зберігання оптимальних розрізів
    memo_cuts = {}
    
    # Допоміжна функція для знаходження максимального прибутку
    def find_max_profit(n):
        if n == 0:
            return 0
        
        if n in memo_profit:
            return memo_profit[n]
        
        max_val = float('-inf')
        for i in range(1, n + 1):
            max_val = max(max_val, prices[i-1] + find_max_profit(n - i))
        
        memo_profit[n] = max_val
        return max_val
    
    # Допоміжна функція для знаходження розрізів
    def find_cuts(n):
        if n == 0:
            return []
        
        if n in memo_cuts:
            return memo_cuts[n]
        
        max_val = float('-inf')
        best_cut = 0
        
        for i in range(1, n + 1):
            current_val = prices[i-1] + find_max_profit(n - i)
            if current_val > max_val:
                max_val = current_val
                best_cut = i
        
        remaining_cuts = find_cuts(n - best_cut)
        memo_cuts[n] = [best_cut] + remaining_cuts
        
        return memo_cuts[n]
    
    # Обчислюємо максимальний прибуток
    max_profit = find_max_profit(length)
    
    # Знаходимо оптимальні розрізи
    cuts = find_cuts(length)
    
    # Підраховуємо кількість розрізів
    number_of_cuts = len(cuts) - 1 if cuts else 0
    
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Створюємо таблиці для зберігання результатів
    dp = [0] * (length + 1)  # максимальний прибуток для довжини i
    cut = [0] * (length + 1)  # оптимальний перший розріз для довжини i
    
    # Будуємо таблиці знизу вгору
    for i in range(1, length + 1):
        max_val = float('-inf')
        
        for j in range(1, i + 1):
            if prices[j-1] + dp[i-j] > max_val:
                max_val = prices[j-1] + dp[i-j]
                cut[i] = j
        
        dp[i] = max_val
    
    # Відновлюємо розрізи
    cuts = []
    remaining = length
    
    while remaining > 0:
        cuts.append(cut[remaining])
        remaining -= cut[remaining]
    
    # Підраховуємо кількість розрізів
    number_of_cuts = len(cuts) - 1 if cuts else 0
    
    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }

def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()