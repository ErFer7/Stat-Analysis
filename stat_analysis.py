# -*- coding: utf-8 -*-

'''
Análise estatística.
'''

from cmath import inf
import csv
import json

from os.path import join
from math import log10, ceil, sqrt, exp, pi
from statistics import median, mode, variance, stdev

from scipy import integrate

import plotly.graph_objects as go


class MathMethods():

    '''
    Wrapper para métodos matemáticos.
    '''

    @staticmethod
    def z_score(z_value: float):
        '''
        Calcula o z score.
        '''

        return integrate.quad(lambda z: (1.0 / sqrt(2.0 * pi)) * exp(-(z ** 2.0 / 2.0)), -inf, z_value)[0]


class DataProcessing():

    '''
    Wrapper para os métodos de processamento de dados.
    '''

    @staticmethod
    def csv2json(input_file_path: str, output_file_path: str) -> None:
        '''
        Gera um arquivo .json a partir de um arquivo csv.

        input_file_path (str): Arquivo .csv de entrada.
        output_file_path (str): Arquivo .json de saída.
        '''

        processed_dict = {}

        with open(input_file_path, mode='r', encoding="utf-8") as csv_file:

            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                processed_dict[row[0]] = row[1:]

        with open(output_file_path, 'w+', encoding="utf-8") as file:

            data_json = json.dumps(processed_dict, indent=4)
            file.write(data_json)

    @staticmethod
    def process_data(input_file_path: str,
                     output_files_path: str,
                     selected_categories: tuple,
                     value_index: int,
                     total: bool = True,
                     filter_: tuple = None) -> None:
        '''
        Processa todos os dados e gera arquivos com os dados agrupados.

        input_file_path (str): Arquivo .json de entrada.
        output_files_path (str): Diretório em que os arquivos gerados serão armazenados, estes arquivos serão gerados
        no formado .txt.
        selected_categories (tuple): Tupla de inteiros com os índices das entradas selecionadas no json para o
        processamento dos dados.
        value_index (int): Índice em cada entrada no json que contém o valor numérico a ser processado.
        total (bool) (Opcional): Indica se um agrupamento total deve ser gerado.
        '''

        data = {}

        with open(input_file_path, 'r', encoding="utf-8") as json_file:

            data = json.load(json_file)

        output_data = {}

        if total:
            output_data["Total"] = []

        for data_value in data.values():

            value = float(data_value[value_index].replace(',', '.'))

            if total:
                output_data["Total"].append(value)

            if filter_ is None:

                for category in selected_categories:

                    if data_value[category] not in output_data:
                        output_data[data_value[category]] = []

                    output_data[data_value[category]].append(value)
            else:

                if data_value[filter_[1]] == filter_[0]:

                    for category in selected_categories:

                        if data_value[category] not in output_data:
                            output_data[data_value[category]] = []

                        output_data[data_value[category]].append(value)

        for category_key, category_values in output_data.items():

            file_name = f"{category_key}.txt" if filter_ is None else f"{filter_[0]} - {category_key}.txt"

            with open(join(output_files_path, file_name), 'w+', encoding="utf-8") as file:

                for value in category_values:
                    file.write(str(value) + '\n')


class StemAndLeavesDiagram():

    '''
    Representação de um diagrama de ramos e folhas.

    total_data (list): Lista com os dados totais.
    data_left (list): Lista com os dados à esquerda do centro.
    data_right (list): Lista com os dados à direita do centro.
    header_left (str): Cabeçalhos dos dados à esquerda.
    header_right (str): Cabeçalhos dos dados à direita.
    '''

    stem: list
    left_leaves: list
    right_leaves: list
    left_frequency: list
    right_frequency: list
    header_left: str
    header_right: str

    def __init__(self,
                 total_data: list,
                 data_left: list,
                 data_right: list,
                 header_left: str,
                 header_right: str) -> None:

        self.stem = []
        self.left_leaves = []
        self.right_leaves = []
        self.left_frequency = []
        self.right_frequency = []
        self.header_left = header_left
        self.header_right = header_right

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

        self.stem = list(center_column_left.keys())

        min_key = float(self.stem[0])
        max_key = float(self.stem[-1])
        current_key = min_key
        i = 0

        while current_key < max_key:

            str_key = f"{current_key:.1f}"

            if str_key not in self.stem:
                self.stem.insert(i, str_key)

            i += 1
            current_key += 0.1

        for i, key in enumerate(self.stem):
            self.left_leaves.append([])
            self.right_leaves.append([])

            left_sum = 0

            if key in center_column_left:

                for leaf in center_column_left[key]:
                    left_sum += center_column_left[key][leaf]
                    self.left_leaves[i].append((leaf, center_column_left[key][leaf]))

            right_sum = 0

            if key in center_column_right:

                for leaf in center_column_right[key]:
                    right_sum += center_column_right[key][leaf]
                    self.right_leaves[i].append((leaf, center_column_right[key][leaf]))

            self.left_frequency.append(left_sum)
            self.right_frequency.append(right_sum)
            self.left_leaves[i] = sorted(self.left_leaves[i], key=lambda val: float(val[0]), reverse=True)
            self.right_leaves[i] = sorted(self.right_leaves[i], key=lambda val: float(val[0]))

        for i, branch in enumerate(self.left_leaves):

            str_branch = ''

            for leaf in branch:
                str_branch += f"({leaf[0]}/{leaf[1]}) "

            self.left_leaves[i] = str_branch

        for i, branch in enumerate(self.right_leaves):

            str_branch = ''

            for leaf in branch:
                str_branch += f"({leaf[0]}/{leaf[1]}) "

            self.right_leaves[i] = str_branch

    def write(self, output_file_path: str) -> None:
        '''
        Escreve o diagrama em um arquivo.

        output_file_path (str): Caminho para o arquivo em que o diagrama é escrito.
        '''

        with open(output_file_path, 'w+', encoding="utf-8") as file:

            file.write(f"Freq:Folhas ({self.header_left}):Ramos:Folhas ({self.header_right}):Freq\n")

            for i, branch in enumerate(self.stem):
                file.write(f"{self.left_frequency[i]}:"
                           f"{self.left_leaves[i]}:"
                           f"{branch}:"
                           f"{self.right_leaves[i]}:"
                           f"{self.right_frequency[i]}\n")


class EmpiricalModel():

    '''
    Modelo empírico.

    data (list): Dados usados no modelo empírico.
    '''

    data: list
    classes: list
    min_value: float
    max_value: float
    class_range: float
    class_kf: float
    class_k: int
    class_amp: float
    frequency: list
    proportion: list
    acc_proportion: list
    middle_point: list
    weighted_average: list
    weighted_average_sum: float
    variance_: list
    median_: float
    mode_: float
    variance_sum: float
    std_deviation: float
    std_avg_error: float
    variation_coeff: float
    median_assimetry: float
    mode_assimetry: float
    simple_average: float
    median_nda: float
    mode_nda: float
    variance_nda: float
    std_deviation_nda: float
    std_avg_error_nda: float
    variation_coeff_nda: float
    median_assimetry_nda: float
    mode_assimetry_nda: float
    relative_error: float

    def __init__(self, data: list) -> None:

        self.data = data
        self.classes = []
        self.min_value = min(self.data)
        self.max_value = max(self.data)
        self.class_range = self.max_value - self.min_value
        self.class_kf = 1 + 3.32 * log10(len(self.data))
        self.class_k = ceil(self.class_kf)
        self.class_amp = self.class_range / self.class_kf
        self.frequency = []
        self.proportion = []
        self.acc_proportion = []
        self.middle_point = []
        self.weighted_average = []
        self.weighted_average_sum = 0.0
        self.variance_ = []
        self.median_ = 0.0
        self.mode_ = 0.0
        self.variance_sum = 0.0
        self.std_deviation = 0.0
        self.std_avg_error = 0.0
        self.variation_coeff = 0.0
        self.median_assimetry = 0.0
        self.mode_assimetry = 0.0
        self.simple_average = 0.0
        self.median_nda = 0.0
        self.mode_nda = 0.0
        self.variance_nda = 0.0
        self.std_deviation_nda = 0.0
        self.std_avg_error_nda = 0.0
        self.variation_coeff_nda = 0.0
        self.median_assimetry_nda = 0.0
        self.mode_assimetry_nda = 0.0
        self.relative_error = 0.0

        # Geração das classes
        for i in range(self.class_k):
            self.classes.append((self.min_value + self.class_amp * i, self.min_value + self.class_amp * (i + 1)))

        # Contagem da frequência
        self.frequency = [0 for _ in range(len(self.classes))]

        for value in self.data:

            for i, class_ in enumerate(self.classes):

                if class_[1] > value >= class_[0]:
                    self.frequency[i] += 1

        # Contagem da proporção
        for freq in self.frequency:
            self.proportion.append(freq / len(self.data))

        # Contagem da proporção acumulada
        acc_prop = 0.0

        for prop in self.proportion:

            self.acc_proportion.append(prop + acc_prop)
            acc_prop += prop

        # Geração dos pontos médios
        for i, class_ in enumerate(self.classes):

            self.middle_point.append((class_[0] + class_[1]) / 2)
            self.weighted_average.append(self.proportion[i] * self.middle_point[i])

        # Cálculo da variância
        self.weighted_average_sum = sum(self.weighted_average)

        for i, class_ in enumerate(self.classes):
            self.variance_.append(((self.middle_point[i] - self.weighted_average_sum) ** 2) * self.proportion[i])

        self.median_ = median(self.data)
        self.mode_ = self.middle_point[self.frequency.index(max(self.frequency))]
        self.variance_sum = sum(self.variance_)
        self.std_deviation = sqrt(self.variance_sum)
        self.std_avg_error = self.std_deviation / sqrt(len(self.data))
        self.variation_coeff = self.std_deviation / self.weighted_average_sum
        self.median_assimetry = 3 * (self.weighted_average_sum - self.median_) / self.std_deviation
        self.mode_assimetry = (self.weighted_average_sum - self.mode_) / self.std_deviation

        self.simple_average = sum(data) / len(data)
        self.median_nda = median(data)
        self.mode_nda = mode(data)
        self.variance_nda = variance(data)
        self.std_deviation_nda = stdev(data)
        self.std_avg_error_nda = self.std_deviation_nda / sqrt(len(data))
        self.variation_coeff_nda = self.std_deviation_nda / self.simple_average
        self.median_assimetry_nda = 3 * (self.simple_average - self.median_nda) / self.std_deviation_nda
        self.mode_assimetry_nda = (self.simple_average - self.mode_nda) / self.std_deviation_nda

        self.relative_error = (abs(self.weighted_average_sum - sum(data) / len(data)) / self.weighted_average_sum)

    def write(self, output_file_path: str) -> None:
        '''
        Escreve a tabela do modelo em um arquivo.

        output_file_path (str): Caminho para o arquivo onde o modelo é escrito.
        '''

        with open(output_file_path, 'w+', encoding="utf-8") as file:

            file.write("Classe:Frequência:pi:Pi:Xi:Xi * pi:di^2 * pi\n")

            for i, class_ in enumerate(self.classes):

                str_class = f"{class_[0]:.3f} ˫ {class_[1]:.3f}:{self.frequency[i]}:{self.proportion[i]:.3f}:" + \
                            f"{self.acc_proportion[i]:.3f}:{self.middle_point[i]:.3f}:" +                        \
                            f"{self.weighted_average[i]:.3f}:{self.variance_[i]:.3f}\n"

                str_class = str_class.replace('.', ',')
                file.write(str_class)

            str_total = f"Total:{sum(self.frequency)}:{sum(self.proportion):.3f}:-:-:" + \
                        f"{self.weighted_average_sum:.3f}:{self.variance_sum:.3f}\n\n"

            str_total = str_total.replace('.', ',')
            file.write(str_total)

            file.write(f"Média ponderada:{self.weighted_average_sum:.3f}:".replace('.', ',') +
                       f"Média simples:{self.simple_average:.3f}\n".replace('.', ','))

            file.write(f"Mediana:{self.median_:.3f}:".replace('.', ',') +
                       f"Mediana NDA:{self.median_nda:.3f}\n".replace('.', ','))

            file.write(f"Moda:{self.mode_:.3f}:".replace('.', ',') +
                       f"Moda NDA:{self.mode_nda:.3f}\n".replace('.', ','))

            file.write(f"Variância:{self.variance_sum:.3f}:".replace('.', ',') +
                       f"Variância NDA:{self.variance_nda:.3f}\n".replace('.', ','))

            file.write(f"Desvio Padrão:{self.std_deviation:.3f}:".replace('.', ',') +
                       f"Desvio Padrão NDA:{self.std_deviation_nda:.3f}\n".replace('.', ','))

            file.write(f"Erro padrão da média:{self.std_avg_error:.3f}:".replace('.', ',') +
                       f"Erro padrão da média NDA:{self.std_avg_error_nda:.3f}\n".replace('.', ','))

            file.write(f"Coeficiente de variação:{self.variation_coeff:.3f}:".replace('.', ',') +
                       f"Coeficiente de variação NDA:{self.variation_coeff_nda:.3f}\n".replace('.', ','))

            file.write(f"Assimetria da mediana:{self.median_assimetry:.3f}:".replace('.', ',') +
                       f"Assimetria da mediana NDA:{self.median_assimetry_nda:.3f}\n".replace('.', ','))

            file.write(f"Assimetria da moda:{self.mode_assimetry:.3f}:".replace('.', ',') +
                       f"Assimetria da moda NDA:{self.mode_assimetry_nda:.3f}\n".replace('.', ','))

            file.write(f"Erro relativo:{self.relative_error:.5f}\n".replace('.', ','))

    def histogram(self, title: str, color: str) -> None:
        '''
        Gera um histograma com o dados comparativos.

        title (str): Título do histograma.
        color (str): Cor do histograma.
        empirical_model (EmpiricalModel): Modelo empírico do histograma.
        '''

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=self.data,
            xbins=dict(
                start=self.classes[0][0],
                end=self.classes[-1][1],
                size=(self.classes[1][0] + self.classes[1][1]) / 2 - (self.classes[0][0] + self.classes[0][1]) / 2
            ),
            marker_color=color,
            opacity=0.75
        ))

        fig.update_layout(
            title_text=title,
            xaxis=dict(
                ticks="outside",
                tick0=(self.classes[0][0] + self.classes[0][1]) / 2,
                dtick=(self.classes[1][0] + self.classes[1][1]) / 2 - (self.classes[0][0] + self.classes[0][1]) / 2),
            xaxis_title_text='Pontos médio da classe',
            yaxis_title_text='Frequência',
            bargap=0.1,
            bargroupgap=0
        )

        fig.show()

    def average_relative_proportion(self, multiplier: float, inclusive: bool) -> float:
        '''
        Proporção em relação à média usando o desvio padrão.

        multiplier (float): Coeficiente do desvio padrão em relação à média, valores positivos correspondem à
        proporção acima da média, valores negativos correspondem à proporção abaixo da média.
        '''

        filtered_data = []

        if inclusive:

            if multiplier >= 0:
                filtered_data = list(filter(lambda x: self.weighted_average_sum <= x
                                            <= self.weighted_average_sum + self.std_deviation * multiplier,
                                            self.data))
            else:
                filtered_data = list(filter(lambda x: self.weighted_average_sum + self.std_deviation * multiplier <= x
                                            <= self.weighted_average_sum,
                                            self.data))
        else:

            if multiplier >= 0:
                filtered_data = list(filter(lambda x: x >= self.weighted_average_sum + self.std_deviation * multiplier,
                                            self.data))
            else:
                filtered_data = list(filter(lambda x: x <= self.weighted_average_sum + self.std_deviation * multiplier,
                                            self.data))

        count = len(filtered_data)
        proportion = count / len(self.data)

        print(f"Proporção com {multiplier} std_dev: {(proportion * 100.0):.2f}% "
              f"({proportion:.4f})")

        return proportion

    def around_average_relative_proportion(self, multiplier: float, inclusive: bool) -> float:
        '''
        Proporção em relação à média usando o desvio padrão.

        multiplier (float): Coeficiente do desvio padrão em relação à média, tanto acima como abaixo.
        '''

        proportion = self.average_relative_proportion(-multiplier, inclusive) + \
            self.average_relative_proportion(multiplier, inclusive)

        print(f"Proporção em torno da média com {multiplier} std_dev: {(proportion * 100.0):.2f}% "
              f"({proportion:.4f})")

        return proportion

    def nda_average_relative_proportion(self, multiplier: float, inclusive: bool) -> float:
        '''
        Proporção em relação à média simples usado o desvio padrão simples.

        multiplier (float): Coeficiente do desvio padrão em relação à média, valores positivos correspondem à
        proporção acima da média, valores negativos correspondem à proporção abaixo da média.
        '''

        if inclusive:

            if multiplier >= 0:
                filtered_data = list(filter(lambda x: self.simple_average <= x
                                            <= self.simple_average + self.std_deviation_nda * multiplier,
                                            self.data))
            else:
                filtered_data = list(filter(lambda x: self.simple_average + self.std_deviation_nda * multiplier <= x
                                            <= self.simple_average,
                                            self.data))
        else:

            if multiplier >= 0:
                filtered_data = list(filter(lambda x: x >= self.simple_average + self.std_deviation_nda * multiplier,
                                            self.data))
            else:
                filtered_data = list(filter(lambda x: x <= self.simple_average + self.std_deviation_nda * multiplier,
                                            self.data))

        count = len(filtered_data)
        proportion = count / len(self.data)

        print(f"Proporção nda com {multiplier} std_dev: {(proportion * 100.0):.2f}% "
              f"({proportion:.4f})")

        return proportion

    def nda_around_average_relative_proportion(self, multiplier: float, inclusive: bool) -> float:
        '''
        Proporção em relação à média simples usando o desvio padrão simples.

        multiplier (float): Coeficiente do desvio padrão em relação à média, tanto acima como abaixo.
        '''

        proportion = self.nda_average_relative_proportion(-multiplier, inclusive) + \
            self.nda_average_relative_proportion(multiplier, inclusive)

        print(f"Proporção nda em torno da média com {multiplier} std_dev: {(proportion * 100.0):.2f}% "
              f"({proportion:.4f})")

        return proportion

    def chi_squared_test(self, output_file_path: str):
        '''
        Teste do Qui-quadrado.
        '''

        expected_values = []
        valid_classes_index = list(range(len(self.classes)))

        z_value = 0.0
        z_sum = 0.0

        inf_class = 0.0
        sup_class = 0.0
        inf_freq = 0.0
        sup_freq = 0.0
        inf_exp_value = 0.0
        sup_exp_value = 0.0

        # Calcula os valores esperados
        for i, class_ in enumerate(self.classes):

            z_inf = round((class_[0] - self.weighted_average_sum) / self.std_deviation, 2)
            z_sup = round((class_[1] - self.weighted_average_sum) / self.std_deviation, 2)

            z_value = MathMethods.z_score(z_sup) - z_sum if i < len(self.classes) - 1 \
                else 1.0 - MathMethods.z_score(z_inf)

            z_sum += z_value

            exp_value = sum(self.frequency) * z_value
            expected_values.append(exp_value)

        inf_exp_value = 0.0
        inf_freq = 0
        inf_class = 0.0
        index = 0

        # Colapsa os valores do limite inferior
        while True:

            inf_exp_value += expected_values[index]
            inf_freq += self.frequency[index]
            inf_class = self.classes[index][1]

            if inf_exp_value <= 5:
                valid_classes_index.remove(index)
                index += 1
            else:

                if index > 0:
                    valid_classes_index.remove(index)
                break

        sup_exp_value = 0.0
        sup_freq = 0
        sup_class = 0.0
        index = len(self.classes) - 1

        # Colapsa os valores do limite superior
        while True:

            sup_exp_value += expected_values[index]
            sup_freq += self.frequency[index]
            sup_class = self.classes[index][0]

            if sup_exp_value <= 5:
                valid_classes_index.remove(index)
                index -= 1
            else:

                if index < len(self.classes) - 1:
                    valid_classes_index.remove(index)
                break

        with open(output_file_path, 'w+', encoding="utf-8") as file:

            chi_squared_sum = 0.0

            file.write("Classes:Oi:Ei:(Oi - Ei)^2/Ei\n")

            if 0 not in valid_classes_index:

                chi_squared = (inf_freq - inf_exp_value) ** 2.0 / inf_exp_value
                chi_squared_sum += chi_squared

                file.write(f"Menos de {inf_class:.3f}:{inf_freq}:{inf_exp_value:.3f}".replace('.', ',') +
                           f":{chi_squared:.3f}\n".replace('.', ','))

            for i in valid_classes_index:

                chi_squared = (self.frequency[i] - expected_values[i]) ** 2.0 / expected_values[i]
                chi_squared_sum += chi_squared

                file.write(f"{self.classes[i][0]:.3f} ˫ {self.classes[i][1]:.3f}:".replace('.', ',') +
                           f"{self.frequency[i]}:{expected_values[i]:.3f}:".replace('.', ',') +
                           f"{chi_squared:.3f}\n".replace('.', ','))

            if len(self.classes) - 1 not in valid_classes_index:

                chi_squared = (sup_freq - sup_exp_value) ** 2.0 / sup_exp_value
                chi_squared_sum += chi_squared

                file.write(f"Mínimo de {sup_class:.3f}:{sup_freq}:{sup_exp_value:.3f}".replace('.', ',') +
                           f":{chi_squared:.3f}\n".replace('.', ','))

            file.write(f"Total:{sum(self.frequency)}:{round(sum(expected_values))}".replace('.', ',') +
                           f":{chi_squared_sum:.3f}\n".replace('.', ','))

    def f_snedecor(self):
        '''
        Distribuição de Fisher-Snedecor.
        '''

        raise NotImplementedError

    def t_student(self):
        '''
        Distribuição de t-Student.
        '''

        raise NotImplementedError


class Ploting():

    '''
    Wrapper para os métodos de plotagem.
    '''
    @staticmethod
    def box_plot(title: str, data: list) -> None:
        '''
        Faz o plot de um diagrama de caixas comparativo.

        title (str): Título do boxplot.
        data (list): Dados.
        '''

        fig = go.Figure()
        fig.add_trace(go.Box(y=data))

        fig.update_layout(
            title_text=title,
        )

        fig.show()

    @staticmethod
    def double_box_plot(title: str, title_a: str, title_b: str, data_a: list, data_b: list) -> None:
        '''
        Faz o plot de um diagrama de caixas comparativo.

        title (str): Título do boxplot.
        title_a (str): Título da caixa esquerda.
        title_b (str): Título da caixa direita.
        data_a (list): Dados da caixa esquerda.
        data_b (list): Dados da caixa direita.
        '''

        fig = go.Figure()
        fig.add_trace(go.Box(y=data_a, name=title_a))
        fig.add_trace(go.Box(y=data_b, name=title_b))

        fig.update_layout(
            title_text=title,
        )

        fig.show()
