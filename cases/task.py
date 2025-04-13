from celery import shared_task


@shared_task
def test_trade_task():
    print("🛠 Steam trade task running...")
    return "Steam trade task complete!"
