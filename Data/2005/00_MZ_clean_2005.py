import pandas as pd
import numpy as np
import datetime
import savReaderWriter
import pyreadstat
import sys
sys.path.append(".")
sys.path.insert(1, '/nas/asallard/BN/Data')
import impute_mun_type as imt


mzpath = "/nas/asallard/BN/Data/2005/MZ2005/MZ05_Datenbank_CH/2_DB_SPSS/"
outputpath = "/nas/asallard/BN/Data/2005/data/"

hhl, meta = pyreadstat.read_sav(mzpath + "Haushalte.sav", encoding="LATIN1")

with savReaderWriter.SavReader(mzpath + "Haushaltspersonen.sav", ioUtf8 = True) as reader:
    persons = pd.DataFrame(reader.all(), columns = [s for s in reader.header])

with savReaderWriter.SavReader(mzpath + "Zielpersonen.sav", ioUtf8 = True) as reader:
    targets = pd.DataFrame(reader.all(), columns = [s for s in reader.header])

#rawdata_wege = []
#with savReaderWriter.SavReader(mzpath + "Wege.sav", ioUtf8 = "CODEPAGE_MODE") as reader_w:
#    for record in reader_w:
#        try:
#            rawdata_wege.append(record)
#        except UnicodeDecodeError:
#            r = record.decode('latin-1')
#            rawdata_wege.append(r.encode('utf-8'))                
#    wege = pd.DataFrame(rawdata_wege)
#    wege = wege.rename(columns=wege.loc[0]).iloc[1:]
#    #wege = pd.DataFrame(reader.all(), columns = [s for s in reader.header])

wege, meta = pyreadstat.read_sav(mzpath + "Wege.sav", encoding="LATIN1")
#wege.to_csv("rawWege2005.csv", index = False)
steps, meta = pyreadstat.read_sav(mzpath + "Etappen.sav", encoding="LATIN1")
#steps.to_csv("rawEtappen2005.csv", index = False)

##with savReaderWriter.SavReader(mzpath + "Etappen.sav", ioUtf8 = True) as reader:
#    steps = pd.DataFrame(reader.all(), columns = [s for s in reader.header])


USE_DETAILED_ACTIVITIES = False

hhl = hhl.rename(columns = {
        "HHNR": "Household_id",
        "WM": "Household_weight",
        "W_X": "home_x",
        "W_Y": "home_y",
        "W_SPRACHE": "home_language",
        "W_KANTON": "home_canton",
        "F21": "household_type",
        "F22A": "household_size",
        "F31": "number_of_cars",
        "F310": "number_of_motorcycles1",
        "F316": "number_of_motorcycles2",
        "F318": "number_of_motorcycles3",
        "F101": "household_income",
        "F319": "number_of_bikes"
        })

hhl = hhl[["Household_id", "Household_weight", "home_x", "home_y",
           "home_language", "home_canton", "household_type", "household_size",
           "number_of_cars", "number_of_motorcycles1", "number_of_motorcycles2",
           "number_of_motorcycles3", "household_income", "number_of_bikes"]]


hhl["household_size_class"] = np.minimum(5, hhl["household_size"]) - 1
hhl.replace('', np.nan, inplace=True)
hhl.dropna(inplace = True)

hhl = imt.impute_everything(hhl)

hhl["number_of_motorcycles"] = [m1 + m2 + m3 for m1, m2, m3 in 
   list(zip(hhl["number_of_motorcycles1"].values.tolist(), hhl["number_of_motorcycles2"].values.tolist(),
            hhl["number_of_motorcycles3"].values.tolist()))]

hhl["nb_bikes"] = np.maximum(0, hhl["number_of_bikes"])
   
del hhl["number_of_motorcycles1"]
del hhl["number_of_motorcycles2"]
del hhl["number_of_motorcycles3"]
del hhl["number_of_bikes"]

languagedic = {1: "German", 2: "French", 3: "Italian", 4: "Romansh", -97: "NA", np.NaN: "NA"}

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

diff_hhl = {1: "Single", 
            7: "Non family", 
            4: "Couple without kids", 
            3: "Couple with kids",
            2: "Single parent",
            5: "WG",
            6: "Others",
            -97: "Others", -99:"Others", -98:"Others"}

hhl["hhtype"] = [diff_hhl[i] for i in hhl["household_type"]]

del hhl["household_type"]

hhl["nb_cars"] = hhl["number_of_cars"]
hhl["nb_motorcycles"] = hhl["number_of_motorcycles"]
hhl.loc[hhl["number_of_cars"] < pd.Series([0 for i in range(len(hhl))]), "nb_cars"] = 0
hhl.loc[hhl["number_of_motorcycles"] < pd.Series([0 for i in range(len(hhl))]), "nb_motorcycles"] = 0
hhl.loc[hhl["nb_bikes"] < pd.Series([0 for i in range(len(hhl))]), "nb_bikes"] = 0

hhl.loc[hhl["number_of_cars"] > pd.Series([10 for i in range(len(hhl))]), "nb_cars"] = 10
hhl.loc[hhl["number_of_motorcycles"] > pd.Series([10 for i in range(len(hhl))]), "nb_motorcycles"] = 10
hhl.loc[hhl["nb_bikes"] > pd.Series([10 for i in range(len(hhl))]), "nb_bikes"] = 10
hhl.loc[hhl["household_size"] > pd.Series([10 for i in range(len(hhl))]), "household_size"] = 10
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

hhl.to_csv(outputpath + "households2005.csv",  index = False)

persons = persons.rename(columns = {
        "HHNR": "Household_id",
        "WM": "Household_weight",
        "HPNR": "Person_id",
        "F23B": "Age",
        "F23C": "Gender",
        "F24": "Driving_license_car",
        "F25": "Driving_license_motorcycle"
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

persons.to_csv(outputpath + "persons2005.csv",  index = False)

targets = targets.rename(columns = {
        "HHNR": "Household_id",
        "ZIELPNR": "Person_id",
        "WP": "Person_weight",
        "F23B": "Age",
        "F23C": "Gender",
        "W_SPRACHE": "language",
        "TAG": "day_of_week",
        "F24": "Driving_license_car",
        "F25": "Driving_license_motorcycle",
        "F44": "Employed_time",
        "F47": "Home office",
        "F26": "Abonments_PT",
        "F415A": "Availability_bicycle",
        "F415B": "Availability_motorcycle1",
        "F415C": "Availability_motorcycle2",
        "F415D": "Availability_motorcycle3",
        "F415E": "Availability_car",
        "F41": "zivil"
        })

targets = targets[["Household_id", "Person_id",
       "Person_weight",
        "Age",
        "Gender",
        "language",
        "day_of_week",
        "Driving_license_car",
        "Driving_license_motorcycle",
        "Employed_time",
        "Home office",
        "Abonments_PT",
        "Availability_bicycle",
        "Availability_motorcycle1",
        "Availability_motorcycle2",
        "Availability_motorcycle3",
        "Availability_car",
        "zivil"]]

targets["PT_subscription"] = ["Yes" for i in range(len(targets))]
targets.loc[targets["Abonments_PT"] == pd.Series([11 for i in range(len(targets))]), "PT_subscription"] = "No"

targets["Employment_status"] = "Employed"
targets.loc[targets["Age"] < pd.Series([16 for i in range(len(targets))]), "Employment_status"] = "Student"
targets.loc[targets["Employed_time"] == pd.Series([4 for i in range(len(targets))]), "Employment_status"] = "Unemployed"
targets.loc[targets["Employed_time"] == pd.Series([5 for i in range(len(targets))]), "Employment_status"] = "Unemployed"
targets.loc[targets["Employed_time"] == pd.Series([6 for i in range(len(targets))]), "Employment_status"] = "Unemployed"
targets.loc[targets["Employed_time"] == pd.Series([8 for i in range(len(targets))]), "Employment_status"] = "Student"
targets.loc[targets["Employed_time"] == pd.Series([7 for i in range(len(targets))]), "Employment_status"] = "Houseperson"
targets.loc[targets["Employed_time"] == pd.Series([9 for i in range(len(targets))]), "Employment_status"] = "Retired"
targets.loc[targets["Employed_time"] == pd.Series([10 for i in range(len(targets))]), "Employment_status"] = "Disabled"
targets.loc[targets["Employed_time"] == pd.Series([11 for i in range(len(targets))]), "Employment_status"] = "Unemployed"

targets["Work_time"] = "Unemployed"
targets.loc[targets["Employed_time"] == pd.Series([1 for i in range(len(targets))]), "Work_time"] = "Full time"
targets.loc[targets["Employed_time"] == pd.Series([2 for i in range(len(targets))]), "Work_time"] = "Half time"
targets.loc[targets["Employed_time"] == pd.Series([3 for i in range(len(targets))]), "Work_time"] = "More than half time"
targets.loc[targets["Employed_time"] >= pd.Series([4 for i in range(len(targets))]), "Work_time"] = "Unemployed"

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
targets.loc[targets["Availability_bicycle"] == pd.Series([4 for i in range(len(targets))]), "Bicycle_available"] = "NA"

targets["Car_available"] = [None for i in range(len(targets))]
targets.loc[targets["Availability_car"] <= pd.Series([0 for i in range(len(targets))]), "Car_available"] = "NA"
targets.loc[targets["Availability_car"] == pd.Series([1 for i in range(len(targets))]), "Car_available"] = "Always"
targets.loc[targets["Availability_car"] == pd.Series([2 for i in range(len(targets))]), "Car_available"] = "Sometimes"
targets.loc[targets["Availability_car"] == pd.Series([3 for i in range(len(targets))]), "Car_available"] = "Never"
targets.loc[targets["Availability_car"] == pd.Series([4 for i in range(len(targets))]), "Car_available"] = "NA"

motorcycles = pd.Series(np.maximum(targets["Availability_motorcycle1"].values.tolist(), np.maximum( targets["Availability_motorcycle2"].values.tolist(),
                     targets["Availability_motorcycle3"].values)))
targets["Motorcycle_available"] = [None for i in range(len(targets))]
targets.loc[motorcycles <= pd.Series([0 for i in range(len(targets))]), "Motorcycle_available"] = "NA"
targets.loc[motorcycles == pd.Series([1 for i in range(len(targets))]), "Motorcycle_available"] = "Always"
targets.loc[motorcycles == pd.Series([2 for i in range(len(targets))]), "Motorcycle_available"] = "Sometimes"
targets.loc[motorcycles == pd.Series([3 for i in range(len(targets))]), "Motorcycle_available"] = "Never"
targets.loc[motorcycles == pd.Series([4 for i in range(len(targets))]), "Motorcycle_available"] = "NA"

targets["Marital_status"] = [0 for i in range(len(targets))]
targets.loc[targets["zivil"] == 1, "Marital_status"] = 0
targets.loc[targets["zivil"] == 2, "Marital_status"] = 1
targets.loc[targets["zivil"] == 3, "Marital_status"] = 2
targets.loc[targets["zivil"] == 4, "Marital_status"] = 2
targets.loc[targets["zivil"] == 5, "Marital_status"] = 1
targets.loc[targets["zivil"] == 6, "Marital_status"] = 0
targets.loc[targets["zivil"] <= 0, "Marital_status"] = 0

targets["age_class9"] = np.digitize(targets["Age"], [6, 15, 18, 24, 30, 45, 65, 80])
targets["age_class"] = np.digitize(targets["Age"], range(6,100,3))

targets["Person_ID"] = 10 * targets["Household_id"] + targets["Person_id"]
targets["Person_id"] = targets["Person_ID"] 

targets.to_csv(outputpath + "target_persons2005.csv", index = False)


wege = wege.rename(columns = {
        "HHNR": "Household_id",
        "ZIELPNR": "Person_id",
        "WP": "Person_weight",
        "WEGNR": "Trip_id",
        "F58": "Departure_time",
        "F514": "Arrival_time",
        "F5202": "Leisure activity type",
        "F521": "Shopping1",
        "wzweck1": "Trip purpose",
        "wzweck2": "Trip back home",
        "w_dist_obj2": "Distance",
        "wmittel": "mode",
        "W_X": "home_x",
        "W_Y": "home_y",
        "S_X": "origin_x",
        "S_Y": "origin_y"
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
       3: "Outdoor diverse", 
       4: "Active sport", 
       5: "Passive sport", 
       6: "WellFit",
       7: "Culture, recreation",
       8: "Association activity",
       9: "Excursion",
       10: "Volunteering", 
       11: "Shopping (L)", 
       12: "Religion",
       13: "Domestic leisure",
       14: "Picnic",
       15: "L-Other", 
       16: "Several purposes", 
       17: "L-Other",  
       18: "Accompanying", 
       19: "L-Other", 
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
        6: "Several shops",
        7: "Grocery and other but non leisure",
        8: "Several shops",
        -99: "S-Other",
        -98: "S-Other",
        -97: "S-Other"
    }

wege["Mode"] = [modes[i] for i in wege["mode"].values.tolist()]
wege["mode_detailed"] = wege["mode"]
wege.loc[wege["mode"] == 1, "mode_detailed"] = "plane"
wege.loc[wege["mode"] == 11, "mode_detailed"] = "taxi"

wege.replace('', np.nan, inplace=True)
print(len(wege))
wege.dropna(subset = ["Trip purpose"], inplace = True)
print(len(wege))

#steps["is_car_passenger"] = steps["f51300"] == 0
#df_passengers = steps[["HHNR", "WEGNR", "is_car_passenger"]].groupby(["HHNR", #"WEGNR"]).sum().reset_index()
#df_passengers.columns = ["Household_id", "Trip_id", "is_car_passenger" ]
#wege = pd.merge(wege, df_passengers, on = ["Household_id", "Trip_id"], how = "left")
#wege.loc[wege["is_car_passenger"] > 0, "mode_detailed"] = "car_passenger"
#wege.loc[wege["is_car_passenger"] > 0, "mode"] = "car_passenger"
#del wege["is_car_passenger"]

wege["Person_ID"] = 10 * wege["Household_id"] + wege["Person_id"]
wege["Person_id"] = wege["Person_ID"]

wege["Purpose"] = [activities[i] for i in wege["Trip purpose"].values.tolist()]
wege.loc[wege["Trip back home"].values >= np.array([2 for i in range(len(wege))]), "Purpose"] = "Home"

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
        wege[["Person_id", "Trip_id", "departure_time"]],
        wege[["Person_id", "previous_trip_id", "arrival_time"]],
        left_on = ["Person_id", "Trip_id"], right_on = ["Person_id", "previous_trip_id"])

df_durations.loc[:, "activity_duration"] = df_durations["arrival_time"] - df_durations["departure_time"]

wege = pd.merge(
        wege, df_durations[["Person_id", "Trip_id", "activity_duration"]],
        on = ["Person_id", "Trip_id"], how = "left"
    )

# Clean as it was done in the pipeline
unknown_ids = set(wege[
        (wege["Mode"] == "unknown") | (wege["Purpose"] == "unknown")
    ]["Person_id"])
print("  Removed %d persons with trips with unknown mode or unknown purpose" % len(unknown_ids))
wege = wege[~wege["Person_id"].isin(unknown_ids)]

df_end = wege[["Person_id", "Trip_id", "Purpose"]].sort_values("Trip_id", ascending = False).drop_duplicates("Person_id")
df_end = df_end[df_end["Purpose"] != "Home"]

before_length = len(np.unique(wege["Person_id"]))
wege = wege[~wege["Person_id"].isin(df_end["Person_id"])]
after_length = len(np.unique(wege["Person_id"]))
print("  Removed %d persons with trips not ending with 'home'" % (before_length - after_length,))

df_start = wege[["Person_id", "Trip_id", "origin_x", "origin_y", "home_x", "home_y"]]
df_start = df_start[
        (df_start["Trip_id"] == 1) & ((df_start["origin_x"] != df_start["home_x"]) |
        (df_start["origin_y"] != df_start["home_y"]))
]

before_length = len(np.unique(wege["Person_id"]))
wege = wege[~wege["Person_id"].isin(df_start["Person_id"])]
after_length = len(np.unique(wege["Person_id"]))
print("  Removed %d persons with trips not starting at home location" % (before_length - after_length,))

wege = wege[["Household_id",  "Person_weight", "Person_id",
        "Trip_id",
        "Departure_time",
        "Arrival_time",
        "Purpose",
        "Distance"]]

wege.to_csv(outputpath + "wege2005.csv", index = False)
    

 



