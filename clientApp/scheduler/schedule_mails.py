from apscheduler.schedulers.background import BackgroundScheduler
from clientApp.views import SummaryReport

def start():
    scheduler = BackgroundScheduler()
    instance = SummaryReport()
    scheduler.add_job(
        instance.mail_summary_report,
        "cron",
        hour=23,
        minute=59,
        id="api_001",
        replace_existing=True,
    )
    scheduler.start()