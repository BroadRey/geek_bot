import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import ADMINS, bot


async def schedule_go_rest() -> None:
    with open('media/gif/chill_gomer.gif', 'rb') as my_gif:
        for admin_id in ADMINS:
            await bot.send_animation(
                admin_id,
                my_gif,
                caption=(
                    'Дружище, у тебя начались выходные!\n'
                    'Давай вылезай из-за компа!'
                )
            )


async def create_scheduler() -> None:
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")

    scheduler.add_job(
        schedule_go_rest,
        trigger=CronTrigger(
            day_of_week=4,
            hour=1,
            minute=10,
            start_date=datetime.datetime.now()
        )
    )

    scheduler.start()
