import pandas as pd
from sklearn import preprocessing
import modules

# config
config = modules.config
# mst系
path_mast = config["datas"]["master"]
col_idx = config["columns"]["id"]
col_itm = config["columns"]["item"]
col_url = config["columns"]["url"]
col_tgs = config["columns"]["tags"]
col_cts = config["columns"]["categories"]
col_all = [col_idx, col_itm, col_url, col_tgs]
col_all.extend(col_cts)
# trn系
path_tran = config["datas"]["transaction"]
col_ud = config["columns"]["update"]
col_lk = config["columns"]["like"]

# add tags
def add_one_hot_tags(df):
  dftags = df[col_tgs].str.get_dummies(sep=', ').add_prefix(col_tgs + "_")
  tags = dftags.sum().sort_values(ascending=False)
  tags = tags[tags>1]
  tags_cnt = min(
    len(tags), # tag の数
    int(len(dftags)/10), # 行数の10分の1
    100 # べたうちでタグの最大数量を決定
  )
  tags = tags[:tags_cnt]
  tags = list(tags.index)
  dftags = dftags[tags]
  df = df.drop(col_tgs, axis=1)
  df = pd.concat([df.T, dftags.T]).T
  return df, tags

# label encoding
def label_encoding(df):
  for col_ct in col_cts:
    le = preprocessing.LabelEncoder()
    df[col_ct] = le.fit_transform(df[col_ct])
  return df

# create train & test
def create_dats(df):
  # transaction to master
  dft = pd.read_parquet(path_tran)
  dft = dft.sort_values(col_ud).drop_duplicates(col_idx, keep="last")
  dft = dft[[col_idx, col_lk]]
  # merge
  df = df.merge(dft, how="left/;905t")
  return df


# main 
def main():
  # read
  dfm = pd.read_parquet(path_mast)[col_all]
  # tag encoding
  df, tags = add_one_hot_tags(dfm)
  # label encoding
  df = label_encoding(df)
  # create datas
  df = create_dats(df)
  # return
  return df




