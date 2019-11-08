# -*- coding: utf-8 -*-

from sklearn.linear_model import BayesianRidge, LinearRegression, LassoCV, RidgeCV, ElasticNetCV
from sklearn.model_selection import train_test_split,cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score, make_scorer
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold
from sklearn.feature_selection import RFE
from sklearn import preprocessing
import matplotlib.pyplot as plt
from scipy.stats import skew
from sklearn.svm import SVR
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib

pd.options.display.float_format = '{:.2f}'.format

"""## Importing the dataset"""

# Import dataset
data = pd.read_csv('https://raw.githubusercontent.com/cpenalozag/twitter_network/master/dataset/dataset.csv')
print(data.shape)

"""### Data preparation"""

# Remove data from users that have less than 3 tweets (for stratified split)
data = data.groupby('id').filter(lambda x : len(x)>=3)

# Remove useless columns
dataset = data.drop(['common_hts','screen_name', 'description', 'tweet_id'], axis=1)

# Convert boolean data to numbers
dataset[["sensitive", "verified"]] *= 1

# One hot encoding for created at tweet
one_hot1 = pd.get_dummies(dataset['created_at_tweet'])
dataset = dataset.drop('created_at_tweet',axis = 1)
dataset = dataset.join(one_hot1)

# One hot encoding for user type
one_hot2 = pd.get_dummies(dataset['tipo'])
dataset = dataset.drop('tipo',axis = 1)
dataset = dataset.join(one_hot2)

# One hot encoding for core
one_hot3 = pd.get_dummies(dataset['partition'])
dataset = dataset.drop('partition',axis = 1)
dataset = dataset.join(one_hot3)

# Set type for categorical variables
bool_vars = ['sensitive', 'verified']
time_vars = ['afternoon', 'early morning', 'late night', 'morning', 'night', 'noon']
type_vars = ['company', 'competition', 'education', 'entertainment', 'event', 'fans', 'gossip', 'government entity', 'informative', 'journalism', 'news', 'ngo', 'personal', 'politics', 'radio', 'religion', 'sports']
cat_vars = bool_vars
cat_vars.extend(time_vars)
cat_vars.extend(type_vars)

dataset[cat_vars] = dataset[cat_vars].astype('category')

# Transform attributes to [0,1]

attributes = ['retweet_count', 'favorite_count','core', 'no_hashtags', 'no_mentions', 'average_engagement', 'listed', 'no_urls', 'effective_length', 'no_media', 'polarity', 'in_degree', 'clustering', 'closeness', 'betweenness', 'vote_rank', 'authority', 'hubs', 'pagerank']
scaler = preprocessing.MinMaxScaler()
dataset[attributes] = scaler.fit_transform(dataset[attributes])

# Transformation for special variables: followers and friends (keep meaning)
dataset[['followers', 'friends']] = dataset[['followers', 'friends']].astype(np.int32)
dataset['followers'] = data['followers'] / 19000000
dataset['friends'] = data['friends'] / 180000

# Remove retweet_count and favorite_count to remove linear dependency with y (engagement)
dataset = dataset.drop(['favorite_count','retweet_count'], axis=1)

dataset.head()

"""### Data understanding"""

# Descriptive statistics
dataset.describe(include='all')

# Plot histograms
_ = dataset.hist(bins = 50 , figsize = (20,20))

# Box-plot
sns.boxplot(x=dataset['engagement'])

"""### Create datasets excluding outliers"""

from scipy import stats
dataset['z'] = np.abs(stats.zscore(dataset['engagement']))

print('Length original dataset:', len(dataset))

# Indices of outliers given different criteria: >3stds, > 2.75stds, > 2.5 stds
indices2std = []
indices3std = []
indices1std = []

# Iterate through the dataset and update index lists
for index, row in dataset.iterrows():
  if row['z'] >= 0.2:
    indices2std.append(index)
  if row['z'] >= 0.3:
    indices3std.append(index)
  if row['z'] >= 1:
    indices1std.append(index)

# Create new datasets    
dataset2 = dataset.drop(indices2std)
dataset3 = dataset.drop(indices3std)
dataset1 = dataset.drop(indices1std)

# Remove data from users that have less than 2 tweets (for stratified split)
dataset2 = dataset2.groupby('id').filter(lambda x : len(x)>=2)
dataset3 = dataset3.groupby('id').filter(lambda x : len(x)>=2)
dataset1 = dataset1.groupby('id').filter(lambda x : len(x)>=2)

# Remove column with z value
dataset = dataset.drop(['z'], axis=1)

# Print length of new datasets
print('Length dataset without > 1 standard deviations:', len(dataset1))
print('Length dataset without > 0.3 standard deviations:', len(dataset3))
print('Length dataset without > 0.2 standard deviations:', len(dataset2))

"""### Train test split"""

# Divide datasets into attributes and labels
cols = [col for col in dataset.columns if col!='engagement']
X = dataset[cols]
Y = dataset['engagement'].values
X2 = dataset2[cols]
Y2 = dataset2['engagement'].values
X3 = dataset3[cols]
Y3 = dataset3['engagement'].values
X1 = dataset1[cols]
Y1 = dataset1['engagement'].values

# Train test split: 90%, 10%

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=1, stratify = X['id'])
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, Y2, test_size=0.1, random_state=1, stratify = X2['id'])
X_train3, X_test3, y_train3, y_test3 = train_test_split(X3, Y3, test_size=0.1, random_state=1, stratify = X3['id'])
X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, Y1, test_size=0.1, random_state=1, stratify = X1['id'])

# Remove id from data
X_train = X_train.drop(['id'], axis=1)
X_test = X_test.drop(['id'], axis=1)
X_train2 = X_train2.drop(['id'], axis=1)
X_test2 = X_test2.drop(['id'], axis=1)
X_train3 = X_train3.drop(['id'], axis=1)
X_test3 = X_test3.drop(['id'], axis=1)
X_train1 = X_train1.drop(['id'], axis=1)
X_test1 = X_test1.drop(['id'], axis=1)

X = X.values


def mean_squared_error_(ground_truth, predictions):
    return mean_squared_error(ground_truth, predictions) ** 0.5


RMSE = make_scorer(mean_squared_error_, greater_is_better=False)

gbr = GradientBoostingRegressor(random_state=0)
param_grid = {
    'n_estimators': [int(x) for x in np.linspace(start=200, stop=2000, num=10)],
    'max_features': [30, 20, 15, 10, 5, 4, 3, 2],
    'max_depth': [2, 3, 4, 5, 6, 7, 8, 10, 15, 20],
    'learning_rate': [0.5, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001],
    'subsample': [1]
}

model = GridSearchCV(estimator=gbr, param_grid=param_grid, n_jobs=1, cv=5, scoring=RMSE)
model.fit(X_train2, y_train2)
print('Gradient boosted tree regression...')
print('Best Params:')
print(model.best_params_)
print('Best CV Score:')
print(-model.best_score_)
print()
y_pred = model.predict(X_test2)

# Regression Accuracy with test set
accuracy = r2_score(y_test2, y_pred)
print('GBR Accuracy dataset: ', accuracy)
mae = mean_absolute_error(y_test2, y_pred)
print('GBR MAE dataset: ', mae)