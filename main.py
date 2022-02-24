# -*- coding: utf-8 -*-

'''
Ferramentas estatísticas.

Python 3.10.2
'''

# TODO: Tornar o funcionamento mais genérico

import os
import stat_analysis

print("INE5405 - Ferramentas estatísticas para a disciplina")

data = {}

while True:

    command = input(">>> ")

    match command:
        case "exit" | 'q':

            print("Saindo.")
            break
        case "csv2json" | "c2j":

            print("Convertendo de csv para json.")

            stat_analysis.csv2json(os.path.join("Data", "Raw", "Coleta.csv"),
                                   os.path.join("Data", "Processed", "Coleta.json"))

            print("Concluído.")
        case "process_data":
            stat_analysis.process_data(os.path.join("Data", "Processed", "Coleta.json"),
                                       os.path.join("Data", "Processed", "Total.txt"),
                                       os.path.join("Data", "Processed", "SC.txt"),
                                       os.path.join("Data", "Processed", "RS.txt"),
                                       os.path.join("Data", "Processed", "NAC.txt"),
                                       os.path.join("Data", "Processed", "OUTR.txt"),
                                       os.path.join("Data", "Processed", "METRO.txt"),
                                       os.path.join("Data", "Processed", "INT.txt"))
        case "serialize_comp" | "sc":

            print("Serializando dados.")

            try:

                with open(os.path.join("Data", "Processed", "Total.txt"), 'r', encoding="utf-8") as file:
                    data["Total"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("Total serizalizado.")

                with open(os.path.join("Data", "Processed", "SC.txt"), 'r', encoding="utf-8") as file:
                    data["SC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("SC serizalizado.")

                with open(os.path.join("Data", "Processed", "RS.txt"), 'r', encoding="utf-8") as file:
                    data["RS"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("RS serizalizado.")

                with open(os.path.join("Data", "Processed", "NAC.txt"), 'r', encoding="utf-8") as file:
                    data["NAC"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("NAC serizalizado.")

                with open(os.path.join("Data", "Processed", "OUTR.txt"), 'r', encoding="utf-8") as file:
                    data["OUTR"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("OUTR serizalizado.")

                with open(os.path.join("Data", "Processed", "METRO.txt"), 'r', encoding="utf-8") as file:
                    data["METRO"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("METRO serizalizado.")

                with open(os.path.join("Data", "Processed", "INT.txt"), 'r', encoding="utf-8") as file:
                    data["INT"] = list(map(lambda val: float(val.strip()), file.readlines()))

                print("INT serizalizado.")
            except FileNotFoundError:

                print("Os arquivos não existem, lembre-se de processar os dados!")

            print("Concluído.")
        case "stem_and_leaves" | "sl":

            print("Construindo diagramas de ramos e folhas.")

            stat_analysis.stem_and_leaves(data["Total"],
                                          data["SC"],
                                          data["RS"],
                                          "Santa Catarina",
                                          "Rio Grande do Sul",
                                          os.path.join("Data", "Represented", "Stem and Leaves - State.txt"))

            print("Diagrama de estados construído.")

            stat_analysis.stem_and_leaves(data["Total"],
                                          data["NAC"],
                                          data["OUTR"],
                                          "Nacionais",
                                          "Outros",
                                          os.path.join("Data", "Represented", "Stem and Leaves - Gas Station.txt"))

            print("Diagrama de postos construído.")

            stat_analysis.stem_and_leaves(data["Total"],
                                          data["METRO"],
                                          data["INT"],
                                          "Metropolitanas",
                                          "Interioranas",
                                          os.path.join("Data", "Represented", "Stem and Leaves - Region.txt"))

            print("Diagrama de regiões construído.")

            print("Concluído.")
        case "empirical_model" | "em":

            print("Construindo modelos empíricos.")

            stat_analysis.empirical_model(data["Total"],
                                          os.path.join("Data", "Represented", "Empirical Model - Total.txt"))

            print("Total construído.")

            stat_analysis.empirical_model(data["SC"],
                                          os.path.join("Data", "Represented", "Empirical Model - SC.txt"))

            print("SC construído.")

            stat_analysis.empirical_model(data["RS"],
                                          os.path.join("Data", "Represented", "Empirical Model - RS.txt"))

            print("RS construído.")

            stat_analysis.empirical_model(data["NAC"],
                                          os.path.join("Data", "Represented", "Empirical Model - NAC.txt"))

            print("NAC construído.")

            stat_analysis.empirical_model(data["OUTR"],
                                          os.path.join("Data", "Represented", "Empirical Model - OUTR.txt"))

            print("OUTR construído.")

            stat_analysis.empirical_model(data["METRO"],
                                          os.path.join("Data", "Represented", "Empirical Model - METRO.txt"))

            print("METRO construído.")

            stat_analysis.empirical_model(data["INT"],
                                          os.path.join("Data", "Represented", "Empirical Model - INT.txt"))

            print("INT construído.")

            print("Concluído.")
        case "histogram" | "h":

            print("Construindo histogramas.")

            stat_analysis.histogram("Total",
                                    "#0000CC",
                                    data["Total"])

            print("Total construído.")

            stat_analysis.histogram("Santa Catarina",
                                    "#0000CC",
                                    data["SC"])

            print("SC construído.")

            stat_analysis.histogram("Rio Grande do Sul",
                                    "#0000CC",
                                    data["RS"])

            print("RS construído.")

            stat_analysis.histogram("Postos nacionais",
                                    "#0000CC",
                                    data["NAC"])

            print("NAC construído.")

            stat_analysis.histogram("Outros postos",
                                    "#0000CC",
                                    data["OUTR"])

            print("OUTR construído.")

            stat_analysis.histogram("Região metropolitana",
                                    "#0000CC",
                                    data["METRO"])

            print("METRO construído.")

            stat_analysis.histogram("Interior",
                                    "#0000CC",
                                    data["INT"])

            print("INT construído.")

            print("Concluído.")
        case "box_plot" | "bp":

            print("Construindo diagramas em caixas")

            stat_analysis.box_plot("Estados", "Santa Catarina", "Rio Grande do Sul", data["SC"], data["RS"])
            print("Estados construídos")

            stat_analysis.box_plot("Postos", "Nacionais", "Outros", data["NAC"], data["OUTR"])
            print("Postos construídos")

            stat_analysis.box_plot("Regiões", "Metropolitanas", "Interior", data["METRO"], data["INT"])
            print("Regiões construídos")

            print("Concluído.")
        case "proportion" | "prop":

            print("Calculando proporções")

            print("SC")
            stat_analysis.average_proportion(data["SC"])
            print("RS")
            stat_analysis.average_proportion(data["RS"])
            print("NAC")
            stat_analysis.average_proportion(data["NAC"])
            print("OUTR")
            stat_analysis.average_proportion(data["OUTR"])
            print("METRO")
            stat_analysis.average_proportion(data["METRO"])
            print("INT")
            stat_analysis.average_proportion(data["INT"])

            print("Concluído.")
        case "proportion2" | "prop2":

            print("Calculando proporções")

            print("SC")
            stat_analysis.above_average_proportion(data["SC"])
            print("RS")
            stat_analysis.above_average_proportion(data["RS"])
            print("NAC")
            stat_analysis.above_average_proportion(data["NAC"])
            print("OUTR")
            stat_analysis.above_average_proportion(data["OUTR"])
            print("METRO")
            stat_analysis.above_average_proportion(data["METRO"])
            print("INT")
            stat_analysis.above_average_proportion(data["INT"])

            print("Concluído.")
        case "empirical_rule" | "emprl":
            print("Checando a regra empírica")

            print("SC")
            stat_analysis.empirical_rule_check(data["SC"], 0.171, 5.303, 1)
            stat_analysis.empirical_rule_check(data["SC"], 0.171, 5.303, 2)
            stat_analysis.empirical_rule_check(data["SC"], 0.171, 5.303, 3)
            print("NAC")
            stat_analysis.empirical_rule_check(data["NAC"], 0.267, 5.364, 1)
            stat_analysis.empirical_rule_check(data["NAC"], 0.267, 5.364, 2)
            stat_analysis.empirical_rule_check(data["NAC"], 0.267, 5.364, 3)
            print("METRO")
            stat_analysis.empirical_rule_check(data["METRO"], 0.173, 5.292, 1)
            stat_analysis.empirical_rule_check(data["METRO"], 0.173, 5.292, 2)
            stat_analysis.empirical_rule_check(data["METRO"], 0.173, 5.292, 3)

            print("Concluído.")
        case _:
            print("Comando não reconhecido.")
