
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('database.config') # 追加
db = SQLAlchemy(app) # 追加

#herokuサーバーをスリープさせない為の対策
@app.route("/")
def index():
    return "This is mis1yakudo_bot!"

if __name__ == "__main__":
    app.run()


