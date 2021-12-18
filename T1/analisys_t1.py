# -*- coding: utf-8 -*-

'''
Trabalho 1 de estatística.

Este programa segue um paradigma funcional.

Python 3.10.
'''

import os
import stat_analysis

print("INE5405 - Trabalho 1 de probabilidade e estatística")

total_values = []
sc_values = []
rs_values = []
nac_values = []
outr_values = []
metro_values = []
int_values = []

while True:

    command = input(">>> ")

    match command:
        case "exit" | 'q':

            print("Saindo.")
            break
        case "csv2json" | "c2j":

            print("Convertendo de csv para json.")

            stat_analysis.csv2json(os.path.join("Data", "Raw", "T1 - Coleta.csv"),
                                   os.path.join("Data", "Processed", "T1 - Coleta.json"))

            print("Concluído.")
        case "process_data":
            stat_analysis.process_data(os.path.join("Data", "Processed", "T1 - Coleta.json"),
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
                    total_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("Total serizalizado.")

                with open(os.path.join("Data", "Processed", "SC.txt"), 'r', encoding="utf-8") as file:
                    sc_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("SC serizalizado.")

                with open(os.path.join("Data", "Processed", "RS.txt"), 'r', encoding="utf-8") as file:
                    rs_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("RS serizalizado.")

                with open(os.path.join("Data", "Processed", "NAC.txt"), 'r', encoding="utf-8") as file:
                    nac_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("NAC serizalizado.")

                with open(os.path.join("Data", "Processed", "OUTR.txt"), 'r', encoding="utf-8") as file:
                    outr_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("OUTR serizalizado.")

                with open(os.path.join("Data", "Processed", "METRO.txt"), 'r', encoding="utf-8") as file:
                    metro_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("METRO serizalizado.")

                with open(os.path.join("Data", "Processed", "INT.txt"), 'r', encoding="utf-8") as file:
                    int_values = list(map(lambda val: float(val.strip()), file.readlines()))

                print("INT serizalizado.")
            except FileNotFoundError:

                print("Os arquivos não existem, lembre-se de processar os dados!")

            print("Concluído.")
        case "stem_and_leaves" | "sl":

            print("Construindo diagramas de ramos e folhas.")

            stat_analysis.stem_and_leaves(total_values,
                                          sc_values,
                                          rs_values,
                                          "Santa Catarina",
                                          "Rio Grande do Sul",
                                          os.path.join("Data", "Represented", "Stem and Leaves - State.txt"))

            print("Diagrama de estados construído.")

            stat_analysis.stem_and_leaves(total_values,
                                          nac_values,
                                          outr_values,
                                          "Nacionais",
                                          "Outros",
                                          os.path.join("Data", "Represented", "Stem and Leaves - Gas Station.txt"))

            print("Diagrama de postos construído.")

            stat_analysis.stem_and_leaves(total_values,
                                          metro_values,
                                          int_values,
                                          "Metropolitanas",
                                          "Interioranas",
                                          os.path.join("Data", "Represented", "Stem and Leaves - Region.txt"))

            print("Diagrama de regiões construído.")

            print("Concluído.")
        case "empirical_model" | "em":

            print("Construindo modelos empíricos.")

            stat_analysis.empirical_model(total_values,
                                          os.path.join("Data", "Represented", "Empirical Model - Total.txt"))

            print("Total construído.")

            stat_analysis.empirical_model(sc_values,
                                          os.path.join("Data", "Represented", "Empirical Model - SC.txt"))

            print("SC construído.")

            stat_analysis.empirical_model(rs_values,
                                          os.path.join("Data", "Represented", "Empirical Model - RS.txt"))

            print("RS construído.")

            stat_analysis.empirical_model(nac_values,
                                          os.path.join("Data", "Represented", "Empirical Model - NAC.txt"))

            print("NAC construído.")

            stat_analysis.empirical_model(outr_values,
                                          os.path.join("Data", "Represented", "Empirical Model - OUTR.txt"))

            print("OUTR construído.")

            stat_analysis.empirical_model(metro_values,
                                          os.path.join("Data", "Represented", "Empirical Model - METRO.txt"))

            print("METRO construído.")

            stat_analysis.empirical_model(int_values,
                                          os.path.join("Data", "Represented", "Empirical Model - INT.txt"))

            print("INT construído.")

            print("Concluído.")
        case "histogram" | "h":

            print("Construindo histogramas.")

            stat_analysis.histogram("Total",
                                    "#0000CC",
                                    total_values)

            print("Total construído.")

            stat_analysis.histogram("Santa Catarina",
                                    "#0000CC",
                                    sc_values)

            print("SC construído.")

            stat_analysis.histogram("Rio Grande do Sul",
                                    "#0000CC",
                                    rs_values)

            print("RS construído.")

            stat_analysis.histogram("Postos nacionais",
                                    "#0000CC",
                                    nac_values)

            print("NAC construído.")

            stat_analysis.histogram("Outros postos",
                                    "#0000CC",
                                    outr_values)

            print("OUTR construído.")

            stat_analysis.histogram("Região metropolitana",
                                    "#0000CC",
                                    metro_values)

            print("METRO construído.")

            stat_analysis.histogram("Interior",
                                    "#0000CC",
                                    int_values)

            print("INT construído.")

            print("Concluído.")
        case "box_plot" | "bp":

            print("Construindo diagramas em caixas")

            stat_analysis.box_plot("Estados", "Santa Catarina", "Rio Grande do Sul", sc_values, rs_values)
            print("Estados construídos")

            stat_analysis.box_plot("Postos", "Nacionais", "Outros", nac_values, outr_values)
            print("Postos construídos")

            stat_analysis.box_plot("Regiões", "Metropolitanas", "Interior", metro_values, int_values)
            print("Regiões construídos")

            print("Concluído.")
        case _:
            print("Comando não reconhecido.")
