# Table Reccomendation
タグなどのテーブルベースのレコメンドアプリ

## 概要
以下のファイルを用意することで簡単にレコメンド画面を作成できる．

- master.parquet
  - レコメンドの対象となる item 群
  - /tablebaserec/data/ に配置
  - 列は以下を用意する
    - id : item を一意に表す id，JANコードなど
    - url : レコメンド画面に付与するリンク
    - item : item を表す名称，商品名など
    - category : item のカテゴリー
    - tags : item のタグ
      - ", " 区切りで文字列を入れる
- transaction.parquet
  - 過去に item を like / not like に分類した履歴
  - /tablebaserec/data/ に配置
  - 列は以下を用意する
    - id : master.parquet と同じ
    - like : like=1, not like=0
    - update : 分類した日付
- images
  - レコメンド画面に表示する画像
  - /tablebaserec/images/ に配置
  - ファイル名は [id].png とする

## 実行方法
### 準備
- /setting/*.txt に サーバーを立てる `hostname`, `port` を記述
- /tablebaserec/config.yaml の設定
  - categories は現在 1 カテゴリーのみに対応
  - また "author" をカテゴリー名称としている
- /tablebaserec/modules/update.py の main 関数を実行

### サーバーの起動
- front-end サーバーの起動
  - /webapp/ で `bash start.sh` を実行
- back-end サーバーの起動
  - /trablebaserec/ で `python flask.py` を実行

### 接続
- 任意のブラウザから `hostname:port_nuxt` で接続

## 実行環境バージョン
- node : v16.13.1
- python : 3.9.6
