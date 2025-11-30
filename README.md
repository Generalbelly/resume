# 職務経歴書

English version is [available](en/Resume.pdf)

## スキル

### 言語

- Go（本業でここ 3 年ほど使用）
- Typescript/Javascript, Node.js, React, Vue（副業、個人開発で使用）（副業、個人開発で使用）
- PHP, Laravel
- 日本語 - ネイティブ
- 英語 - 問題なくコミュニケーションはとれるレベル, TOEIC 960 点

### インフラ

- GCP
  - Cloud Run
  - PubSub
  - Datastore
  - Memorystore
  - Cloud Scheduler
  - GAE
  - GCE
  - Cloud SQL
  - BigQuery
  - Cloud Storage
  - Cloud Monitoring
  - Cloud Logging
  - Cloud Build
  - GitHub Action
  - Circle CI
  - Docker
  - Firebase（個人開発）
  - Cloud Function（個人開発）
- AWS
  - EC2
  - S3

## 強み

スタートアップの経験が長いので、とりあえずやってみよう、作ってみようという精神を持っています。  
一方、初期の設計・実装が甘いと、プロダクトが伸びてきたときに改修コストがかかることも身にしみてるので、そのへんのバランスを意識して開発をすすめられます。（もちろんスケールしないと見えてこない問題も多々ありますが。。。）  
また、ビジネスを軌道に乗せるには、営業・マーケティング・カスタマーサポート、どの仕事も重要だと認識してるので、お互いの仕事に敬意を払いつつ協働できます。

## その他エンジニアとしての自分について

- 新規開発・プロダクトが好き
  - 好きなメディア
    - [Indie Hackers](https://www.indiehackers.com/)
    - [Reddit の SideProject スレ](https://www.reddit.com/r/SideProject/)
    - [Product Hunt](https://www.producthunt.com/)
- エンジニアになった理由はサービス、事業をつくりたいから
- 小さくてもニッチでもいいから 1 発サービスをあてたい

## Links

- [ブログ](https://www.tumblr.com/blog/nobuyoshi-shimmen)
- [GitHub](https://github.com/Generalbelly)
- [LinkedIn](https://www.linkedin.com/in/nobuyoshi-shimmen-9a8b1a94/)

## 職務経歴

### 2024/07 - 2025/10（現在） : アジト株式会社

TODO: 新規プロダクトの PdM 兼 開発の経験を書く

### 2023/01 - 2024/06 : アジト株式会社

Databeat の組織が PMM と PdM 体制になり、PdM（プロダクトマネージャー）として、ビジネスサイドとの橋渡し役を務め、基盤システムの刷新、既存機能改善、開発体制の整備を推進しました。

担当業務

- 事業計画の策定（with CEO、PMM）
- プロダクトロードマップの作成・管理
- 要件定義・優先順位付け
- 開発チームのマネジメント（タスク割り振り、進捗管理、新人オンボーディング）
- 障害発生時の旗振り、ビジネスサイドとの調整
- 機能リリースのビジネスサイドとの調整
- 重要顧客のオンボーディングへの参加
- ベータ版機能の開発

チーム規模

- エンジニア 8-10 人
- PMM 1 人
- CS 5-6 人

プロジェクト

- 基盤システムの刷新の推進
  - 刷新を進めつつ、新基盤のインフラ特性を活かし、当日データ取得に対応し、競合との差別化を行なった
- アプリケーションスタッツ・障害情報可視化
  - 媒体のデータ取得完了時間の可視化した
- ユーザーの Looker Studio へのレポート出力を簡易化
  - Linking API を活用し、即時で作れる仕組みの構築した
- 顧客のオンボーディングへの参加
  - 顧客側でエンジニアが出てくるケースも多くなったため、開発サイドの代表としてオンボーディングに参加するようにした
- ベータ版機能の開発
  - 開発リソースが割けないが、顧客からニーズがあるものに関して、GAS を使って実現した（GA4 連携、AppsFlyer 連携, Ajust 連携等）

### 2018/09 - 2022/12 : アジト株式会社 （2022 年 10 月プレイドグループへ参画）

創業メンバーとしてジョインし、BigQuery を最大限活用した[広告レポーティングツール](https://www.data-be.at/)を CTO の右腕となりイチから開発しました。  
テックリードを務め、ビジネスサイドとのコミュニケーションや新機能の要件定義、チーム（3-5 名ほど）へのタスクの割り振り、進捗の管理等の仕事もしました。

担当業務

- 技術選定
- 要件定義
- 設計
- 実装・テスト
- 運用・障害対応
- 新規サービスのプロトタイプ作成

チーム規模

- エンジニア 8-10 人
- デザイナ 0-1 人
- PM/営業 1 人

プロダクト規模

- 接続媒体数 20
- 接続広告アカウント数 約 20,000
- 取得広告レポート数 約 200,000

プロジェクト

- 既存の広告レポート取得アプリケーションのリプレイス（サーバーレス化）
  - 使用技術 Go, PubSub, Cloud Run, Datastore, Memorystore, Cloud Scheduler, BigQuery
- 広告文から業界を判別するプログラムのプロトタイプの開発
  - 使用技術 Go, PubSub, Cloud Run, Datastore
- 広告レポート取得アプリケーションの運用・追加機能開発
  - 使用技術 Go, PubSub, GAE, Datastore, Cloud Scheduler, BigQuery
- 広告データとお客様のデータを紐付けるためのデータマートを作成するアプリケーションの開発
  - 使用技術 Go, PubSub, Cloud Run, Datastore, BigQuery
- BI ツール用 SQL 生成アプリケーションの開発
  - 使用技術 Go, Cloud Run
- Excel レポート生成アプリケーションの開発
  - 使用技術 PHP（フレームワークなし）, GCE, PubSub
- Web アプリケーションのバックエンド・フロントエンド開発
  - 使用技術 Javascript, Vue.js(Vuetify), PHP（Laravel）, GCE

### 2021/02 - 2022/04 : 株式会社ウブン

ご縁があり、副業として Amazon のセラー向けのツールを開発しました。  
フルスタックにフロント、バックエンド、バッチ処理を担当しました。

担当業務

- 実装・テスト
- 運用・障害対応

チーム規模

- エンジニア 2 人
- PM 1 人

### 2015/10 - 2018/07 : 株式会社テクロコ（ソウルドアウト株式会社からの出向）

オールインワンなマーケティングツール [brick](https://www.brick.tools/)の開発業務に携わりました。  
以前、制作業務をしていたときに感じていた問題を解決すべく、[サイトレビュー](https://markezine.jp/article/detail/26719)という、Web サイトのデザインに対するレビュー・修正・指摘をブラウザ上で行えるツールを企画・開発しました。

担当業務

- 企画
- 要件定義
- 設計
- 実装・テスト
- 運用・障害対応

チーム規模

- エンジニア 2 人
- PM 1 人

業務外

- Udacity Machine Learning Engineer Nanodegree Program を修了

### 2014-04 - 2015-09 : ソウルドアウト株式会社

趣味で iOS アプリを作っていてコードが多少かけたので、GAS, Salesforce API, Hubspot API を使って業務効率化を行っていました。

担当業務

- 企画
- 要件定義
- 実装
- 運用

業務外

- Udacity iOS Engineer Nanodegree Program を修了
