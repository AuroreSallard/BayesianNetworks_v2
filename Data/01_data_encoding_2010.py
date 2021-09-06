# region import packages
import numpy as np
import pandas as pd
from scipy import stats
import impute_income as ii

# endregion

# region load data
# folder contain the original data
data_folder = '/nas/asallard/BN/Data/data/'
USE_DETAILED_ACTIVITIES = False

households = pd.read_csv(
    data_folder + 'households2010.csv', encoding="latin1")

persons = pd.read_csv(
    data_folder + 'persons2010.csv', encoding="latin1")

target_persons = pd.read_csv(
    data_folder + 'target_persons2010.csv', encoding="latin1")

wege = pd.read_csv(
    data_folder + 'wege2010.csv', encoding="latin1")

'''
households.dtypes

for i in wege.columns:
    print(str(i) + ':\n')
    if wege[i].dtype == 'O':
        print(wege[i].value_counts())
    else:
        print(stats.describe(wege[i], nan_policy = 'omit'))
    print('\n')
'''

# endregion

# region data encoding for BN -- households
# households.columns
################################ household_size
# There is no missing value:
households['household_size'].value_counts(dropna=False)
# np.sum(households['household_size'].value_counts()) == len(households['household_size'])

# Five categories: [1], [2], [3], [4], [>5]
# households['household_size5'] = None
# households.loc[households['household_size'] == 1, 'household_size5'] = '1'
# households.loc[households['household_size'] == 2, 'household_size5'] = '2'
# households.loc[households['household_size'] == 3, 'household_size5'] = '3'
# households.loc[households['household_size'] == 4, 'household_size5'] = '4'
# households.loc[households['household_size'] >= 5, 'household_size5'] = '>=5'
# households['household_size'].value_counts()
# households['household_size5'].value_counts()


################################ language
# There is no missing value:
households['language'].value_counts(dropna=False)
# np.sum(households['language'].value_counts()) == len(households['language'])
# np.unique(households['language'])


################################ check canton category
# There is no missing value:
households['canton'].value_counts(dropna=False)
# np.sum(households['canton'].value_counts()) == len(households['canton'])


################################ check hhtype
# There is no missing value:
households['hhtype'].value_counts(dropna=False)
# np.sum(households['hhtype'].value_counts()) == len(households['hhtype'])


################################ change nb_cars category
# There is 25 missing values:
households['nb_cars'].value_counts(dropna=False)
# np.sum(households['nb_cars'].value_counts()) == len(households['nb_cars'])
# Six categories: [0], [1], [2], [3], [>4], [NaN]
# households['nb_cars6'] = '0'
# households.loc[households['nb_cars'] == 1, 'nb_cars6'] = '1'
# households.loc[households['nb_cars'] == 2, 'nb_cars6'] = '2'
# households.loc[households['nb_cars'] == 3, 'nb_cars6'] = '3'
# households.loc[households['nb_cars'] >= 4, 'nb_cars6'] = '>=4'
# households.loc[households['nb_cars'].isnull(), 'nb_cars6'] = None
# households['nb_cars'].value_counts(dropna=False)
# households['nb_cars6'].value_counts(dropna=False)


################################ change nb_motorcycles category
# There is 65 missing values:
households['nb_motorcycles'].value_counts(dropna=False)
# np.sum(households['nb_motorcycles'].value_counts()) == len(households['nb_motorcycles'])
# Six categories: [0], [1], [2], [3], [>4], [NaN]
# households['nb_motorcycles6'] = '0'
# households.loc[households['nb_motorcycles'] == 1, 'nb_motorcycles6'] = '1'
# households.loc[households['nb_motorcycles'] == 2, 'nb_motorcycles6'] = '2'
# households.loc[households['nb_motorcycles'] == 3, 'nb_motorcycles6'] = '3'
# households.loc[households['nb_motorcycles'] >= 4, 'nb_motorcycles6'] = '>=4'
# households.loc[households['nb_motorcycles'].isnull(), 'nb_motorcycles6'] = None
# households['nb_motorcycles'].value_counts(dropna=False)
# households['nb_motorcycles6'].value_counts(dropna=False)


################################ change household income category
# There is 16566 missing values:
households['hhl_income'].value_counts(dropna=False)
# np.sum(households['hhl_income'].value_counts()) == len(households['hhl_income'])
# Ten categories: ["< 2000 CHF"], ["2000 - 4000 CHF"], ["4001 - 6000 CHF"],
# ["6001 - 8000 CHF"], ["8001 - 10000 CHF"], ["10001 - 12000 CHF"],
# ["12001 - 14000 CHF"], ["14001 - 16000 CHF"], ["16000 + CHF"]

# income_dic = {
#     "< 2000 CHF": '<2000',
#     "2000 - 4000 CHF": '2000-4000',
#     "4001 - 6000 CHF": '4001-6000',
#     "6001 - 8000 CHF": '6001-8000',
#     "8001 - 10000 CHF": '8001-10000',
#     "10001 - 12000 CHF": '10001-12000',
#     "12001 - 14000 CHF": '12001-14000',
#     "14001 - 16000 CHF": '14001-16000',
#     "16000 + CHF": '>16000',
#     np.nan: None,
# }

income_dic = {
    "< 2000 CHF": 1,
    "2000 - 4000 CHF": 3,
    "4001 - 6000 CHF": 5,
    "6001 - 8000 CHF": 7,
    "8001 - 10000 CHF": 9,
    "10001 - 12000 CHF": 11,
    "12001 - 14000 CHF": 13,
    "14001 - 16000 CHF": 15,
    "16000 + CHF": 17,
    np.nan: -1,
}

households['hhl_income10'] = [income_dic[i] for i in households['hhl_income']]

# households['hhl_income10'].value_counts(dropna=False)
# households['hhl_income'].value_counts(dropna=False)
# endregion
# =============================================================================


# =============================================================================
# region data encoding for BN -- target_persons


# target_persons.columns

# Uncomment when not working with MZ_2010
#target_persons["Person_id"] = target_persons["Household_id"]

################################ change Age category
# There is no missing value:
target_persons['Age'].value_counts(dropna=False)
# np.sum(target_persons['Age'].value_counts()) == len(target_persons['Age'])

# Five categories: [<=12], [13-23], [24-45], [46-64], [>=65]
# target_persons['age5'] = None
# target_persons.loc[target_persons['Age'] <= 12, 'age5'] = '<=12'
# target_persons.loc[
#     (target_persons['Age'] >= 13) & (target_persons['Age'] <= 23),
#     'age5'] = '13-23'
# target_persons.loc[
#     (target_persons['Age'] >= 24) & (target_persons['Age'] <= 45),
#     'age5'] = '24-45'
# target_persons.loc[
#     (target_persons['Age'] >= 46) & (target_persons['Age'] <= 64),
#     'age5'] = '46-64'
# target_persons.loc[target_persons['Age'] >= 65, 'age5'] = '>=65'
# target_persons['age5'].value_counts().sum() == target_persons.shape[0]


################################ check PT_subscription
# There is no missing value:
target_persons['PT_subscription'].value_counts(dropna=False)
# np.sum(target_persons['PT_subscription'].value_counts()) == len(target_persons['PT_subscription'])


################################ Employment_status
# There is no missing value:
target_persons['Employment_status'].value_counts(dropna=False)
# np.sum(target_persons['Employment_status'].value_counts()) == len(target_persons['Employment_status'])

# Seven categories: ['Employed'], ['Retired'], ['Student'], ['Houseperson'],
# ['Unemployed'], ['Disabled'], ['Military/civil service']


################################ Work_time
# There is no missing value:
target_persons['Work_time'].value_counts(dropna=False)
# np.sum(target_persons['Work_time'].value_counts()) == len(target_persons['Work_time'])
target_persons.loc[target_persons["Employment_status"]!= "Employed", "Work_time"] = target_persons[target_persons["Employment_status"] != "Employed"]["Employment_status"].values.tolist()

# four categories, but unreliable


################################ Sex
# There is no missing value:
target_persons['Sex'].value_counts(dropna=False)
# np.sum(target_persons['Sex'].value_counts()) == len(target_persons['Sex'])

# two categories


################################ License_car
# There is 8461 missing values:
target_persons['License_car'].value_counts(dropna=False)
# np.sum(target_persons['License_car'].value_counts()) == len(target_persons['License_car'])

# target_persons['License_car3'] = None
# target_persons.loc[
#     target_persons['License_car'] == 'No', 'License_car3'] = 'no'
# target_persons.loc[
#     target_persons['License_car'] == 'Yes', 'License_car3'] = 'yes'

# target_persons['License_car3'].value_counts(dropna=False)


################################ License_motorcycle
# There is 8742 missing values:
target_persons['License_motorcycle'].value_counts(dropna=False)
# np.sum(target_persons['License_motorcycle'].value_counts()) == len(target_persons['License_motorcycle'])
# target_persons['License_motorcycle3'] = None
# target_persons.loc[target_persons['License_motorcycle']
#                    == 'No', 'License_motorcycle3'] = 'no'
# target_persons.loc[target_persons['License_motorcycle']
#                    == 'Yes', 'License_motorcycle3'] = 'yes'

# target_persons['License_motorcycle3'].value_counts(dropna=False)


################################ week_day
# There is no missing values:
target_persons['Week_day'].value_counts(dropna=False)
# np.sum(target_persons['Week_day'].value_counts()) == len(target_persons['Week_day'])


################################ Work_from_home
# There is 47944 missing values:
target_persons['Work_from_home'].value_counts(dropna=False)
# np.sum(target_persons['Work_from_home'].value_counts()) == len(target_persons['Work_from_home'])


################################ Bicycle_available
# There is 1213 missing values:
target_persons['Bicycle_available'].value_counts(dropna=False)
# np.sum(target_persons['Bicycle_available'].value_counts()) == len(target_persons['Bicycle_available'])

# Four categories
# target_persons['Bicycle_available4'] = None
# target_persons.loc[target_persons['Bicycle_available']
#                    == 'Never', 'Bicycle_available4'] = 'never'
# target_persons.loc[target_persons['Bicycle_available']
#                    == 'Sometimes', 'Bicycle_available4'] = 'sometimes'
# target_persons.loc[target_persons['Bicycle_available']
#                    == 'Always', 'Bicycle_available4'] = 'always'

# target_persons['Bicycle_available4'].value_counts(dropna=False)


################################ Car_available
# There is 15705 missing values:
target_persons['Car_available'].value_counts(dropna=False)
# np.sum(target_persons['Car_available'].value_counts()) == len(target_persons['Car_available'])

# Four categories
# target_persons['Car_available4'] = None
# target_persons.loc[target_persons['Car_available']
#                    == 'Never', 'Car_available4'] = 'never'
# target_persons.loc[target_persons['Car_available']
#                    == 'Sometimes', 'Car_available4'] = 'sometimes'
# target_persons.loc[target_persons['Car_available']
#                    == 'Always', 'Car_available4'] = 'always'

# target_persons['Car_available4'].value_counts(dropna=False)
# target_persons['Car_available'].value_counts(dropna=False)


################################ Motorcycle_available
# There is 5764 missing values:
target_persons['Motorcycle_available'].value_counts(dropna=False)
# np.sum(target_persons['Motorcycle_available'].value_counts()) == len(target_persons['Motorcycle_available'])

# Four categories
# target_persons['Motorcycle_available4'] = None
# target_persons.loc[target_persons['Motorcycle_available']
#                    == 'Never', 'Motorcycle_available4'] = 'never'
# target_persons.loc[target_persons['Motorcycle_available']
#                    == 'Sometimes', 'Motorcycle_available4'] = 'sometimes'
# target_persons.loc[target_persons['Motorcycle_available']
#                    == 'Always', 'Motorcycle_available4'] = 'always'

# target_persons['Motorcycle_available4'].value_counts(dropna=False)
# target_persons['Motorcycle_available'].value_counts(dropna=False)


# endregion
# =============================================================================


# =============================================================================
# region data encoding for BN -- wege


# wege.columns
################################ change purpose category
# There is no missing value:
# np.sum(wege['Purpose'].value_counts()) == len(wege['Purpose'])

# Eight purpose categories: {
    # 'h': 'Home', 'w': 'Work', 'l': 'Leisure', 's': 'Shopping',
    # 'e': 'Education', 'a': 'assistance', 'o': 'Others', 'm': 'Meal',
    # 'b': 'Business',
    # }
trip_purpose_detailed = {
    #### 'Home'
    'Home': 'Home',
    
    #### 'Work'
    'Work': 'Work',
    
    #### 'Leisure'
    'L-Other': 'Leisure',
    'Shopping(L)': 'Leisure',
    'Domestic leisure': 'Leisure',
    'Hiking': 'Leisure',
    'Active sport': 'Leisure',
    'Passive sport': 'Leisure',
    'Leisure(S)': 'Leisure',
    'Picnic': 'Leisure',
    'Tour': 'Leisure',
    'Culture, recreation': 'Leisure',
    'Biking': 'Leisure',
    'Visits': 'Leisure',
    'Outdoor diverse': 'Leisure',
    'WellFit': 'Leisure',
    'Unpaid work': 'Leisure',
    'Association activity': 'Leisure',
    'Excursion': 'Leisure',
    'Religion': 'Leisure',
    'Several purposes': 'Leisure',
    'Gastronomy': 'Leisure',
    
    #### 'Shopping'
    'Grocery': 'Shopping',
    'S-Other': 'Shopping',
    'Other consumption': 'Shopping',
    'Investment goods': 'Shopping',
    
    #### 'Errand'
    'Business activity': 'Errand',
    'Business trip': 'Errand',
    
    #### 'Other'
    'No answer': 'Other',
    'Don\'t know': 'Other',
    'Other': 'Other',
    'Services': 'Other',
    
    #### 'Assistance'
    'Accompanying others': 'Assistance',
    'Accompanying children': 'Assistance',
    
    #### 'Education'
    'Education': 'Education',
}

trip_purpose_dic_not_detailed = {
    "Home": "home",
    "Other": "other",
    "Connection": "other",
    "Work": "work",
    "Education": "education",
    "Shopping": "shopping",
    "Leisure": "leisure",
    "Crossing borders": "other"
}

trip_purpose_dic = trip_purpose_dic_not_detailed
if USE_DETAILED_ACTIVITIES:
    trip_purpose_dic = trip_purpose_dic_detailed
wege['purpose8'] = [trip_purpose_dic[i] for i in wege['Purpose']]

# remove the first activity which is 'Home', 193880 - 188260 = [5620]
wege = wege.loc[(wege['Trip_id'] != 1) | (wege['purpose8'] != 'Home')].copy()


### Adding activity duration
# isLast trip of the day?

# Uncomment when not working with MZ_2010
#wege["Person_id"] = wege["Household_id"]

nb_trips = wege.groupby(["Person_id"]).count()["Trip_id"].reset_index()
nb_trips.columns = ["Person_id", "Nb_trips"]
wege = pd.merge(wege, nb_trips, on = "Person_id")

wege["isLastTrip"] = (wege["Trip_id"] == wege["Nb_trips"])
wege.drop(columns = ["Nb_trips"], inplace = True)

# Computing activity duration if not isLast
wege.loc[:, "previous_trip_id"] = wege["Trip_id"] -1
df_durations = pd.merge(
        wege[["Person_id", "Trip_id", "Arrival_time"]],
        wege[["Person_id", "previous_trip_id", "Departure_time"]],
        left_on = ["Person_id", "Trip_id"], right_on = ["Person_id", "previous_trip_id"])

df_durations.loc[:, "activity_duration"] = df_durations["Departure_time"] - df_durations["Arrival_time"]

wege = pd.merge(
        wege, df_durations[["Person_id", "Trip_id", "activity_duration"]],
        on = ["Person_id", "Trip_id"], how = "left"
    )

wege.loc[wege["isLastTrip"], "activity_duration"] = -1000
wege.loc[np.isnan(wege["activity_duration"]), "activity_duration"] = -1000


'''
wege['purpose8'].value_counts(dropna=False)
# sum(wege['purpose8'].value_counts(dropna=False)) == sum(wege['Purpose'].value_counts(dropna=False))
# wege['Household_id'].value_counts()

wege.groupby(['Household_id'], as_index=False).tail(1).Trip_id.value_counts()
wege.groupby(['Household_id'], as_index=False).tail(1).purpose8.value_counts()
# 97.4% of activity chains end at home
49460 / wege.Household_id.unique().shape[0]

wege.groupby(['Household_id'], as_index=False).nth(4).Trip_id.value_counts()

'''

# endregion
# =============================================================================


# =============================================================================
# region combine required data for BN model


################################ specify required columns and extract
# households.columns
# target_persons.columns
# wege.columns


households_cols = [
    'Household_id', 'Household_weight', 'household_size', 'language',
    'canton', 'hhtype', 'nb_cars', 'nb_motorcycles', 'hhl_income10', 'household_size_class', 'municipality_type', 'nb_bikes']

target_persons_cols = [
    'Household_id', 'Person_weight', 'Age', 'PT_subscription',
    'Employment_status', 'Work_time', 'Sex', 'Language', 'License_car',
    'License_motorcycle', 'Week_day', 'Work_from_home', 'Bicycle_available',
    'Car_available', 'Motorcycle_available', 'age_class', 'Marital_status', "Person_id"
]

data4bn = pd.merge(
    households[households_cols], target_persons[target_persons_cols],
    on='Household_id', how = "right"
    )

data4bn = ii.impute(data4bn)


################################ store activities

# wege['purpose8'].value_counts()
# about 9.5% of activity chains is longer than 6
# sum(wege.Trip_id == 7) / len(np.unique(wege.Household_id))

# number of activities to store
activity_count = 21

for i in range(activity_count):
    
    wege_act = wege.groupby(['Person_id'], as_index=False).nth(i).copy()[
        ['Person_id', 'purpose8', "activity_duration"]
    ].rename(columns={'purpose8': 'activity' + str(i+1),
                      "activity_duration": "duration" + str(i+1)})
    
    data4bn = pd.merge(data4bn, wege_act, on='Person_id', how='left')
    data4bn['activity' + str(i+1)].replace(to_replace=[None], value = "stop", inplace = True)
    data4bn['duration' + str(i+1)].replace(to_replace=[None], value = 0, inplace = True)

data4bn["activity0"] = ["home" for i in range(len(data4bn))]

weights = data4bn["Person_weight"]
min_weight = np.min(weights)
weights_int = [int(w / min_weight) for w in weights]

data4bn["weights"] = weights_int
#data4bn.drop(columns = ["Person_weight", "Household_weight"], inplace = True)

all_nb_work = []
all_nb_education = []
all_nb_secondary = []
all_nb_all = []
total_duration_mandatory = []

for i in range(len(data4bn)):
    row = data4bn.iloc[i]
    act_and_durations = row[25:-2]
    activities = act_and_durations[1::2]
    durations = act_and_durations[0::2]
    nb_work = 0
    nb_educ = 0
    nb_secondary = 0
    total_mandatory = 0
    nb_all = 0
    for d in range(len(activities)):
        if activities[d] in ["education", "work"]:
            nb_all += 1
            if activities[d] == "education":
                nb_educ += 1
            else:
                nb_work += 1
            total_mandatory += durations[d]
        elif activities[d] in ["other", "leisure", "shopping"]:
            nb_secondary += 1
            nb_all += 1
        elif activities[d] == "home":
            nb_all += 1

    all_nb_work.append(nb_work)
    all_nb_education.append(nb_educ)
    all_nb_secondary.append(nb_secondary)
    all_nb_all.append(nb_all)
    total_duration_mandatory.append(total_mandatory)

data4bn["Count_work_activities"] = all_nb_work
data4bn["Count_educ_activities"] = all_nb_education
data4bn["Count_sec_activities"] = all_nb_secondary
data4bn["Count_activities"] = all_nb_all
data4bn["Mandatory_total_duration"] = total_duration_mandatory

data4bn.to_csv(data_folder + 'data4bn_2010.csv', na_rep = 'NA', index = False,
               index_label=False)

'''
# check

data4bn_check = pd.read_csv(
    data_folder + 'data4bn.csv', encoding="latin1", low_memory=False)

data4bn_check.dtypes

for i in data4bn_check.columns:
    print(str(i) + ':\n')
    if data4bn_check[i].dtype == 'O':
        print(data4bn_check[i].value_counts(dropna=False))
    else:
        print(stats.describe(data4bn_check[i], nan_policy = 'omit'))
    print('\n')

'''
# endregion
# =============================================================================









