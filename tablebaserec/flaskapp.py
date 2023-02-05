import pandas as pd
import datetime
import yaml
import json
from flask import Flask, request, send_file
from flask_cors import CORS

path_yaml = "config.yaml"
with open(path_yaml) as file:
    config = yaml.safe_load(file)

infos = ["hostname", "port_flask"]
settings = {}
for info in infos:
    f = open(f'../setting/{info}.txt', 'r')
    settings[info] = f.read()
    f.close()

col_lk = config["columns"]["like"]
col_id = config["columns"]["id"]

def get_now():
    DIFF_JST_FROM_UTC = 9
    return datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)

def reload_prediction():
    df = pd.read_parquet(config["datas"]["prediction"])
    df = df.rename(
        columns={
            col_id: "id",
            config["columns"]["item"]: "item",
            config["columns"]["url"]: "url",
            config["columns"]["category"]: "category"
        }
    )
    return df
df = reload_prediction()

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app)


@app.route("/datas", methods=["GET"])
def datas():
    contentsToShow = str(request.args.get("contentsToShow"))
    contentsIn1Page = int(request.args.get("contentsIn1Page"))
    page = int(request.args.get("page"))
    category = str(request.args.get("category"))
    tag = str(request.args.get("tag"))

    # train (or test) への絞り込み
    tmp = df.copy()
    if contentsToShow == "":
        tmp = tmp[(tmp[col_lk] != 1) & (tmp[col_lk] != 0)].copy()
    elif contentsToShow == "train":
        tmp = tmp[(tmp[col_lk] == 1) | (tmp[col_lk] == 0)].copy()
    # 属性による絞り込み
    if category != "":
        tmp = tmp[tmp["category"] == category]
    # Tagによる絞り込み
    if tag != "":
        tmp = tmp[tmp[tag] == 1]    
    # page の絞り込み
    tmp = tmp.sort_values([col_lk, "item"], ascending=False)
    tmp = tmp.reset_index(drop=True)
    tmp = tmp[(page - 1) * contentsIn1Page : page * contentsIn1Page]
    # return
    return tmp.T.to_json()


@app.route("/image", methods=["GET"])
def image():
    index = int(request.args.get("id"))
    image = send_file(f"./images/{index}.png")
    return image


@app.route("/categories", methods=["GET"])
def categories():
    cts = df[["category", col_lk]].copy()
    cts0 = pd.DataFrame({"category":cts["category"].unique()})
    cts0[col_lk] = 0
    cts = pd.concat([cts, cts0])
    cts = (
        cts.groupby("category", as_index=False).mean().sort_values(col_lk, ascending=False)
    )
    cts = cts[cts["category"]!=""]
    cts = pd.concat([
        cts, pd.DataFrame({"category": [""], col_lk: [2]})
    ])
    cts = cts.set_index("category")
    return cts[col_lk].to_json()


@app.route("/tags", methods=["GET"])
def tags():
    tags = df.columns.to_list()
    for rm in ["id", "item", "url", "category", col_lk]:
        tags.remove(rm)
    return tags


@app.route("/updatelike", methods=["GET"])
def updatelike():
    idx = int(request.args.get("id"))
    like = int(request.args.get("like"))
    # 更新対象の読み込み
    transaction = pd.read_parquet(config["datas"]["transaction"])
    prediction = pd.read_parquet(config["datas"]["prediction"])
    # transaction の更新
    rows = pd.DataFrame({col_id: [idx]})
    rows[col_lk] = like
    rows["update"] = get_now()
    transaction = pd.concat([transaction, rows]).reset_index(drop=True)
    # pd.to_parquet(config["datas"]["transaction"], index=False)
    # prediction の更新
    prediction.loc[prediction[col_id]==idx, col_lk] = like
    prediction.to_parquet(config["datas"]["prediction"], index=False)    
    # global df の更新
    global df
    df = reload_prediction()
    return ""


@app.route("/retraining", methods=["GET"])
def retraining():
    import modules
    _ = modules.update.main()
    del modules
    # global df の更新
    global df
    df = reload_prediction()
    return ""


if __name__ == "__main__":
    app.run(host=settings["hostname"], port=settings["port_flask"], debug=True)
