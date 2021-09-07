import sklearn.tree
import numpy as np

def impute(df_mz):
    # Train the tree
    no_income_selector = df_mz["hhl_income10"] == -1
    df_mz["sex"] = 1
    df_mz.loc[df_mz["Sex"] == "Male", "sex"] = 2

    print(list(set(df_mz["nb_cars"].values.tolist())))
    print(list(set(df_mz["nb_bikes"].values.tolist())))
    print(list(set(df_mz["Age"].values.tolist())))
    print(list(set(df_mz["sex"].values.tolist())))
    print(list(set(df_mz["Marital_status"].values.tolist())))
    print(list(set(df_mz["household_size"].values.tolist())))

    # TODO: We don't use any weights here. Shouldn't we?
    training_data = df_mz[~no_income_selector][[
        "age_class9"#, "sex", "Marital_status", "household_size", "nb_cars"#, "nb_bikes"
    ]].values

    training_labels = df_mz[~no_income_selector]["hhl_income10"].values
    training_weights = df_mz[~no_income_selector]["Person_weight"].values

    # TODO: Maybe adjusted later!
    classifier = sklearn.tree.DecisionTreeClassifier(min_samples_leaf = 30, max_depth = 5)

    classifier.fit(X=training_data, y=training_labels, sample_weight=None)

    # Predict the incomes
    prediction_data = df_mz[no_income_selector][[
        "age_class9"#, "sex", "Marital_status", "household_size", "nb_cars"#, "nb_bikes"
    ]].values

    df_mz.loc[no_income_selector, "hhl_income10"] = classifier.predict(prediction_data)

    df_mz["income_imputed"] = False
    df_mz.loc[no_income_selector, "income_imputed"] = True

    return df_mz

