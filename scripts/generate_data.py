from faker import Faker
from datetime import datetime, timedelta
import csv, random, os
from clickhouse_driver import Client

DATA_PATH = "/app/data/sales.csv"

# فقط اگر فایل وجود نداشت، دیتا بساز
if not os.path.exists(DATA_PATH):
    fake = Faker()
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "user_id", "order_date", "amount", "country", "currency", "category"])
        for i in range(10000):
            writer.writerow([
                i,
                random.randint(1, 500),
                (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
                round(random.uniform(10, 500), 2),
                fake.country(),
                fake.currency_code(),
                random.choice(["Electronics", "Books", "Clothing", "Food", "Toys"])
            ])
    print("Data generated and saved to", DATA_PATH)
else:
    print("Data already exists, skipping generation.")

# اتصال به ClickHouse
client = Client(
    host='clickhouse',
    port=9000,
    user='default',
    password='',    # اگر پس‌ورد خالی ست کرده‌اید
    database='default'
)

# ایجاد جدول اگر نبود
client.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        order_id   Int32,
        user_id    Int32,
        order_date Date,
        amount     Float32,
        country    String,
        currency   String,
        category   String
    ) ENGINE = MergeTree()
    ORDER BY order_id
''')

# بارگذاری از طریق table function file()
client.execute('''
    INSERT INTO sales
    SELECT *
    FROM file('/var/lib/clickhouse/user_files/data/sales.csv', CSV,
        'order_id Int32, user_id Int32, order_date Date, amount Float32,
         country String, currency String, category String')
''')

print("Data loaded into ClickHouse.")
