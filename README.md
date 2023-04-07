# avito-parser #
Парсер обьявлений с сайта avito.ru
---
Данный скрипт парсит объявления из всех регионов, с применением следующих фильтров:
1.	Ключевые слова, хотя бы одно из которых должно встречаться в названии объявления
2.	Негативные подсказки, которых не должно быть в названии объявления 
3.	Поиск товаров с включенной доставкой
4.	Категория
5.	Ценовой диапазон
---
После парсинга объявления зансятся в Excel таблицу в соответсвующие столбцы

Парсер написан на библиотеке Selenium, с применением pandas для создания Excel файла


