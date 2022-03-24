# -*- coding: utf-8 -*-

'''
Ferramentas estatísticas.

Python 3.10.2
'''

from os.path import join

from stat_analysis import DataProcessing, StemAndLeavesDiagram, EmpiricalModel, Ploting, Probability

print("INE5405 - Ferramentas de estatísica e probabilidade")

data = {}
empirical_models = {}

while True:

    command = input(">>> ").split()

    match command[0]:
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

            print("Concluído.")
        case "serialize_comp" | "sc":

            print("Serializando dados.")

            try:

                with open(join("Data", "Processed", "Total.txt"), 'r', encoding="utf-8") as file:
                    data["Total"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("Total serizalizado.")

                with open(join("Data", "Processed", "SC.txt"), 'r', encoding="utf-8") as file:
                    data["SC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("SC serizalizado.")

                with open(join("Data", "Processed", "RS.txt"), 'r', encoding="utf-8") as file:
                    data["RS"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("RS serizalizado.")

                with open(join("Data", "Processed", "NAC.txt"), 'r', encoding="utf-8") as file:
                    data["NAC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("NAC serizalizado.")

                with open(join("Data", "Processed", "OUTR.txt"), 'r', encoding="utf-8") as file:
                    data["OUTR"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("OUTR serizalizado.")

                with open(join("Data", "Processed", "METRO.txt"), 'r', encoding="utf-8") as file:
                    data["METRO"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("METRO serizalizado.")

                with open(join("Data", "Processed", "INT.txt"), 'r', encoding="utf-8") as file:
                    data["INT"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("INT serizalizado.")
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

            Ploting.box_plot("Estados", "Santa Catarina", "Rio Grande do Sul", data["SC"], data["RS"])
            print("Estados construídos")

            Ploting.box_plot("Postos", "Nacionais", "Outros", data["NAC"], data["OUTR"])
            print("Postos construídos")

            Ploting.box_plot("Regiões", "Metropolitanas", "Interior", data["METRO"], data["INT"])
            print("Regiões construídos")

            print("Concluído.")
        case "proportion" | "prop":

            print("Calculando proporções")

            print("SC")
            Probability.average_proportion(data["SC"])
            print("RS")
            Probability.average_proportion(data["RS"])
            print("NAC")
            Probability.average_proportion(data["NAC"])
            print("OUTR")
            Probability.average_proportion(data["OUTR"])
            print("METRO")
            Probability.average_proportion(data["METRO"])
            print("INT")
            Probability.average_proportion(data["INT"])

            print("Concluído.")
        case "proportion2" | "prop2":

            print("Calculando proporções")

            print("SC")
            Probability.above_average_proportion(data["SC"])
            print("RS")
            Probability.above_average_proportion(data["RS"])
            print("NAC")
            Probability.above_average_proportion(data["NAC"])
            print("OUTR")
            Probability.above_average_proportion(data["OUTR"])
            print("METRO")
            Probability.above_average_proportion(data["METRO"])
            print("INT")
            Probability.above_average_proportion(data["INT"])

            print("Concluído.")
        case "empirical_rule" | "emprl":
            print("Checando a regra empírica")

            print("SC")
            Probability.empirical_rule_check(data["SC"], 0.171, 5.303, 1)
            Probability.empirical_rule_check(data["SC"], 0.171, 5.303, 2)
            Probability.empirical_rule_check(data["SC"], 0.171, 5.303, 3)
            print("NAC")
            Probability.empirical_rule_check(data["NAC"], 0.267, 5.364, 1)
            Probability.empirical_rule_check(data["NAC"], 0.267, 5.364, 2)
            Probability.empirical_rule_check(data["NAC"], 0.267, 5.364, 3)
            print("METRO")
            Probability.empirical_rule_check(data["METRO"], 0.173, 5.292, 1)
            Probability.empirical_rule_check(data["METRO"], 0.173, 5.292, 2)
            Probability.empirical_rule_check(data["METRO"], 0.173, 5.292, 3)

            print("Concluído.")
        case "extreme_prices" | "xp":
            print("Calculando as proporções extremas")

            print("Total")
            Probability.simple_proportion(data["Total"], 0.209, 5.35, -2.5)
            Probability.simple_proportion(data["Total"], 0.209, 5.35, 2.5)

            print("Concluído.")
        case _:
            print("Comando não reconhecido.")
