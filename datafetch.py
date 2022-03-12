import pandas as pd
from pymongo import MongoClient

def preprocess_dataframe(df_survey):
    df_survey['time'] = pd.to_datetime(df_survey['time']).dt.date
    df_survey = df_survey.drop(['__v'], axis=1)

    df_survey['product_fit'] = df_survey['product_fit'].replace({'1': 'Not Disappointed',
                                                                 '2': 'Somewhat Disappointed',
                                                                 '3': 'Very Disappointed'})

    df_table = df_survey[['product_fit_comment', 'improvement']]
    df_table = df_table[(df_table['product_fit_comment'] != 'none') & (df_table['improvement'] != 'none')]

    df_nums = df_survey.copy()
    df_nums = df_nums.groupby('time').count()
    df_nums.reset_index(inplace=True)
    df_nums = df_nums[['time', '_id']]
    df_nums = df_nums.rename(columns={'time': 'date', '_id': 'count'})

    return df_nums

def load_mongo_dataframe():
    print('Trying to connect to MongoDB..')
    client = MongoClient("mongodb+srv://dbUser:120994@cluster0.dv2zh.mongodb.net/")
    db = client.pear_bva_db
    df_survey = pd.DataFrame(list(db.surveys.find()))

    df_table = preprocess_dataframe(df_survey)
    return df_table

def load_local_dataframe():
    print('Trying to load the file from Local..')
    df_survey = pd.read_csv('sample_dataset/surveyData.csv')
    df_table = preprocess_dataframe(df_survey)
    return df_table