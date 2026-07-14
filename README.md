# Life Game Project

ライフゲームの初期密度による変化を調べるPythonプログラムです。

## ファイル構成


Learning-Python
│
├── Life-Game.py
├── README.md
│
└── lifegame_results
├── result.csv
├── time.png
├── population.png
└── extinction.png

---

## 各ファイルの説明

### Life-Game.py

ライフゲームのシミュレーションを実行するメインプログラム。

機能：

- 100×100セルの世界を作成
- 初期密度を変更して実験
- 複数回シミュレーション
- 生存セル数を計測
- 安定までの世代数を計測
- 結果をCSVとグラフとして保存

実行方法：

```bash
python3 Life-Game.py

lifegame_results フォルダ
実験後に自動生成される結果保存用フォルダ。
result.csv
実験結果を表形式で保存したファイル。
内容：

初期密度
平均安定世代
平均最終生存セル数
全滅率
time.png
初期密度と安定までの時間を表すグラフ。
population.png
初期密度と最終的な生存セル数を表すグラフ。
extinction.png
初期密度と全滅率を表すグラフ。