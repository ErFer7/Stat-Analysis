# -*- coding: utf-8 -*-

'''
Análise estatística.
'''

from audioop import mul
import csv
import json

from math import log10, ceil, sqrt
from statistics import median, mode, variance, stdev, NormalDist

import plotly.graph_objects as go


def csv2json(input_file_path: str, output_file_path: str):
    '''
    Gera um arquivo .json a partir de um arquivo csv.
    '''

    processed_dict = {}

    with open(input_file_path, mode='r', encoding="utf-8") as csv_file:

        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            processed_dict[row[0]] = row[1:]

    with open(output_file_path, 'w+', encoding="utf-8") as file:

        data_json = json.dumps(processed_dict, indent=4)
        file.write(data_json)


def process_data(input_file_path: str, *output_files_path: str):
    '''
    Processa todos os dados e gera arquivos com os dados agrupados.
    '''

    data = {}

    with open(input_file_path, 'r', encoding="utf-8") as json_file:

        data = json.load(json_file)

    total_values = []
    sc_values = []
    rs_values = []
    nac_values = []
    outr_values = []
    metro_values = []
    int_values = []

    for key in data:

        value = float(data[key][4].replace(',', '.'))

        total_values.append(value)

        if data[key][1] == "SC":
            sc_values.append(value)
        else:
            rs_values.append(value)

        if data[key][3] == "NAC":
            nac_values.append(value)
        else:
            outr_values.append(value)

        if data[key][5] == "METRO":
            metro_values.append(value)
        else:
            int_values.append(value)

    for i in range(7):

        with open(output_files_path[i], 'w+', encoding="utf-8") as file:

            match i:

                case 0:

                    for value in total_values:
                        file.write(str(value) + '\n')
                case 1:

                    for value in sc_values:
                        file.write(str(value) + '\n')
                case 2:

                    for value in rs_values:
                        file.write(str(value) + '\n')
                case 3:

                    for value in nac_values:
                        file.write(str(value) + '\n')
                case 4:

                    for value in outr_values:
                        file.write(str(value) + '\n')
                case 5:

                    for value in metro_values:
                        file.write(str(value) + '\n')
                case 6:

                    for value in int_values:
                        file.write(str(value) + '\n')


def stem_and_leaves(total_data: list,
                    data_left: list,
                    data_right: list,
                    header_left: str,
                    header_right: str,
                    output_file_path: str):
    '''
    Cria um diagram de ramos e folhas comparativo.
    '''

    center_column_left = {}
    center_column_right = {}

    total_data.sort()
    data_left.sort()
    data_right.sort()

    for value in total_data:

        val_stem_key = f"{value:.3f}"[:3]

        if val_stem_key not in center_column_left:
            center_column_left[val_stem_key] = {}

        if val_stem_key not in center_column_right:
            center_column_right[val_stem_key] = {}

    for value in data_left:

        val_stem_key = f"{value:.3f}"[:3]
        val_leaf_key = f"{value:.3f}"[3:]

        if val_leaf_key in center_column_left[val_stem_key]:
            center_column_left[val_stem_key][val_leaf_key] += 1
        else:
            center_column_left[val_stem_key][val_leaf_key] = 1

    for value in data_right:

        val_stem_key = f"{value:.3f}"[:3]
        val_leaf_key = f"{value:.3f}"[3:]

        if val_leaf_key in center_column_right[val_stem_key]:
            center_column_right[val_stem_key][val_leaf_key] += 1
        else:
            center_column_right[val_stem_key][val_leaf_key] = 1

    stem = list(center_column_left.keys())

    min_key = float(stem[0])
    max_key = float(stem[-1])
    current_key = min_key
    i = 0

    while current_key < max_key:

        str_key = f"{current_key:.1f}"

        if str_key not in stem:
            stem.insert(i, str_key)

        i += 1
        current_key += 0.1

    left_leaves = []
    right_leaves = []
    left_frequency = []
    right_frequency = []

    for i, key in enumerate(stem):
        left_leaves.append([])
        right_leaves.append([])

        left_sum = 0

        if key in center_column_left:

            for leaf in center_column_left[key]:
                left_sum += center_column_left[key][leaf]
                left_leaves[i].append((leaf, center_column_left[key][leaf]))

        right_sum = 0

        if key in center_column_right:

            for leaf in center_column_right[key]:
                right_sum += center_column_right[key][leaf]
                right_leaves[i].append((leaf, center_column_right[key][leaf]))

        left_frequency.append(left_sum)
        right_frequency.append(right_sum)
        left_leaves[i] = sorted(left_leaves[i], key=lambda val: float(val[0]), reverse=True)
        right_leaves[i] = sorted(right_leaves[i], key=lambda val: float(val[0]))

    for i, branch in enumerate(left_leaves):

        str_branch = ''

        for leaf in branch:
            str_branch += f"({leaf[0]}/{leaf[1]}) "

        left_leaves[i] = str_branch

    for i, branch in enumerate(right_leaves):

        str_branch = ''

        for leaf in branch:
            str_branch += f"({leaf[0]}/{leaf[1]}) "

        right_leaves[i] = str_branch

    with open(output_file_path, 'w+', encoding="utf-8") as file:

        file.write(f"Freq:Folhas ({header_left}):Ramos:Folhas ({header_right}):Freq\n")

        for i, branch in enumerate(stem):
            file.write(f"{left_frequency[i]}:{left_leaves[i]}:{branch}:{right_leaves[i]}:{right_frequency[i]}\n")


def generate_classes(data: list):
    '''
    Gera classes de um modelo empírico.
    '''

    range_ = max(data) - min(data)
    k = 1 + 3.32 * log10(len(data))
    class_amp = range_ / k

    print("Geração de classes.")
    print(f"Mínimo: {min(data):.3f}")
    print(f"Máximo: {max(data):.3f}")
    print(f"Range: {range_:.3f}")
    print(f"k: {k:.3f} ou {ceil(k)}")
    print(f"Amplitude: {class_amp:.3f}")

    k = ceil(k)

    classes = []

    for i in range(k):
        classes.append((min(data) + class_amp * i, min(data) + class_amp * (i + 1)))

    return classes


def frequency_count(classes: list, data: list):
    '''
    Gera uma lista com a contagem pelas classes.
    '''

    frequency = [0 for _ in range(len(classes))]

    for value in data:

        for i, class_ in enumerate(classes):

            if class_[1] > value >= class_[0]:
                frequency[i] += 1

    return frequency


def empirical_model(data: list, output_file_path: str):
    '''
    Gera uma tabela do modelo empírico.
    '''

    classes = generate_classes(data)
    frequency = frequency_count(classes, data)
    proportion = []
    acc_proportion = []
    middle_point = []
    weighted_average = []
    variance_ = []

    for freq in frequency:
        proportion.append(freq / len(data))

    acc_prop = 0.0

    for prop in proportion:

        acc_proportion.append(prop + acc_prop)
        acc_prop += prop

    for i, class_ in enumerate(classes):

        middle_point.append((class_[0] + class_[1]) / 2)
        weighted_average.append(proportion[i] * middle_point[i])

    weighted_average_sum = sum(weighted_average)

    for i, class_ in enumerate(classes):
        variance_.append(((middle_point[i] - weighted_average_sum) ** 2) * proportion[i])

    median_ = median(data)
    mode_ = middle_point[frequency.index(max(frequency))]
    variance_sum = sum(variance_)
    std_deviation = sqrt(variance_sum)
    std_avg_error = std_deviation / sqrt(len(data))
    variation_coeff = std_deviation / weighted_average_sum
    median_assimetry = 3 * (weighted_average_sum - median_) / std_deviation
    mode_assimetry = (weighted_average_sum - mode_) / std_deviation

    simple_average = sum(data) / len(data)
    median_nda = median(data)
    mode_nda = mode(data)
    variance_nda = variance(data)
    std_deviation_nda = stdev(data)
    std_avg_error_nda = std_deviation_nda / sqrt(len(data))
    variation_coeff_nda = std_deviation_nda / simple_average
    median_assimetry_nda = 3 * (simple_average - median_nda) / std_deviation_nda
    mode_assimetry_nda = (simple_average - mode_nda) / std_deviation_nda

    relative_error = (abs(weighted_average_sum - sum(data) / len(data)) / weighted_average_sum)

    with open(output_file_path, 'w+', encoding="utf-8") as file:

        file.write("Classe:Frequência:pi:Pi:Xi:Xi * pi:di^2 * pi\n")

        for i, class_ in enumerate(classes):

            str_class = f"{class_[0]:.3f} ˫ {class_[1]:.3f}:{frequency[i]}:{proportion[i]:.3f}:" + \
                        f"{acc_proportion[i]:.3f}:{middle_point[i]:.3f}:{weighted_average[i]:.3f}:{variance_[i]:.3f}\n"

            str_class = str_class.replace('.', ',')
            file.write(str_class)

        str_total = f"Total:{sum(frequency)}:{sum(proportion):.3f}:-:-:{weighted_average_sum:.3f}:" + \
                    f"{variance_sum:.3f}\n\n"

        str_total = str_total.replace('.', ',')
        file.write(str_total)

        file.write(f"Média ponderada:{weighted_average_sum:.3f}:".replace('.', ',') +
                   f"Média simples:{simple_average:.3f}\n".replace('.', ','))

        file.write(f"Mediana:{median_:.3f}:".replace('.', ',') +
                   f"Mediana NDA:{median_nda:.3f}\n".replace('.', ','))

        file.write(f"Moda:{mode_:.3f}:".replace('.', ',') +
                   f"Moda NDA:{mode_nda:.3f}\n".replace('.', ','))

        file.write(f"Variância:{variance_sum:.3f}:".replace('.', ',') +
                   f"Variância NDA:{variance_nda:.3f}\n".replace('.', ','))

        file.write(f"Desvio Padrão:{std_deviation:.3f}:".replace('.', ',') +
                   f"Desvio Padrão NDA:{std_deviation_nda:.3f}\n".replace('.', ','))

        file.write(f"Erro padrão da média:{std_avg_error:.3f}:".replace('.', ',') +
                   f"Erro padrão da média NDA:{std_avg_error_nda:.3f}\n".replace('.', ','))

        file.write(f"Coeficiente de variação:{variation_coeff:.3f}:".replace('.', ',') +
                   f"Coeficiente de variação NDA:{variation_coeff_nda:.3f}\n".replace('.', ','))

        file.write(f"Assimetria da mediana:{median_assimetry:.3f}:".replace('.', ',') +
                   f"Assimetria da mediana NDA:{median_assimetry_nda:.3f}\n".replace('.', ','))

        file.write(f"Assimetria da moda:{mode_assimetry:.3f}:".replace('.', ',') +
                   f"Assimetria da moda NDA:{mode_assimetry_nda:.3f}\n".replace('.', ','))

        file.write(f"Erro relativo:{relative_error:.5f}\n".replace('.', ','))


def histogram(title: str, color: str, data: list):
    '''
    Gera um histograma com o dados comparativos.
    '''

    classes = generate_classes(data)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data,
        xbins=dict(
            start=classes[0][0],
            end=classes[-1][1],
            size=(classes[1][0] + classes[1][1]) / 2 - (classes[0][0] + classes[0][1]) / 2
        ),
        marker_color=color,
        opacity=0.75
    ))

    fig.update_layout(
        title_text=title,
        xaxis=dict(
            ticks="outside",
            tick0=(classes[0][0] + classes[0][1]) / 2,
            dtick=(classes[1][0] + classes[1][1]) / 2 - (classes[0][0] + classes[0][1]) / 2),
        xaxis_title_text='Pontos médio da classe',
        yaxis_title_text='Frequência',
        bargap=0.1,
        bargroupgap=0
    )

    fig.show()


def box_plot(title: str, title_a: str, title_b: str, data_a: list, data_b: list):
    '''
    Faz o plot de um diagrama de caixas comparativo.
    '''

    fig = go.Figure()
    fig.add_trace(go.Box(y=data_a, name=title_a))
    fig.add_trace(go.Box(y=data_b, name=title_b))

    fig.update_layout(
        title_text=title,
    )

    fig.show()


def average_proportion(data: list):
    '''
    Calcula a proporção simples.
    '''

    simple_average = sum(data) / len(data)
    std_deviation = stdev(data)

    count = 0

    for value in data:

        if simple_average - std_deviation <= value <= simple_average + std_deviation:
            count += 1

    print(f"Proporção: {count / len(data):.3f}")


def above_average_proportion(data: list):
    '''
    Calcula a proporção simples.
    '''

    simple_average = sum(data) / len(data)
    std_deviation = stdev(data)

    count = 0

    for value in data:

        if value > simple_average + 2 * std_deviation:
            count += 1

    print(f"Proporção: {count / len(data):.3f}")


def simple_proportion(data: list, std_deviation: float, average: float, multiplier: float):
    '''
    Calcula a proporção simples.
    '''

    simple_average = sum(data) / len(data)
    simple_std_deviation = stdev(data)

    filtered_data = []

    if multiplier >= 0:
        filtered_data = list(filter(lambda x: x >= average + std_deviation * multiplier, data))
    else:
        filtered_data = list(filter(lambda x: x <= average + std_deviation * multiplier, data))

    count = len(filtered_data)
    probability = sum(filtered_data)

    print(filtered_data)
    print(count)

    print(f"Proporção com std_dev = {multiplier}: {((count / len(data)) * 100.0):.2f}%, "
          f"Probabilidade: {((probability / count)):.2f}%")

    if multiplier >= 0:
        filtered_data = list(filter(lambda x: x >= simple_average + simple_std_deviation * multiplier, data))
    else:
        filtered_data = list(filter(lambda x: x <= simple_average + simple_std_deviation * multiplier, data))

    count = len(filtered_data)
    probability = sum(filtered_data)

    print(f"Proporção simples com std_dev = {multiplier}: {((count / len(data)) * 100.0):.2f}%, "
          f"Probabilidade simples: {((probability / count)):.2f}%")



def empirical_rule_check(data: list, std_deviation: float, average: float, multiplier: float):
    '''
    Checa a regra empírica.
    '''

    simple_average = sum(data) / len(data)
    simple_std_deviation = stdev(data)

    count = 0
    probability = 0

    for value in data:

        if average - std_deviation * multiplier <= value <= average + std_deviation * multiplier:
            count += 1
            probability += value

    print(f"Proporção empírica M{multiplier}: {((count / len(data)) * 100.0):.2f}%, "
          f"Probabilidade: {((probability / count) * 100.0):.2f}%")

    count = 0
    probability = 0

    for value in data:

        if simple_average - simple_std_deviation * multiplier \
           <= value <=                                        \
           simple_average + simple_std_deviation * multiplier:
            count += 1
            probability += value

    print(f"Proporção simples M{multiplier}: {((count / len(data)) * 100.0):.2f}%, "
          f"Probabilidade: {((probability / count) * 100.0):.2f}%")


def pdfwrapper(mean: float, std_deviation: float, value: float):
    '''
    Calcula a densidade de probabilidade.
    '''

    normal_distribution = NormalDist(mean, std_deviation)
    print(normal_distribution.pdf(value))
