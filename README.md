# 匿名掲示板 Anonymous Boardapp

## アプリ概要

このアプリはブラウザ上で動作するコメントアプリです。大学の授業にて前期、後期の1年間を通して制作を行いました。
大学の授業で質問する際に、既存のオンラインツールでは名前や学籍番号などが表示されてしまい、投稿者が他の学生や教員などに知られてしまいました。そのために質問しづらい環境になっているのではないかと考え、誰が質問しているのかを知られることなくコメントできるアプリとして作成を始めました。

[前期の制作](https://github.com/wakashiyo/AnonymousBoardapp-FirstTerm "前期の匿名掲示板")では、コメントの投稿機能や編集、削除、返信機能といった掲示板アプリとしての基礎となる部分を実装しました。

当初はこの段階までの開発で終わる予定でしたが、さらに使いやすいアプリにしたいという思いがあり、開発を継続することにしました。

ユーザー登録、ログイン機能やコメントに対するいいね機能を目標として後期の制作を始めました。

## 使用技術

### FRONTEND

![Javascript](https://img.shields.io/badge/-Javascript-000.svg?logo=javascript&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=for-the-badge)

### BACKEND

![Python](https://img.shields.io/badge/-Python-FFE873.svg?logo=python&style=for-the-badge)
![Django](https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge)

### MIDDLEWARE

![NGINX](https://img.shields.io/badge/-Nginx-269539.svg?logo=nginx&style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/-Postgresql-336791.svg?logo=postgresql&style=for-the-badge&logoColor=fff)
![Redis](https://img.shields.io/badge/-Redis-D82C20.svg?logo=redis&style=for-the-badge&logoColor=fff)

### INFRASTRUCTURE

![Docker](https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge)

### EDITOR

![Visual Stduio Code](https://img.shields.io/badge/-Visualstudiocode-007ACC.svg?logo=visualstudiocode&style=for-the-badge)

## 環境

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.10-alpine|
| Django                | 4.2.7      |
| PostgreSQL            | 16.0       |
| Bootstrap             | 5.3.0      |
| nginx                 | 1.17.7     |
| Gunicorn              | 20.1.0     |
| Redis                 | 7.2.3      |

### コンテナの起動

.envファイルをプロジェクトのrootディレクトリに作成し、以下の項目をそれぞれ設定します。

```{.env}
SECRET_KEY=YOUR_SERCRET_KEY
POSTGRES_DB=boardappdb
POSTGRES_USER=boardappadmin
POSTGRES_PASSWORD=YOUR_PASSOWORD
POSTGRES_HOST=db
POSTGRES_PORT=5432
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=YOUR_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=YOUR_OAUTH2_SECRET_KEY
```

.envファイルを作成後、以下のコマンドを実行します。

```{bash}
docker compose up -d
```

### 動作確認

`http://localhost:8080` でアクセスできるかどうかを確認してください。

### コンテナの停止

以下のコマンドでコンテナを停止します。

```{bash}
docker compose down
```

## 機能

1. コメントの投稿

    ![一覧ページ画像](./images/list.png)

2. パスワード設定によるコメント編集操作の制限

    ![投稿ページ画像](./images/posting.png)

3. コメントの編集、削除

4. 返信の投稿

5. ページネーション

    ![コメント詳細](./images/detail.png)

6. サインアップ

    ![サインアップページ画像](./images/signup.png)

7. ログイン/ログアウト

    ![ログインページ画像](./images/login.png)

    ![ログアウトページ画像](./images/logout.png)

8. コメントのお気に入り

    ![お気に入り機能画像](./images/good.png)

## 発表

前期と同様に今回の制作も学内で発表を行いました。以下はそのときに使用した発表用資料です。制作の経緯や工夫点、課題などを記載していますので、ぜひご覧ください。

[Boardapp 発表資料（外部サイト）](https://www.canva.com/design/DAF_lSH_hbY/-eQoy1D34qBRkU8dAAlUYg/edit?utm_content=DAF_lSH_hbY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
