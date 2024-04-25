from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .views import sendPing

def ping():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(sendPing, 'interval', minutes=30)
        scheduler.start()
    except:
        print("Error pinging...")