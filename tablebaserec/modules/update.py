import lightgbm as lgbm
import modules
import pandas as pd
from sklearn import preprocessing

# config
config = modules.config
# mst系
path_mast = config["datas"]["master"]
col_idx = config["columns"]["id"]
col_itm = config["columns"]["item"]
col_url = config["columns"]["url"]
col_tgs = config["columns"]["tags"]
col_cat = config["columns"]["category"]
col_all = [col_idx, col_itm, col_url, col_tgs, col_cat]
col_idxcts = [col_idx, col_cat]

# trn系
path_tran = config["datas"]["transaction"]
col_ud = config["columns"]["update"]
col_lk = config["columns"]["like"]
# output
path_pred = config["datas"]["prediction"]


# add tags
def add_one_hot_tags(df):
    dftags = df[col_tgs].str.get_dummies(sep=", ")
    # dftags = dftags.add_prefix(col_tgs + "_")
    tags = dftags.sum().sort_values(ascending=False)
    tags = tags[tags > 1]
    tags_cnt = min(
        len(tags), int(len(dftags) / 10), 100  # tag の数  # 行数の10分の1  # べたうちでタグの最大数量を決定
    )
    tags = tags[:tags_cnt]
    tags = list(tags.index)
    dftags = dftags[tags]
    df = df.drop(col_tgs, axis=1)
    df = pd.concat([df.T, dftags.T]).T
    return df, tags


# label encoding
def label_encoding(df):
    le = preprocessing.LabelEncoder()
    df[col_cat] = le.fit_transform(df[col_cat])
    return df


# add target
def add_target(df):
    # transaction to master
    dft = pd.read_parquet(path_tran)
    dft = dft.sort_values(col_ud).drop_duplicates(col_idx, keep="last")
    dft = dft[[col_idx, col_lk]]
    # merge
    df = df.merge(dft, how="left")
    return df


# split train & test
def split_data(df):
    train = df[~df[col_lk].isnull()].set_index(col_idx)
    test = df[df[col_lk].isnull()].set_index(col_idx)
    x_train = train.drop([col_itm, col_url, col_lk], axis=1).astype(int)
    x_test = test.drop([col_itm, col_url, col_lk], axis=1).astype(int)
    y_train = train[col_lk].astype(int)
    return x_train, y_train, x_test


# model creation & prediction
def lgbm_predict(x_train, y_train, x_test):
    # model creation
    seed = 2023
    model = lgbm.LGBMClassifier(
        boosting_type="gbdt",
        num_leaves=31,
        max_depth=-1,
        learning_rate=0.1,
        n_estimators=100,
        reg_alpha=0.0,
        reg_lambda=0.0,
        random_state=seed,
    )
    model.fit(x_train, y_train)
    # prediction
    pred_train = pd.DataFrame({col_idx: x_train.index, col_lk: y_train}).reset_index(
        drop=True
    )
    pred_test = pd.DataFrame(
        {col_idx: x_test.index, col_lk: model.predict_proba(x_test).T[1].T}
    ).reset_index(drop=True)
    pred = pd.concat([pred_train, pred_test])
    return pred


# main
def main():
    # read
    dfm = pd.read_parquet(path_mast)[col_all]
    # tag encoding
    df, tags = add_one_hot_tags(dfm)
    # label encoding
    df = label_encoding(df)
    # add target
    df = add_target(df)
    # split train & test
    x_train, y_train, x_test = split_data(df)
    # model creation
    pred = lgbm_predict(x_train, y_train, x_test)
    # merge
    df = df.drop(col_lk, axis=1).merge(pred, on=col_idx)
    # inverse label encoding
    df = df.drop(col_cat, axis=1).merge(dfm[col_idxcts], on=col_idx)
    # output
    df.to_parquet(path_pred)
    # return
    return df
