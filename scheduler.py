import tweepy,os,datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from main import db
from database.models import YakudoScore
import subprocess
from subprocess import PIPE

twische = BlockingScheduler()

auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'),os.environ.get('CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('ACCESS_TOKEN_KEY'), os.environ.get('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth)
userID = "mis1yakudo334"

def getalltweets():
    all_tweets = []
    Current_Date = datetime.datetime.today()
    starttime = Current_Date.strftime('%Y-%m-%d_00:00:00_JST')
    endtime = Current_Date.strftime('%Y-%m-%d_23:59:59_JST')
    tweets = api.user_timeline(screen_name=userID,since = starttime, until = endtime, count=200,include_rts=False, tweet_mode='extended')
    all_tweets.extend([t for t in tweets if "Score:" in t.full_text])
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=userID, since = starttime, until = endtime, count=200,include_rts=False,max_id=oldest_id - 1,tweet_mode='extended')
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend([t for t in tweets if "Score:" in t.full_text])
    return all_tweets

@twische.scheduled_job('interval',minutes=1)
def timed_job():
    now = datetime.datetime.now()
    if now.minute == 0:
        yakudos = YakudoScore.query.filter(YakudoScore.date==datetime.datetime.now().strftime('%Y-%m-%d')).all()
        if len(yakudos) == 0:
            api.update_status("おいお前ら!早くyakudoしろ!(" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ")")
        else:
            api.update_status("本日のyakudo:" + str(len(yakudos)) + "件(" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ")")
        print("ScheduledTask Complete")
    elif now.minute == 59 and now.hour == 23:
        yakudos = YakudoScore.query.filter(YakudoScore.date == datetime.datetime.now().strftime('%Y-%m-%d')).all()
        maxscore = 0
        maxuser = ""
        maxtweetid = ""
        if len(yakudos) == 0:
            api.update_status("本日のyakudoは...何一つ...出ませんでした...")
        else:
            for yakudo in yakudos:
                if yakudo.score > maxscore:
                    maxscore = yakudo.score
                    maxtweetid = yakudo.tweetid
                    maxuser = yakudo.username
            if maxscore > 0:
                msg = "Highest Score:{:.3f}\n優勝おめでとう!\n".format(maxscore)
                url = "https://twitter.com/" + maxuser + "/status/" + maxtweetid
                api.update_status(msg + url)
            else:
                api.update_status("おい待てや...今日のyakudo...-inf点しか無いやん...")
    elif now.minute == 500:
        print("Checking Database")
        yakudos = YakudoScore.query.filter(YakudoScore.date == datetime.datetime.now().strftime('%Y-%m-%d')).all()
        count = 0
        for yakudo in yakudos:
            if yakudo.score > maxscore:
                maxscore = yakudo.score
                maxtweetid = yakudo.tweetid
                maxuser = yakudo.username
        YakudoScore.query.filter(YakudoScore.tweetid == "1387621068945313798").delete()
        try:
            tweet = api.get_status("1387621068945313798")
            print(tweet)
        except:
            tweet = api.search(expanded_url="https://twitter.com/tamacake39/status/1387621068945313798")
            print("Tweet Not Found")


if __name__ == "__main__":
    twische.start()