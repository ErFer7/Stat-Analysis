# -*- coding: utf-8 -*-

'''
Ferramentas estatísticas.

Python 3.10.2
'''

from os.path import join

from stat_analysis import DataProcessing, StemAndLeavesDiagram, EmpiricalModel, Ploting

print("INE5405 - Ferramentas de estatísica e probabilidade")

data = {}
empirical_models = {}

while True:

    command = input(">>> ")

    match command:
        case "quit" | 'q':

            print("Saindo.")
            break
        case "csv2json" | "c2j":

            print("Convertendo de csv para json.")

            DataProcessing.csv2json(join("Data", "Raw", "Coleta.csv"),
                                    join("Data", "Processed", "Coleta.json"))

            print("Concluído.")
        case "process_data" | "pd":

            print("Processando dados.")

            DataProcessing.process_data(join("Data", "Processed", "Coleta.json"),
                                        join("Data", "Processed"),
                                        (1, 3, 5),
                                        4)

            DataProcessing.process_data(join("Data", "Processed", "Coleta.json"),
                                        join("Data", "Processed"),
                                        (3, 5),
                                        4,
                                        False,
                                        ("SC", 1))

            DataProcessing.process_data(join("Data", "Processed", "Coleta.json"),
                                        join("Data", "Processed"),
                                        (3, 5),
                                        4,
                                        False,
                                        ("RS", 1))


            print("Concluído.")
        case "serialize_comp" | "sc":

            print("Serializando dados.")

            try:

                with open(join("Data", "Processed", "Total.txt"), 'r', encoding="utf-8") as file:
                    data["Total"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "SC.txt"), 'r', encoding="utf-8") as file:
                    data["SC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "RS.txt"), 'r', encoding="utf-8") as file:
                    data["RS"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "NAC.txt"), 'r', encoding="utf-8") as file:
                    data["NAC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "OUTR.txt"), 'r', encoding="utf-8") as file:
                    data["OUTR"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "METRO.txt"), 'r', encoding="utf-8") as file:
                    data["METRO"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "INT.txt"), 'r', encoding="utf-8") as file:
                    data["INT"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "SC - NAC.txt"), 'r', encoding="utf-8") as file:
                    data["SC - NAC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "SC - OUTR.txt"), 'r', encoding="utf-8") as file:
                    data["SC - OUTR"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "SC - METRO.txt"), 'r', encoding="utf-8") as file:
                    data["SC - METRO"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "RS - NAC.txt"), 'r', encoding="utf-8") as file:
                    data["RS - NAC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "RS - OUTR.txt"), 'r', encoding="utf-8") as file:
                    data["RS - OUTR"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "RS - METRO.txt"), 'r', encoding="utf-8") as file:
                    data["RS - METRO"] = list(map(lambda val: float(val.strip()), file.readlines()))

                with open(join("Data", "Processed", "RS - INT.txt"), 'r', encoding="utf-8") as file:
                    data["RS - INT"] = list(map(lambda val: float(val.strip()), file.readlines()))
            except FileNotFoundError:

                print("Os arquivos não existem, lembre-se de processar os dados!")

            print("Concluído.")
        case "stem_and_leaves" | "sl":

            print("Construindo diagramas de ramos e folhas.")

            states = StemAndLeavesDiagram(data["Total"],
                                          data["SC"],
                                          data["RS"],
                                          "Santa Catarina",
                                          "Rio Grande do Sul")

            states.write(join("Data", "Represented", "Stem and Leaves - State.txt"))

            print("Diagrama de estados construído.")

            states = StemAndLeavesDiagram(data["Total"],
                                          data["NAC"],
                                          data["OUTR"],
                                          "Nacionais",
                                          "Outros")

            states.write(join("Data", "Represented", "Stem and Leaves - Gas Station.txt"))

            print("Diagrama de postos construído.")

            states = StemAndLeavesDiagram(data["Total"],
                                          data["METRO"],
                                          data["INT"],
                                          "Metropolitanas",
                                          "Interioranas")

            states.write(join("Data", "Represented", "Stem and Leaves - Region.txt"))

            print("Diagrama de regiões construído.")

            print("Concluído.")
        case "empirical_model" | "em":

            print("Construindo modelos empíricos.")

            for data_key, data_values in data.items():

                empirical_models[data_key] = EmpiricalModel(data_values)
                empirical_models[data_key].write(join("Data", "Represented", f"Empirical Model - {data_key}.txt"))

            print("Concluído.")
        case "histogram" | "h":

            print("Construindo histogramas.")

            empirical_models["Total"].histogram("Total",
                                                "#0000CC")

            print("Total construído.")

            empirical_models["SC"].histogram("Santa Catarina",
                                             "#0000CC")

            print("SC construído.")

            empirical_models["RS"].histogram("Rio Grande do Sul",
                                             "#0000CC")

            print("RS construído.")

            empirical_models["NAC"].histogram("Postos nacionais",
                                              "#0000CC")

            print("NAC construído.")

            empirical_models["OUTR"].histogram("Outros postos",
                                               "#0000CC")

            print("OUTR construído.")

            empirical_models["METRO"].histogram("Região metropolitana",
                                                "#0000CC")

            print("METRO construído.")

            empirical_models["INT"].histogram("Interior",
                                              "#0000CC")

            print("INT construído.")

            print("Concluído.")
        case "box_plot" | "bp":

            print("Construindo diagramas em caixas")

            Ploting.double_box_plot("Estados",
                                    "Santa Catarina",
                                    "Rio Grande do Sul",
                                    data["SC"],
                                    data["RS"])

            print("Estados construídos")

            Ploting.double_box_plot("Postos em Santa Catarina",
                                    "Nacionais",
                                    "Outros",
                                    data["SC - NAC"],
                                    data["SC - OUTR"])

            print("SC: Postos construídos")

            Ploting.double_box_plot("Postos no Rio Grande do Sul",
                                    "Nacionais",
                                    "Outros",
                                    data["RS - NAC"],
                                    data["RS - OUTR"])

            print("RS: Postos construídos")

            Ploting.box_plot("Região metropolitana em Santa Catarina", data["SC - METRO"])
            print("SC: Regiões construídas")

            Ploting.double_box_plot("Regiões no Rio Grande do Sul",
                                    "Metropolitanas",
                                    "Interior",
                                    data["RS - METRO"],
                                    data["RS - INT"])

            print("RS: Regiões construídas")

            print("Concluído.")
        case "proportion" | "pr":

            print("Calculando proporções")

            for empirical_model_key, empirical_model in empirical_models.items():

                print(empirical_model_key)
                empirical_model.nda_around_average_relative_proportion(1.0, True)
                print()

            print("Concluído.")
        case "proportion_2x_above" | "pr2xup":

            print("Calculando proporções")

            for empirical_model_key, empirical_model in empirical_models.items():

                print(empirical_model_key)
                empirical_model.nda_average_relative_proportion(2.0, False)
                print()

            print("Concluído.")
        case "empirical_rule" | "emprl":
            print("Checando a regra empírica")

            for empirical_model_key, empirical_model in empirical_models.items():

                print(empirical_model_key)

                for i in range(1, 4):
                    empirical_model.around_average_relative_proportion(i, True)
                    print()

                for i in range(1, 4):
                    empirical_model.nda_around_average_relative_proportion(i, True)
                    print()

            print("Concluído.")
        case "extreme_prices" | "xp":
            print("Calculando as proporções extremas")

            for empirical_model_key, empirical_model in empirical_models.items():

                print(empirical_model_key)
                empirical_model.average_relative_proportion(-2.5, False)
                empirical_model.average_relative_proportion(2.5, False)
                print()

            print("Concluído.")
        case "qui_squared_test" | "qst":
            print("Aplicando o teste do Qui-quadrado")

            for empirical_model_key, empirical_model in empirical_models.items():

                print(empirical_model_key)
                empirical_model.chi_squared_test()
                print()

            print("Concluído.")
        case _:
            print("Comando não reconhecido.")
