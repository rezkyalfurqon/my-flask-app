import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

def training():
    # Import data dari CSV
    data = pd.read_csv('./machine_learning/dataset/testdataset.csv')
    data.head()

    # Konversi tiap value kedalam bentuk angka
    data.loc[data['Sensor1'] == 'NoData', 'Sensor1'] = 0
    data.loc[data['Sensor1'] == 'Less', 'Sensor1'] = 1
    data.loc[data['Sensor1'] == 'More', 'Sensor1'] = 2

    data.loc[data['Sensor2'] == 'NoData', 'Sensor2'] = 0
    data.loc[data['Sensor2'] == 'Less', 'Sensor2'] = 1
    data.loc[data['Sensor2'] == 'More', 'Sensor2'] = 2

    data.loc[data['Sensor3'] == 'NoData', 'Sensor3'] = 0
    data.loc[data['Sensor3'] == 'Less', 'Sensor3'] = 1
    data.loc[data['Sensor3'] == 'More', 'Sensor3'] = 2

    data.loc[data['Sensor4'] == 'NoData', 'Sensor4'] = 0
    data.loc[data['Sensor4'] == 'Less', 'Sensor4'] = 1
    data.loc[data['Sensor4'] == 'More', 'Sensor4'] = 2

    data.loc[data['Sensor5'] == 'NoData', 'Sensor5'] = 0
    data.loc[data['Sensor5'] == 'Less', 'Sensor5'] = 1
    data.loc[data['Sensor5'] == 'More', 'Sensor5'] = 2

    data.loc[data['Sensor6'] == 'NoData', 'Sensor6'] = 0
    data.loc[data['Sensor6'] == 'Less', 'Sensor6'] = 1
    data.loc[data['Sensor6'] == 'More', 'Sensor6'] = 2

    data.loc[data['Sensor7'] == 'NoData', 'Sensor7'] = 0
    data.loc[data['Sensor7'] == 'Less', 'Sensor7'] = 1
    data.loc[data['Sensor7'] == 'More', 'Sensor7'] = 2

    data.loc[data['Sensor8'] == 'NoData', 'Sensor8'] = 0
    data.loc[data['Sensor8'] == 'Less', 'Sensor8'] = 1
    data.loc[data['Sensor8'] == 'More', 'Sensor8'] = 2

    data.loc[data['Sensor9'] == 'NoData', 'Sensor9'] = 0
    data.loc[data['Sensor9'] == 'Less', 'Sensor9'] = 1
    data.loc[data['Sensor9'] == 'More', 'Sensor9'] = 2

    data.loc[data['Sensor10'] == 'NoData', 'Sensor10'] = 0
    data.loc[data['Sensor10'] == 'Less', 'Sensor10'] = 1
    data.loc[data['Sensor10'] == 'More', 'Sensor10'] = 2

    data.loc[data['Kondisi'] == 'Vandalisme', 'Kondisi'] = 2
    data.loc[data['Kondisi'] == 'Normal', 'Kondisi'] = 0
    data.loc[data['Kondisi'] == 'GempaTidakMerusak', 'Kondisi'] = 1
    data.loc[data['Kondisi'] == 'GempaMerusak', 'Kondisi'] = 1

    data = data.apply(pd.to_numeric, errors='coerce')
    data.head(10)

    X = data.iloc[:, 0:10].values  # Independent Feature
    y = data.iloc[:, -1].values    # Dependent Feature
    #memasukan smote pada dataset
    # smote = SMOTE()
    # X_train_smote, y_train_smote = smote.fit_resample(X,y)
    # Pisahkan atribut untuk training & test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    return [X_train, X_test, y_train, y_test]