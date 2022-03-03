import sys
import time
from datetime import datetime
import pandas as pd
import seaborn as sns
import collections
import matplotlib.pyplot as plt
import numpy as np

def main():
    if len(sys.argv) < 3 and len(sys.argv) >= 2:
        df = pd.read_csv(sys.argv[1])
        setup(df)
    else:
        print("No logfile specified, exiting...")
        time.sleep(2)
        exit(0)

def setup(df):
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
    
    fig, ax = plt.subplots(figsize=(9, 7))
    time_field, time_field_list = get_field(df, "Time")
    x = [datetime.strptime(i, "%S.%f").second for i in time_field_list[1:]]
    engine_field, engine_field_list = get_field(df, "EngineRPM")
    y = engine_field_list[1:].astype(float)
    d = {'Time': x, 'Engine RPM': y}
    temp_df = pd.DataFrame(d)
    sns.set_style("darkgrid")
    sns.lineplot(x='Time', y='Engine RPM', data=temp_df)
    ax.set_xlim(0, int(float(max(time_field_list, key = float))) - 1)
    ax.set_xticks(range(0, int(float(max(time_field_list, key = float)))))
    plt.show()

    fig, axs = plt.subplots(2, 2, figsize=(9, 7))
    time_field, time_field_list = get_field(df, "Time")
    x = [datetime.strptime(i, "%S.%f") for i in time_field_list[1:]]
    engine_field, engine_field_list = get_field(df, "EngineRPM")
    y1 = engine_field_list[1:].astype(float)
    axs[0, 0].plot(x, y1)
    axs[0, 0].set(xlabel='', ylabel='Engine RPM\n')
    axs[0, 0].set_xticklabels([])
    tia_field, tia_field_list = get_field(df, "tia")
    y2 = tia_field_list[1:].astype(float)
    axs[0, 1].plot(x, y2, 'tab:orange')
    axs[0, 1].set(xlabel='', ylabel='Intake Air Temp')
    axs[0, 1].set_xticklabels([])
    map_field, map_field_list = get_field(df, "map_mes")
    y3 = map_field_list[1:].astype(float)
    axs[1, 0].plot(x, y3, 'tab:green')
    axs[1, 0].set(xlabel='', ylabel='Boost\n')
    axs[1, 0].set_xticklabels([])
    timing_advance_field, timing_advance_field_list = get_field(df, "IgnitionTimingAdvancefor#1Cylinder")
    y4 = timing_advance_field_list[1:].astype(float)
    axs[1, 1].plot(x, y4, 'tab:red')
    axs[1, 1].set(xlabel='', ylabel='Timing Advance')
    axs[1, 1].set_xticklabels([])
    plt.show()

    #for field in air_fields:
    #    found_field, found_field_list = get_field(df, field)
    #    print_field(found_field, field)

def get_field(df, field):
    for i, (columnName, columnData) in enumerate(df.iteritems()):
        columnName = str(columnName).replace(" ", "")
        columnName = columnName.replace('"', "")
        if str(columnName) == str(field):
            print("* Found field: [" + str(i) + "] " + str(columnName))
            field = columnData.values[2:]
            field_list = str(field).replace(" ", ", ")
            field_list = str(field_list).replace("'", "")
            field_list = str(field_list).replace("\n", "")
            field_list = field_list.strip('][').split(', ')
            field_list = np.array(field_list)
            return field, field_list
    return "ERROR"

def print_field(column, field):
    print("* Printing field: " + str(field))
    col_length = len(column)
    for val in range(0, col_length):
        print("  {:<7} {:<25} {}".format("", column[val], field))
        #time.sleep(0.0025)

def print_all_fields(df):
    print()
    print("{:<5}\n".format("[ALL LOGGING FIELDS]"))
    columns = collections.defaultdict(list)
    for i, (columnName, columnData) in enumerate(df.iteritems()):
        columnName = str(columnName).replace(" ", "")
        columnName = columnName.replace('"', "")
        print("{:<5} {}".format("[" + str(i) + "]", columnName))
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
        input("{:<5} {} {}".format("[" + str(j) + "]", name, "(" + current + ")"))
        print()
        for val in range(2, col_length):
            print("{:<7} {:<25} {}".format("", col[0][val], name))
            time.sleep(0.0025)
    print()
    print("[DONE]")
    print()

if __name__ == "__main__":
    main()
