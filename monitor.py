import datetime
import tempfile
import requests
import os
import tweepy
from threading import Thread
import cv2
from main import db
from database.models import YakudoScore

auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'),os.environ.get('CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('ACCESS_TOKEN_KEY'), os.environ.get('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth)
keyword= ['#yakudotest']

botname = "mis1yakudo334"

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        t = Thread(runtask(status))
        t.start()

def checkyakudo(url):
    # load img from url
    res = requests.get(url)
    img = None
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    result = (1/cv2.Laplacian(img, cv2.CV_64F).var())*10000 # yakudoスコアの計算
    return result

def runtask(status):
    print("getmessage")
    if status.user.screen_name != botname:
        url = "https://twitter.com/" + status.user.screen_name + "/status/" + status.id_str
        msg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')+"\n"
        msg += "User:@"+status.user.screen_name + "\n"
        # yakudo_check_block
        yakudo = YakudoScore(username=status.user.screen_name,tweetid=status.id_str,date=datetime.datetime.now().strftime('%Y-%m-%d'))
        if hasattr(status, 'extended_entities'):
            print(status.extended_entities)
            finalscore = 0
            count = 0
            isphoto = True
            for image in status.extended_entities["media"]:
                if image["type"] == "video":
                    msg += "やめろ！クソ動画を投稿するんじゃない!\n"
                    msg += "Score:-inf\n"
                    yakudo.score = 0
                    isphoto = False
                    break
                score = checkyakudo(image['media_url_https'])
                finalscore += score
                count += 1
                childtext = "{:.0f}枚目:{:.3f}\n"
                msg += childtext.format(count, score)
                yakudo.score = score
                print(msg)
            if isphoto:
                finalscore //= count
                msg += "GoodYakudo!\n" if finalscore >= 150 else "もっとyakudoしろ！\n"
                finaltext = "Score:{:.3f}\n"
                msg += finaltext.format(finalscore)
        else:
            msg += "画像が入ってないやん!\n"
            msg += "Score:-inf\n"
            yakudo.score = 0
        db.session.add(yakudo)
        db.session.commit()
        api.update_status(msg + url)
        api.create_friendship(status.user.id)

def start_monitoring():
    myStreamListener = MyStreamListener()
    print("start monitoring")
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=keyword)

if __name__ == "__main__":
    start_monitoring()
