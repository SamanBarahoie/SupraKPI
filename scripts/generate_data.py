from faker import Faker
from datetime import datetime, timedelta
import csv, random
import os
from clickhouse_driver import Client

if not os.path.exists("data/sales.csv"):
    fake = Faker()
    with open("data/sales.csv", "w") as f:
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
                fake.word(ext_word_list=["Electronics", "Books", "Clothing", "Food", "Toys"])
            ])

    client = Client('clickhouse')

    client.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            order_id Int32,
            user_id Int32,
            order_date Date,
            amount Float32,
            country String,
            currency String,
            category String
        ) ENGINE = MergeTree()
        ORDER BY order_id
    ''')

    client.execute('''
        INSERT INTO sales (order_id, user_id, order_date, amount, country, currency, category)
        SELECT order_id, user_id, order_date, amount, country, currency, category
        FROM file('/app/data/sales.csv', CSV)
    ''')

    print("Data generated and saved to sales.csv")
else:
    print("Data already exists, skipping data generation.")

