### что нужно сделать:
- прописать саму змейку (основная идея: змейка состоит из отдельных квадратиков, когда она съедает фрукт добавляется ещё один квадратик;
каждый квадратик - объект класса body_parts, они все хранятся в массиве snake;
первый квадратик каждый кадр сдвигается на вектор скорости v, а остальным надо как-то придумать
полезная ссылка https://proglib.io/p/samouchitel-po-python-dlya-nachinayushchih-chast-21-osnovy-razrabotki-igr-na-pygame-2023-05-29 (но гуглить наверно все умеют)
- прописать фрукты (спавн и взаимодействие с ними)
- прописать препятствия (для каждого уровня сложности свою расстановку, на первом можно не делать)
- прописать условие смерти (столкновение с препятствием, стеной или с собой должно вызвать pygame.quit() game_over() return 0)
- добавить таблицу лидеров и её обновление (основная идея: хранить в отдельном json файле словарь имя:рекорд, и это будет оставаться даже когда программу закрывают;
функция show_leaderboard() выводит окошко со списком (больше ничего не требуется, только чтобы можно было закрыть) (я не знаю какой библиотекой его лучше всего сделать, но вроде на pygame можно),
функция save_highscore() обновляет файл на компьютере, добавляя туда последний рекорд (по имени в переменной username и очкам в переменной score)  
*_этот пункт в принципе наверно можно не делать, но для него уже всё подготовлено, и без этого в проекте на троих будет маловато работы_*



 ### что было бы прикольно сделать:
- чтобы счет всегда выводился в углу (для етого нужно будет сделать чтобы окно было больше чем границы поля, чтобы счет не закрывал змейку)
- двигающиеся препятствия
- дождь (капельки просто мешают обзору)
- пасхалку если игрок вводит определённый юзернейм (но я не придумала какую)
- чтобы новые уровни открывались только если наберёшь определённое количество очков
- сделать глаза
- сделать музыку