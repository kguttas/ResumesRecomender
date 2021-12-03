from Database import db_mongo

db = db_mongo.db_mongo()

#db.insert_text({"text": "Text content"})

#db.insert_text_full_resume({"text": "all content resume", "class": "ACCOUNT"})

df = db.get_text(2)

#print(items_df)

for item in df["class"]:
    # This does not give a very readable output
    text = item.encode('utf8')
    print(item)

df = db.get_text_full_resume(2)

#print(items_df)

for item in df["text"]:
    # This does not give a very readable output
    text = item.encode('utf8')
    print(item)