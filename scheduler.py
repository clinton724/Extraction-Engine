import pytz
import requests
import subprocess
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor

def send_request():
    requests.post("https://tranquil-hamlet-30660.herokuapp.com/schedule.json", data={
        "project": "cryptocurrency",
        "spider": "getUrls"
    })

if __name__ == "__main__":
    subprocess.run("scrapyd-deploy", shell=True, universal_newlines=True)
    scheduler = TwistedScheduler(timezone=pytz.timezone('Asia/Kolkata'))
    # cron trigger that schedules job every every 20 minutues on weekdays
    scheduler.add_job(send_request, 'cron', day_of_week='mon-fri', minute='*/20')
    # start the scheduler
    scheduler.start()
    reactor.run()

