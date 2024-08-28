from numba import jit

@jit(nopython=True)
def check_dividers(num):
    dividers = []
    for divider in range(1, num):
        if num % divider == 0:
            dividers.append(divider)
    if sum(dividers) == num:
        return True
    return False

@jit(nopython=True)
def perfect_num(total_num):
    perfect_nums = []
    
    for i in range(total_num):
        if check_dividers(i):
            perfect_nums.append(i)
    
    print(perfect_nums)

# Пример использования
perfect_num(10000)