import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_poro_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Размер ячейки
    dx, dy = map(float, lines[0].split()[2:4])

    # Координаты сетки
    x1, x2, y1, y2 = map(float, lines[1].split())

    # Считываем значения пористости начиная с 5-й строки
    raw_values = []
    for line in lines[4:]:
        raw_values.extend(map(float, line.split()))
    
    total_cells = len(raw_values)

    # Вычисляем количество ячеек
    x_length = x2 - x1
    y_length = y2 - y1
    nx = int(round(x_length / dx) + 1)
    ny = int(round(y_length / dy) + 1)

    if nx * ny != total_cells:
        raise ValueError(f"Неверное количество значений: {total_cells}, не совпадает с {ny} * {nx} = {ny * nx}")

    # Центры ячеек
    x_coords = np.linspace(x1 + dx/2, x2 - dx/2, nx)
    y_coords = np.linspace(y1 + dy/2, y2 - dy/2, ny)

    # Массив пористости
    poro_array = np.array(raw_values).reshape(ny, nx)
    poro_array[poro_array == 9999900] = 0

    # Сетка координат
    xx, yy = np.meshgrid(x_coords, y_coords)

    # DataFrame
    df = pd.DataFrame({
        'X': xx.flatten(),
        'Y': yy.flatten(),
        'PORO': poro_array.flatten()
    })

    return df

def visualize_poro_map(df):
    plt.figure(figsize=(10, 8))
    plt.tricontourf(df['X'], df['Y'], df['PORO'], levels=100, cmap='jet')
    plt.colorbar(label='Пористость')
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.title('Карта пористости')
    # plt.gca().invert_yaxis()
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

# Пример использования
file_path = 'DATA/map_PORO_2D.txt'
df_poro = read_poro_map(file_path)
print(df_poro)
visualize_poro_map(df_poro)
