def output(num: int) -> None:
    result: str = ''
    for i in range(num+1):
        result += i*str(i)
    print(result)


print('Введите число')
output(int(input()))
