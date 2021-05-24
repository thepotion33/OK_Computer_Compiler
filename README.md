# OK_Computer_Compiler
Курсовая работа студента группы ИБ-118 Сидельникова Фёдора
## Запуск
При запуске mips_generator.py происходит поиск в директории файла программы example.ok и по итогу работы генерирует файл с инструкциями для Mips MIPS.s
## Библиотеки:
ply - для лексера и парсера
re - для регулярных выражений
## Пример кода:
```
/* fibonacci numbers example */

variables
i, a, b, n, c, t --> int

{
    i -> 1;
    t -> 8;
    b -> 1;
    c -> 1;

    while(i < t)
    {
        i -> i + 1;
        a -> c;
        c -> b;
        b -> a + b;
        write(a);
        write("\n")
    }
}

```
## Output:
1  
1  
2  
3  
5  
8  
13  
## Видео:
https://disk.yandex.ru/i/1IfgLQmH2AND5g
