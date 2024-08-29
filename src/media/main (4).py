import pandas as pd  # импорт модуля pandas
import numpy as np  # импорт модуля numpy
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # для избежания ошибки SettingWithCopyWarning мы устанавливаем значение None

df = pd.read_csv('skater_stats.csv', low_memory=False)  # считываем файл, авт-ки разбивая данные на столбцы
year = int(input('Введите сезон(год): '))
df = df.loc[df['Season'] == year]  # сортируем чтобы остались строки, где нужный нам год

tab = df[['Player', 'Tm', 'G']]  # присваиваем tab столбцы с этими названиями
tab.G = pd.to_numeric(tab.G, errors='coerce')  # преобр-ем аргумент в числовой тип и "-" становится NaN
tab = tab.dropna()  # удаляем все строки с пропусками
tab.G = tab.G.astype(int)  # преобр-ем стобец G в int вместо float
tab = tab.sort_values(by='G', ascending=False)  # сортируем от большего к меньшему в столбце G
tab = tab.reset_index()  # переиндексация
tab = tab.drop('index', axis=1)  # удаляем столбец с заголовком index
tab = tab.set_index(np.arange(1, len(tab)+1))
# устанавливаем нашему DataFrame'у индекс с помощью set_index указав в параметрах созданный путем numpy.arange массив

print(tab)

# Загрузка данных
skater_stats = pd.read_csv('skater_stats.csv', low_memory=False)

# Преобразование колонок к числовым типам, где это необходимо
skater_stats['+/-'] = pd.to_numeric(skater_stats['+/-'], errors='coerce')


# Функция для построения гистограммы
def plot_plus_minus_histogram_by_year(skater_stats, year):
    # Фильтрация данных по указанному году
    yearly_data = skater_stats[skater_stats['Season'] == year]

    if yearly_data.empty:
        print(f"Нет данных за {year} год.")
        return

    # Найти лучших игроков по показателю +/- в каждой команде
    best_players = yearly_data.loc[yearly_data.groupby('Tm')['+/-'].idxmax()]

    # Проверка на пустую серию
    if best_players.empty:
        print(f"Нет игроков с данными по +/- за {year} год.")
        return

    # Построение гистограммы
    plt.figure(figsize=(12, 8))
    bins = np.arange(best_players['+/-'].min() - 1, best_players['+/-'].max() + 2) - 0.5
    plt.hist(best_players['+/-'].dropna(), bins=bins, edgecolor='black')
    plt.title(f'Гистограмма коэффициента полезности (+/-) лучших игроков каждой команды в {year} году')
    plt.xlabel('Коэффициент полезности (+/-)')
    plt.ylabel('Количество игроков')
    plt.grid(True)
    plt.show()


# Пример вызова функции
plot_plus_minus_histogram_by_year(skater_stats, year)
