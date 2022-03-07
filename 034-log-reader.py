import sys
import time
from datetime import datetime
import pandas as pd
import seaborn as sns
import collections
import matplotlib.pyplot as plt
import numpy as np
from colorama import init, Fore, Back, Style

sns.set_style("darkgrid")
init(autoreset=False)

all_logging_fields = [
       "Time",
       "Milliseconds",
       "tia",
       "TIA_AM_SCHA",
       "tqi_gs_fast_dec",
       "tqi_gs_fast_inc",
       "pv_av",
       "LAMB_LS_UP[1]",
       "LAMB_LS_UP[2]",
       "state_eng",
       "teg_dyn_up_cat[1]",
       "TEG_DYN_UP_CAT[2]",
       "fup",
       "fup_sp",
       "pump_vol_vcv",
       "efppwm",
       "fup_efp",
       "iga_av_mv",
       "TI_1_HOM[0]",
       "TI_1_HOM[3]",
       "amp_mes",
       "map",
       "map_mes",
       "map_1_mes",
       "map_2_mes",
       "pdt_mes",
       "maf",
       "iga_ad_1_knk[0]",
       "iga_ad_1_knk[1]",
       "iga_ad_1_knk[2]",
       "iga_ad_1_knk[3]",
       "iga_ad_1_knk[4]",
       "iga_ad_1_knk[5]",
       "lamb_sp[1]",
       "LAMB_SP[2]",
       "tqi_av",
       "gear",
       "vs",
       "CAM_SP_IVVT_IN",
       "map_sp",
       "rfp_sp",
       "ShortTermFuelTrim-Bank1",
       "LongTermFuelTrim-Bank1",
       "ShortTermFuelTrim-Bank2",
       "LongTermFuelTrim-Bank2",
       "EngineRPM",
       "IgnitionTimingAdvancefor#1Cylinder",
       "Ambientairtemperature",
       "CommandedThrottleActuatorControl"
    ]

fuel_fields = [
    "Time",
    "Milliseconds",
    "fup",
    "fup_sp",
    "pump_vol_vcv",
    "efppwm",
    "fup_efp",
    "ShortTermFuelTrim-Bank1",
    "LongTermFuelTrim-Bank1",
    "ShortTermFuelTrim-Bank2",
    "LongTermFuelTrim-Bank2",
    "EngineRPM",
    "CommandedThrottleActuatorControl"
]

air_fields = [
    "Time",
    "Milliseconds",
    "tia",
    "TIA_AM_SCHA",
    "tqi_gs_fast_dec",
    "tqi_gs_fast_inc",
    "pv_av",
    "LAMB_LS_UP[1]",
    "LAMB_LS_UP[2]",
    "state_eng",
    "teg_dyn_up_cat[1]",
    "TEG_DYN_UP_CAT[2]",
    "amp_mes",
    "map",
    "map_mes",
    "map_1_mes",
    "map_2_mes",
    "pdt_mes",
    "maf",
    "lamb_sp[1]",
    "LAMB_SP[2]",
    "tqi_av",
    "gear",
    "vs",
    "CAM_SP_IVVT_IN",
    "map_sp",
    "rfp_sp",
    "EngineRPM",
    "Ambientairtemperature",
    "CommandedThrottleActuatorControl"
]

ignition_fields = [
        "Time",
        "Milliseconds",
        "tia",
        "TI_1_HOM[0]",
        "TI_1_HOM[3]",
        "iga_ad_1_knk[0]",
        "iga_ad_1_knk[1]",
        "iga_ad_1_knk[2]",
        "iga_ad_1_knk[3]",
        "iga_ad_1_knk[4]",
        "iga_ad_1_knk[5]",
        "EngineRPM",
        "IgnitionTimingAdvancefor#1Cylinder",
        "CommandedThrottleActuatorControl"
    ]

def main():
    if len(sys.argv) < 3 and len(sys.argv) >= 2:
        try:
            df = pd.read_csv(sys.argv[1])
        except Exception:
            input(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "\nError loading logfile, press enter to exit...")
            print()
            exit(0)
        loop(df)
    else:
        input(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "\nNo logfile specified, press enter to exit...")
        print()
        exit(0)

def loop(df):
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + " ______________________")
    print("|                      |")
    print("| 034 Log Reader Shell |")
    print("|______________________|")
    while True:
        found_field = ""
        found_field_list = ""
        prompt_input = input("\n[S] SEARCH [P] PRINT [G] GRAPH [A] PRINT ALL : ")
        if prompt_input.lower() == "s":
            search_fields(df)
            continue
        if prompt_input.lower() == "p":
            print_fields(df)
            continue
        if prompt_input.lower() == "g":
            graph_fields(df)
            continue
        if prompt_input.lower() == "a":
            print_all(df)
            continue
        print("\nCommand not found...")
    
def search_fields(df):
    print("\n ---------------")
    print("| SEARCH FIELDS |")
    print(" ---------------\n")
    print_all_fields(df)
    found_field = ""
    found_field_list = ""
    prompt_input = ""
    while True:
        prompt_input = input("\nENTER FIELD INDEX : ")
        if len(prompt_input) == 0:
            print("\nInvalid index...")
            continue
        try:
            int_input = int(prompt_input)
        except Exception:
            print("\nInvalid index...")
            continue
        if int(prompt_input) > 48 or int(prompt_input) < 0:
            print("\nInvalid index...")
            continue
        else:
            break
    for x, field in enumerate(all_logging_fields):
        try:
            if int(prompt_input) == x:
                found_field, found_field_list, found_field_str = get_field(df, field)
                if len(found_field_list) == 0:
                    print("\nInvalid index...")
                while True:
                    op = input("\n" + found_field_str.strip() + " - [P] PRINT [G] GRAPH : ")
                    if op:
                        if op == 'p' or op == 'P':
                            print_field(found_field, field)
                            break
                        if op == 'g' or op == 'G':
                            graph_field(df, field, found_field_list)
                            break
                    print("\nCommand not found....\n")
        except Exception:
            prompt_input = prompt_input
    return

def print_fields(df):
    print("\n --------------")
    print("| PRINT FIELDS |")
    print(" --------------\n")
    print_all_fields(df)
    found_field_list = ""
    while True:
        prompt_input = input("\nENTER FIELD INDICES (COMMA SEPARATED) : ")
        prompt_input = prompt_input.replace(" ", "")
        prompt_input = [int(x) for x in prompt_input.split(',') if x.strip().isdigit()]
        print()
        if len(prompt_input) == 0:
            print("Invalid indices...")
            continue
        if int(max(prompt_input, key = int)) > 48 or int(max(prompt_input, key = int)) < 0:
            print("Invalid indices...")
            continue
        field_names = []
        field_nums = []
        print_fields = []
        for prompt_field in prompt_input:
            for x, field in enumerate(all_logging_fields):
                try:
                    if int(prompt_field) == x:
                        found_field, found_field_list, found_field_str = get_field(df, field)
                        field_names.append(field)
                        field_nums.append(x)
                        print_fields.append(found_field_list)
                except Exception:
                    prompt_input = prompt_input
        for x, num in enumerate(field_nums):
            print("{:<15} {}".format("[" + str(num) + "]", str(field_names[x])))
        print()
        header = ""
        for num in field_nums:
            header += "[{:<15}".format(str(num) + "]")
        print(header + "\n")
        for i in range(len(print_fields[0])):
            printout = ""
            for j in range(len(print_fields)):
                printout += "{:<15} ".format(np.array(print_fields[j])[i])
            print(printout)
        return

def graph_fields(df):
    print("\n --------------")
    print("| GRAPH FIELDS |")
    print(" --------------\n")
    print_all_fields(df)
    found_field_list = ""
    while True:
        prompt_input = input("\nENTER FIELD INDICES (COMMA SEPARATED) : ")
        prompt_input = prompt_input.replace(" ", "")
        prompt_input = [int(x) for x in prompt_input.split(',') if x.strip().isdigit()]
        print()
        if len(prompt_input) == 0:
            print("Invalid indices...")
            continue
        if int(max(prompt_input, key = int)) > 48 or int(max(prompt_input, key = int)) < 0:
            print("Invalid indices...")
            continue
        field_names = []
        field_nums = []
        print_fields = []
        for prompt_field in prompt_input:
            for x, field in enumerate(all_logging_fields):
                try:
                    if int(prompt_field) == x:
                        found_field, found_field_list, found_field_str = get_field(df, field)
                        field_names.append(field)
                        field_nums.append(x)
                        print_fields.append(found_field_list)
                except Exception:
                    prompt_input = prompt_input
        for x, num in enumerate(field_nums):
            print("{:<15} {}".format("[" + str(num) + "]", str(field_names[x])))
        graph_multiple_fields(df, field_names, print_fields)
        return

def print_all(df):
    print("\n ------------------")
    print("| PRINT ALL FIELDS |")
    print(" ------------------\n")
    print_all_data(df)

def graph_multiple_fields(df, field_names, field_lists):
    for i in range(len(field_lists)):
        graph_field(df, field_names[i], field_lists[i])

def graph_field(df, field_name, field_list):
    fig, ax = plt.subplots(figsize=(10, 8))
    time_field, time_field_list, time_field_str = get_field(df, "Time")
    x = [datetime.strptime(i, "%S.%f").second for i in time_field_list[1:]]
    y = field_list[1:].astype(float)
    d = {'\nTime': x, field_name + '\n': y}
    temp_df = pd.DataFrame(d)
    sns.lineplot(x='\nTime', y=field_name + '\n', data=temp_df)
    ax.set_xlim(0, int(float(max(time_field_list, key = float))) - 1)
    ax.set_xticks(range(0, int(float(max(time_field_list, key = float)))))
    plt.show()

def get_field(df, field):
    for i, (columnName, columnData) in enumerate(df.iteritems()):
        columnName = str(columnName).replace(" ", "")
        columnName = columnName.replace('"', "")
        if str(columnName) == str(field):
            found_field_str = "\n[" + str(i) + "] " + str(columnName).upper() + "\n"
            field = columnData.values[2:]
            field_list = str(field).replace(" ", ", ")
            field_list = str(field_list).replace("'", "")
            field_list = str(field_list).replace("\n", "")
            field_list = field_list.strip('][').split(', ')
            field_list = np.array(field_list)
            return field, field_list, found_field_str

def print_field(column):
    print()
    col_length = len(column)
    for val in range(0, col_length):
        print(column[val])

def print_all_fields(df):
    columns = collections.defaultdict(list)
    for i, (columnName, columnData) in enumerate(df.iteritems()):
        columnName = str(columnName).replace(" ", "")
        columnName = columnName.replace('"', "")
        print("{:<15} {}".format("[" + str(i) + "]", columnName))
        columns[columnName].append(columnData.values)

def print_all_data(df):
    columns = collections.defaultdict(list)
    for i, (columnName, columnData) in enumerate(df.iteritems()):
        columnName = str(columnName).replace(" ", "")
        columnName = columnName.replace('"', "")
        print("{:<15} {}".format("[" + str(i) + "]", columnName))
        columns[columnName].append(columnData.values)
    for j, col in enumerate(columns.items()):
        name = str(col[0]).upper()
        current = ""
        col = columns.get(col[0])
        col_length = len(col[0])
        for val in range(0, 2):
            val = str(col[0][val]).replace(" ", "")
            if val:
                current += val + ", "
        current = current[:-2]
        print()
        input("{} {} {} {}".format("[" + str(j) + "]", name, "(" + current + ")", ": PRESS ENTER"))
        print()
        for val in range(2, col_length):
            print("{:<7} {:<25} {}".format("", col[0][val], name))
            time.sleep(0.0015)
    print()
    print("[DONE]")
    print()

if __name__ == "__main__":
    main()
