import pandas as pd
import numpy as np
import datetime
import sys
sys.path.append(".")
sys.path.insert(1, '/nas/asallard/BN/Data')
import impute_mun_type as imt

mzpath = "/nas/ivtmatsim/scenarios/switzerland/data/microcensus/"
outputpath = "/nas/asallard/BN/Data/2015/data/"

hhl = pd.read_csv(mzpath + "haushalte.csv", encoding = "latin1")
persons = pd.read_csv(mzpath + "haushaltspersonen.csv", encoding = "latin1")
targets = pd.read_csv(mzpath + "zielpersonen.csv", encoding = "latin1", sep = ",")
wege = pd.read_csv(mzpath + "wege.csv", encoding = "latin1")
steps = pd.read_csv(mzpath + "etappen.csv", encoding = "latin1")

USE_DETAILED_ACTIVITIES = False

hhl = hhl.rename(columns = {
        "HHNR": "Household_id",
        "WM": "Household_weight",
        "W_X_CH1903": "home_x",
        "W_Y_CH1903": "home_y",
        "W_SPRACHE": "home_language",
        "W_KANTON": "home_canton",
        "hhtyp": "household_type",
        "hhgr": "household_size",
        "f30100": "number_of_cars",
        "f31200": "number_of_motorcycles1",
        "f31900": "number_of_motorcycles2",
        "f32100": "number_of_motorcycles3",
        "F20601": "household_income",
        "f32200a": "number_of_bikes1",
        "f32200b": "number_of_bikes2",
        "f32200c": "number_of_bikes3"
        })

hhl = hhl[["Household_id", "Household_weight", "home_x", "home_y",
           "home_language", "home_canton", "household_type", "household_size",
           "number_of_cars", "number_of_motorcycles1", "number_of_motorcycles2",
           "number_of_motorcycles3","number_of_bikes1", "number_of_bikes2",
           "number_of_bikes3", "household_income"]]

hhl["household_size_class"] = np.minimum(5, hhl["household_size"]) - 1

hhl = imt.impute_everything(hhl)

hhl["number_of_cars"] = np.maximum(0, hhl["number_of_cars"])

hhl["number_of_motorcycles"] = [m1 + m2 + m3 for m1, m2, m3 in 
   list(zip(hhl["number_of_motorcycles1"].values.tolist(), hhl["number_of_motorcycles2"].values.tolist(),
            hhl["number_of_motorcycles3"].values.tolist()))]

hhl["number_of_bikes"] = [m1 + m2 + m3 for m1, m2, m3 in 
   list(zip(hhl["number_of_bikes1"].values.tolist(), hhl["number_of_bikes2"].values.tolist(),
            hhl["number_of_bikes3"].values.tolist()))]
   
del hhl["number_of_motorcycles1"]
del hhl["number_of_motorcycles2"]
del hhl["number_of_motorcycles3"]
del hhl["number_of_bikes1"]
del hhl["number_of_bikes2"]
del hhl["number_of_bikes3"]

languagedic = {1: "German", 2: "French", 3: "Italian", 4: "Romansh", -97: "NA"}

hhl["language"] = [languagedic[i] for i in hhl["home_language"]]

del hhl["home_language"]

cantons = {-97:"NA",	
1:	"Zürich",
2:	"Bern",
3:	"Luzern",
4:	"Uri",
5:	"Schwyz",
6:	"Obwalden",
7:	"Nidwalden",
8:	"Glarus",
9:	"Zug",
10:	"Fribourg",
11:	"Solothurn",
12:	"Basel-Stadt",
13:	"Basel-Land",
14:	"Schaffhausen",
15:	"Appenzell Ausserrhoden",
16:	"Appenzell Innerrhoden",
17:	"St. Gallen",
18:	"Graubünden",
19:	"Aargau",
20:	"Thurgau",
21:	"Ticino",
22:	"Vaud",
23:	"Valais",
24:	"Neuchâtel",
25:	"Genève",
26:	"Jura"}

hhl["canton"] = [cantons[i] for i in hhl["home_canton"]]

del hhl["home_canton"]

diff_hhl = {10: "Single", 
            30: "Non family", 
            210: "Couple without kids", 
            220: "Couple with kids",
            230: "Single parent", 
            -97: "Others", -99:"Others", -98:"Others"}

hhl["hhtype"] = [diff_hhl[i] for i in hhl["household_type"]]

del hhl["household_type"]

hhl["nb_cars"] = hhl["number_of_cars"]
hhl["nb_motorcycles"] = hhl["number_of_motorcycles"]
hhl["nb_bikes"] = hhl["number_of_bikes"]
hhl.loc[hhl["number_of_cars"] < pd.Series([0 for i in range(len(hhl))]), "nb_cars"] = "NA"
hhl.loc[hhl["number_of_motorcycles"] < pd.Series([0 for i in range(len(hhl))]), "nb_motorcycles"] = "NA"
del hhl["number_of_cars"]
del hhl["number_of_motorcycles"]

inchhl = {-99: "NA",
          -97: "NA",
          -98: "NA",
1:	"< 2000 CHF",
2:	"2000 - 4000 CHF",
3:	"4001 - 6000 CHF",
4:	"6001 - 8000 CHF",
5:	"8001 - 10000 CHF",
6:	"10001 - 12000 CHF",
7:	"12001 - 14000 CHF",
8:	"14001 - 16000 CHF",
9:	"16000 + CHF"}

hhl["hhl_income"] = [inchhl[i] for i in hhl["household_income"]]
del hhl["household_income"]

hhl.to_csv(outputpath + "households0109.csv",  index = False)

persons = persons.rename(columns = {
        "HHNR": "Household_id",
        "WM": "Household_weight",
        "HPNR": "Person_id",
        "alter": "Age",
        "gesl": "Gender",
        "f20400a": "Driving_license_car",
        "f20400b": "Driving_license_motorcycle"
        })

sexdic = {1: "Male", 2: "Female", -98: "NA"}

persons["Sex"] = [sexdic[i] for i in persons["Gender"].values.tolist()]
del persons["Gender"]

persons["License_car"] = [None for i in range(len(persons))]
persons["License_motorcycle"] = [None for i in range(len(persons))]
persons.loc[persons["Driving_license_car"] == pd.Series([1 for i in range(len(persons))]), "License_car"] = "Yes"
persons.loc[persons["Driving_license_car"] == pd.Series([2 for i in range(len(persons))]), "License_car"] = "No"
persons.loc[persons["Driving_license_car"] <= pd.Series([0 for i in range(len(persons))]), "License_car"] = "NA"
persons.loc[persons["Driving_license_motorcycle"] == pd.Series([1 for i in range(len(persons))]), "License_motorcycle"] = "Yes"
persons.loc[persons["Driving_license_motorcycle"] == pd.Series([2 for i in range(len(persons))]), "License_motorcycle"] = "No"
persons.loc[persons["Driving_license_motorcycle"] <= pd.Series([0 for i in range(len(persons))]), "License_motorcycle"] = "NA"

del persons["Driving_license_motorcycle"]
del persons["Driving_license_car"]

persons.to_csv(outputpath + "persons0109.csv",  index = False)

targets = targets.rename(columns = {
        "HHNR": "Household_id",
        "WP": "Person_weight",
        "alter": "Age",
        "gesl": "Gender",
        "sprache": "language",
        "tag": "day_of_week",
        "f20400a": "Driving_license_car",
        "f20400b": "Driving_license_motorcycle",
        "f40900": "Employed_time",
        "f40800_01": "Employed",
        "f41001a": "Unemployed_status",
        "f81300": "Home office",
        "f41610a": "Abonments_GA",
        "f41610c": "Abonments_Verbund",
        "f41610d": "Abonments_Strecken",
        "f41610f": "Abonments_Junior",
        "f41610g": "Abonments_other",
        "f41610b": "Abonments_Halbtax",
        "f41610e": "Abonments_Gleis7",
        "f42100a": "Availability_bicycle",
        "f42100b": "Availability_motorcycle1",
        "f42100c": "Availability_motorcycle2",
        "f42100d": "Availability_motorcycle3",
        "f42100e": "Availability_car",
        })

targets = targets[["Household_id",
       "Person_weight",
        "Age",
        "Gender",
        "language",
        "day_of_week",
        "Driving_license_car",
        "Driving_license_motorcycle",
        "Employed_time",
        "Employed",
        "Unemployed_status",
        "Home office",
        "Abonments_GA",
        "Abonments_Verbund",
        "Abonments_Strecken",
        "Abonments_Junior",
        "Abonments_other",
        "Abonments_Halbtax",
        "Abonments_Gleis7",
        "Availability_bicycle",
        "Availability_motorcycle1",
        "Availability_motorcycle2",
        "Availability_motorcycle3",
        "Availability_car",
        "zivil"]]

targets["PT_subscription"] = ["No" for i in range(len(targets))]
targets.loc[targets["Abonments_GA"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"
targets.loc[targets["Abonments_Verbund"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"
targets.loc[targets["Abonments_Strecken"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"
targets.loc[targets["Abonments_Junior"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"
targets.loc[targets["Abonments_Halbtax"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"
targets.loc[targets["Abonments_Gleis7"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"
targets.loc[targets["Abonments_other"] == pd.Series([1 for i in range(len(targets))]), "PT_subscription"] = "Yes"

targets.loc[targets["Age"] < pd.Series([15 for i in range(len(targets))]), "Employment_status"] = "Student"
targets.loc[targets["Unemployed_status"] == pd.Series([21 for i in range(len(targets))]), "Employment_status"] = "Unemployed"
targets.loc[targets["Unemployed_status"] == pd.Series([22 for i in range(len(targets))]), "Employment_status"] = "Unemployed"
targets.loc[targets["Unemployed_status"] == pd.Series([32 for i in range(len(targets))]), "Employment_status"] = "Student"
targets.loc[targets["Unemployed_status"] == pd.Series([33 for i in range(len(targets))]), "Employment_status"] = "Houseperson"
targets.loc[targets["Unemployed_status"] == pd.Series([34 for i in range(len(targets))]), "Employment_status"] = "Retired"
targets.loc[targets["Unemployed_status"] == pd.Series([35 for i in range(len(targets))]), "Employment_status"] = "Disabled"
targets.loc[targets["Unemployed_status"] == pd.Series([36 for i in range(len(targets))]), "Employment_status"] = "Military/civil service"
targets.loc[targets["Unemployed_status"] == pd.Series([95 for i in range(len(targets))]), "Employment_status"] = "Unemployed"
targets.loc[targets["Employed"] > pd.Series([0 for i in range(len(targets))]), "Employment_status"] = "Employed"
targets.loc[targets["Employed_time"] == pd.Series([1 for i in range(len(targets))]), "Work_time"] = "Full time"
targets.loc[targets["Employed_time"] == pd.Series([2 for i in range(len(targets))]), "Work_time"] = "Half time"
targets.loc[targets["Employed_time"] == pd.Series([3 for i in range(len(targets))]), "Work_time"] = "More than half time"
targets.loc[targets["Employed_time"] < pd.Series([0 for i in range(len(targets))]), "Work_time"] = "Unemployed"

targets["Sex"] = [None for i in range(len(targets))]
targets["Language"] = [None for i in range(len(targets))]
targets.loc[targets["Gender"] == pd.Series([1 for i in range(len(targets))]), "Sex"] = "Male"
targets.loc[targets["Gender"] == pd.Series([2 for i in range(len(targets))]), "Sex"] = "Female"
targets.loc[targets["Gender"] == pd.Series([-98 for i in range(len(targets))]), "Sex"] = "NA"

targets.loc[targets["language"] == pd.Series([1 for i in range(len(targets))]), "Language"] = "German"
targets.loc[targets["language"] == pd.Series([2 for i in range(len(targets))]), "Language"] = "French"
targets.loc[targets["language"] == pd.Series([3 for i in range(len(targets))]), "Language"] = "Italian"
targets.loc[targets["language"] == pd.Series([4 for i in range(len(targets))]), "Language"] = "Romansh"
targets.loc[targets["language"] == pd.Series([-97 for i in range(len(targets))]), "Language"] = "NA"

targets["License_car"] = [None for i in range(len(targets))]
targets["License_motorcycle"] = [None for i in range(len(targets))]
targets.loc[targets["Driving_license_car"] == pd.Series([1 for i in range(len(targets))]), "License_car"] = "Yes"
targets.loc[targets["Driving_license_car"] == pd.Series([2 for i in range(len(targets))]), "License_car"] = "No"
targets.loc[targets["Driving_license_car"] <= pd.Series([0 for i in range(len(targets))]), "License_car"] = "NA"
targets.loc[targets["Driving_license_motorcycle"] == pd.Series([1 for i in range(len(targets))]), "License_motorcycle"] = "Yes"
targets.loc[targets["Driving_license_motorcycle"] == pd.Series([2 for i in range(len(targets))]), "License_motorcycle"] = "No"
targets.loc[targets["Driving_license_motorcycle"] <= pd.Series([0 for i in range(len(targets))]), "License_motorcycle"] = "NA"

del targets["Driving_license_motorcycle"]
del targets["Driving_license_car"]

week = {1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"}
targets["Week_day"] = [week[i] for i in targets["day_of_week"]]

targets["Work_from_home"] = [None for i in range(len(targets))]
targets.loc[targets["Home office"] == pd.Series([1 for i in range(len(targets))]), "Work_from_home"] = "Yes"
targets.loc[targets["Home office"] == pd.Series([2 for i in range(len(targets))]), "Work_from_home"] = "Sometimes"
targets.loc[targets["Home office"] == pd.Series([3 for i in range(len(targets))]), "Work_from_home"] = "No"
targets.loc[targets["Home office"] <= pd.Series([0 for i in range(len(targets))]), "Work_from_home"] = "NA"

targets["Bicycle_available"] = [None for i in range(len(targets))]
targets.loc[targets["Availability_bicycle"] <= pd.Series([0 for i in range(len(targets))]), "Bicycle_available"] = "NA"
targets.loc[targets["Availability_bicycle"] == pd.Series([1 for i in range(len(targets))]), "Bicycle_available"] = "Always"
targets.loc[targets["Availability_bicycle"] == pd.Series([2 for i in range(len(targets))]), "Bicycle_available"] = "Sometimes"
targets.loc[targets["Availability_bicycle"] == pd.Series([3 for i in range(len(targets))]), "Bicycle_available"] = "Never"

targets["Car_available"] = [None for i in range(len(targets))]
targets.loc[targets["Availability_car"] <= pd.Series([0 for i in range(len(targets))]), "Car_available"] = "NA"
targets.loc[targets["Availability_car"] == pd.Series([1 for i in range(len(targets))]), "Car_available"] = "Always"
targets.loc[targets["Availability_car"] == pd.Series([2 for i in range(len(targets))]), "Car_available"] = "Sometimes"
targets.loc[targets["Availability_car"] == pd.Series([3 for i in range(len(targets))]), "Car_available"] = "Never"


motorcycles = pd.Series(np.maximum(targets["Availability_motorcycle1"].values.tolist(), np.maximum( targets["Availability_motorcycle2"].values.tolist(),
                     targets["Availability_motorcycle3"].values)))
targets["Motorcycle_available"] = [None for i in range(len(targets))]
targets.loc[motorcycles <= pd.Series([0 for i in range(len(targets))]), "Motorcycle_available"] = "NA"
targets.loc[motorcycles == pd.Series([1 for i in range(len(targets))]), "Motorcycle_available"] = "Always"
targets.loc[motorcycles == pd.Series([2 for i in range(len(targets))]), "Motorcycle_available"] = "Sometimes"
targets.loc[motorcycles == pd.Series([3 for i in range(len(targets))]), "Motorcycle_available"] = "Never"

targets["Marital_status"] = [None for i in range(len(targets))]
targets.loc[targets["zivil"] == 1, "Marital_status"] = 0
targets.loc[targets["zivil"] == 2, "Marital_status"] = 1
targets.loc[targets["zivil"] == 3, "Marital_status"] = 2
targets.loc[targets["zivil"] == 4, "Marital_status"] = 2
targets.loc[targets["zivil"] == 5, "Marital_status"] = 0
targets.loc[targets["zivil"] == 6, "Marital_status"] = 1
targets.loc[targets["zivil"] == 7, "Marital_status"] = 2

targets["age_class"] = np.digitize(targets["Age"], range(6,100,3))
#targets["age_class"] = np.digitize(targets["Age"], [6, 18, 24, 30, 45, 65, 80])

for name_col in ["Abonments_GA",
        "Abonments_Verbund",
        "Abonments_Strecken",
        "Abonments_Junior",
        "Abonments_other",
        "Abonments_Halbtax", "Employed_time",
        "Abonments_Gleis7", "Unemployed_status", "Employed", "Gender", "language",
        "Availability_motorcycle1", "Availability_motorcycle2", "Availability_motorcycle3",
        "Home office", "Availability_car", "Availability_bicycle", "day_of_week"]:
    del targets[name_col]

targets.to_csv(outputpath + "target_persons0109.csv", index = False)


wege = wege.rename(columns = {
        "HHNR": "Household_id",
        "WP": "Person_weight",
        "WEGNR": "Trip_id",
        "f51100": "Departure_time",
        "f51400": "Arrival_time",
        "f51700_weg": "Leisure activity type",
        "f51800a": "Shopping1",
        "wzweck1": "Trip purpose",
        "wzweck2": "Trip back home",
        "w_rdist": "Distance",
        "wmittel": "mode",
        "W_X_CH1903": "home_x",
        "W_Y_CH1903": "home_y",
        "S_X_CH1903": "origin_x",
        "S_Y_CH1903": "origin_y"
        })

modes = {
        -99: "unknown",
        1: "pt",
        2: "pt",
        3: "pt",
        4: "pt",
        5: "pt",
        6: "pt",
        7: "pt",
        8: "pt",
        9: "car",
        10: "car",
        11: "pt",
        12: "car",
        13: "car",
        14: "bike",
        15: "walk",
        16: "car",
        17: "unknown",
}
    
activities = {
        1: "Connection",
        2: "Work",
        3: "Education",
        4: "Shopping",
        5: "Other",
        6: "Work",
        7: "Work",
        8: "Leisure",
        9: "Other",
        10: "Other",
        11: "Home",
        12: "unknown",
        13: "Crossing borders",
        -99: "unknown",
        -98: "unknown",
        -97: "unknown"
    }   

leisure = {
       1: "Visits",
       2: "Gastronomy",
       3: "Active sport", 
       4: "Hiking", 
       5: "Biking", 
       6: "Passive sport",
       7: "Outdoor diverse",
       8: "WellFit",
       9: "Culture, recreation",
       10: "Unpaid work", 
       11: "Association activity", 
       12: "Excursion",
       13: "Religion",
       14: "Domestic leisure",
       15: "Picnic", 
       16: "Shopping(L)", 
       17: "Tour",  
       18: "L-Other", 
       22: "Several purposes", 
       -99: "L-Other",
       -98: "L-Other",
       -97: "L-Other"
   }

shopping = {
        1: "Grocery",
        2: "Other consumption",
        3: "Investment goods",
        4: "Leisure(S)",
        5: "S-Other",
        -99: "S-Other",
        -98: "S-Other",
        -97: "S-Other"
    }

wege["Mode"] = [modes[i] for i in wege["mode"].values.tolist()]
wege["mode_detailed"] = wege["mode"]
wege.loc[wege["mode"] == 1, "mode_detailed"] = "plane"
wege.loc[wege["mode"] == 11, "mode_detailed"] = "taxi"

steps["is_car_passenger"] = steps["f51300"] == 0
df_passengers = steps[["HHNR", "WEGNR", "is_car_passenger"]].groupby(["HHNR", "WEGNR"]).sum().reset_index()
df_passengers.columns = ["Household_id", "Trip_id", "is_car_passenger" ]
wege = pd.merge(wege, df_passengers, on = ["Household_id", "Trip_id"], how = "left")
wege.loc[wege["is_car_passenger"] > 0, "mode_detailed"] = "car_passenger"
wege.loc[wege["is_car_passenger"] > 0, "mode"] = "car_passenger"
del wege["is_car_passenger"]


wege["Purpose"] = [activities[i] for i in wege["Trip purpose"].values.tolist()]
wege.loc[wege["Trip back home"] >= pd.Series([2 for i in range(len(wege))]), "Purpose"] = "Home"

if USE_DETAILED_ACTIVITIES:
    wege.loc[wege["Trip purpose"] == pd.Series([4 for i in range(len(wege))]).reset_index(drop=True) ,
         "Purpose"] = pd.Series([shopping[i] for i in wege["Shopping1"].values.tolist()]).reset_index(drop=True)


    wege.loc[wege["Trip purpose"] == pd.Series([8 for i in range(len(wege))]),
         "Purpose"] = pd.Series([leisure[i] for i in wege["Leisure activity type"].values.tolist()])

#wege = wege[wege["Trip back home"] != 3]

wege.loc[:, "departure_time"] = wege["Departure_time"] * 60
wege.loc[:, "arrival_time"] = wege["Arrival_time"] * 60

wege.loc[:, "previous_trip_id"] = wege["Trip_id"] -1
df_durations = pd.merge(
        wege[["Household_id", "Trip_id", "departure_time"]],
        wege[["Household_id", "previous_trip_id", "arrival_time"]],
        left_on = ["Household_id", "Trip_id"], right_on = ["Household_id", "previous_trip_id"])

df_durations.loc[:, "activity_duration"] = df_durations["arrival_time"] - df_durations["departure_time"]

wege = pd.merge(
        wege, df_durations[["Household_id", "Trip_id", "activity_duration"]],
        on = ["Household_id", "Trip_id"], how = "left"
    )

# Clean as it was done in the pipeline
unknown_ids = set(wege[
        (wege["Mode"] == "unknown") | (wege["Purpose"] == "unknown")
    ]["Household_id"])
print("  Removed %d persons with trips with unknown mode or unknown purpose" % len(unknown_ids))
wege = wege[~wege["Household_id"].isin(unknown_ids)]

df_end = wege[["Household_id", "Trip_id", "Purpose"]].sort_values("Trip_id", ascending = False).drop_duplicates("Household_id")
df_end = df_end[df_end["Purpose"] != "Home"]

before_length = len(np.unique(wege["Household_id"]))
wege = wege[~wege["Household_id"].isin(df_end["Household_id"])]
after_length = len(np.unique(wege["Household_id"]))
print("  Removed %d persons with trips not ending with 'home'" % (before_length - after_length,))

df_start = wege[["Household_id", "Trip_id", "origin_x", "origin_y", "home_x", "home_y"]]
df_start = df_start[
        (df_start["Trip_id"] == 1) & ((df_start["origin_x"] != df_start["home_x"]) |
        (df_start["origin_y"] != df_start["home_y"]))
]

before_length = len(np.unique(wege["Household_id"]))
wege = wege[~wege["Household_id"].isin(df_start["Household_id"])]
after_length = len(np.unique(wege["Household_id"]))
print("  Removed %d persons with trips not starting at home location" % (before_length - after_length,))

wege = wege[["Household_id",  "Person_weight",
        "Trip_id",
        "Departure_time",
        "Arrival_time",
        "Purpose",
        "Distance"]]

wege.to_csv(outputpath + "wege0109.csv", index = False)
print(len(list(set(wege["Household_id"].values.tolist()))))
    

 



