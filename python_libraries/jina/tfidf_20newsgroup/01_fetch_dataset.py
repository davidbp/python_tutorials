from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import os

def twenty_newsgroup_to_csv(data_path='./dataset'):

    os.mkdir(data_path)
    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))

    df = pd.DataFrame([newsgroups_train.data, newsgroups_train.target.tolist()]).T
    df.columns = ['text', 'target']

    targets = pd.DataFrame( newsgroups_train.target_names)
    targets.columns=['title']

    out = pd.merge(df, targets, left_on='target', right_index=True)
    out['date'] = pd.to_datetime('now')
    out.to_csv(os.path.join(data_path,'20_newsgroup.csv'))
    
twenty_newsgroup_to_csv()

