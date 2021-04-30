# yakudobot

## これは何?
- ハッシュタグ「#mis1yakudo」がついてるツイートを自動的にリツイートしたり、yakudo写真を評価したりするbotです。
時間あったらアプリをDocker化するかもしれません。

## 使い方
### 環境構築
まず、```~/.bashrc```を編集して、APIのTokenを環境変数として登録してください。
```
export ACCESS_TOKEN_KEY="xxxxxxx"
...
```
次に、必要なライブラリーを導入します。
python3がインストールされていない方は、まずpython3をインストールしてください。
```
sudo apt install python3 python3-pip
```
python3とpipが導入できたら、下記のコマンドを実行します。
```
git clone https://github.com/HarrisonKawagoe3960X/yakudobot.git
cd yakudobot
pip3 install -r requirements.txt
```
これで、必要なライブラリーの導入が終了しました。
### アプリの構成
- ```scheduler.py```定期ツイート&ツイ消しの探知
- ```monitor.py```「#mis1yakudo」を含むツイートの探知&引用リツイート
### アプリの起動
```
python3 scheduler.py
python3 monitor.py
```
