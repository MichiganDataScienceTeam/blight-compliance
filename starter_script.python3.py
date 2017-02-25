import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble     import RandomForestClassifier
from sklearn.ensemble     import RandomForestRegressor


# Open data files
path = "./data/"

train = pd.read_csv(path+'train.csv', encoding='iso-8859-1')[::]
test = pd.read_csv(path+'test.csv')
test_ticket_id = np.array(test['ticket_id'])

train = train.set_index('ticket_id')
test = test.set_index('ticket_id')

# Drop the violators who were found not responsible
train.dropna(subset=['compliance'], inplace=True)

# Drop some uninformative features
for column_name in ['inspector_name', 'violator_name', \
                    'violation_zip_code', 'violation_street_number', 'violation_street_name',\
                    'mailing_address_str_number', 'mailing_address_str_name', 'city',\
                    'state', 'zip_code', 'non_us_str_code', 'country',\
                    'violation_description', \
                    'admin_fee', 'state_fee', 'late_fee']:
    test.drop(column_name, axis=1, inplace=True)



# Convert datetime columns into years/months/days
for column_name in ['ticket_issued_date', 'hearing_date']:
    print('Converting datetime to years/months/days...', column_name)
    
    # test
    day_time = pd.to_datetime(test[column_name])
    test.drop(column_name, axis=1, inplace=True)
    test[column_name+'_month'] = np.array(day_time.dt.month)
    test[column_name+'_year'] = np.array(day_time.dt.year)
    test[column_name+'_day'] = np.array(day_time.dt.day)
    test[column_name+'_dayofweek'] = np.array(day_time.dt.dayofweek)
    
    # train
    day_time = pd.to_datetime(train[column_name])
    train.drop(column_name, axis=1, inplace=True)
    train[column_name+'_month'] = np.array(day_time.dt.month)
    train[column_name+'_year'] = np.array(day_time.dt.year)
    train[column_name+'_day'] = np.array(day_time.dt.day)
    train[column_name+'_dayofweek'] = np.array(day_time.dt.dayofweek)

# Convert string columns to categorical
cols = test.select_dtypes(exclude=['float', 'int']).columns
len_train = len(train)
temp_concat = pd.concat((train[cols], test[cols]), axis=0)

# Some filtering on violation_code to make it more manageable
temp_concat['violation_code'] = temp_concat['violation_code'].apply(lambda x: x.split(' ')[0])
temp_concat['violation_code'] = temp_concat['violation_code'].apply(lambda x: x.split('(')[0])
temp_concat['violation_code'][temp_concat['violation_code'].apply(lambda x: x.find('-')<=0)] = np.nan

# Make all codes with < 10 occurrences null
counts = temp_concat['violation_code'].value_counts()
temp_concat['violation_code'][temp_concat['violation_code'].isin(counts[counts < 10].index)] = np.nan

for column_name in cols:
    print('Converting to categorical...', column_name, '# variables:', len(temp_concat[column_name].unique()))
    dummies = pd.get_dummies(temp_concat[column_name])
    temp_concat[dummies.columns] = dummies
    temp_concat.drop(column_name, axis=1, inplace=True)
    train.drop(column_name, axis=1, inplace=True)
    test.drop(column_name, axis=1, inplace=True)

train[temp_concat.columns] = temp_concat.loc[train.index]
test[temp_concat.columns] = temp_concat.loc[test.index]

features = list( test.columns )
response = ['compliance']

print("Number of features:", len(features))

classifiers = {
    "SGD": SGDClassifier(),
    "ASGD": SGDClassifier(average=True),
    "Perceptron": Perceptron(),
    "Passive-Aggressive I": PassiveAggressiveClassifier(loss='hinge', C=1.0),
    "SAG": LogisticRegression(solver='sag', tol=1e-1, C=1.e4 / train[features].shape[0]),
    "RF_C": RandomForestClassifier(max_depth=25),
    "RF_R": RandomForestRegressor(max_depth=25)
}


X = train[features]
Y = np.array(train[response]).ravel()

# Normalize
mn = X.mean()
std = X.std()
X = (X - mn)/std
X = X.replace([np.inf, -np.inf], np.nan)
X[pd.isnull(X)] = 0

Xtest = (test[features] - mn)/std
Xtest = Xtest.replace([np.inf, -np.inf], np.nan)
Xtest[pd.isnull(Xtest)] = 0

# Select the model

for classifier_type in list(classifiers.keys()):
    
    # Train classifier
    clf = classifiers[classifier_type]
    clf.fit(X, Y)
    
    # Predict
    y_pred = np.array(clf.predict(Xtest))
    y_pred = y_pred - y_pred.min()
    y_pred = y_pred / y_pred.max()

    # Save
    df = {"ticket_id":test_ticket_id, "compliance":y_pred}
    df = pd.DataFrame(df, columns=["ticket_id", "compliance"])
    df.to_csv("./data/submission_%s.csv"%classifier_type, index=False)
