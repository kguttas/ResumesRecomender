from Database import db_mongo
from Utilities import clean_text

ct = clean_text.CleanText()

db = db_mongo.db_mongo()

#db.insert_text({"text": "Text content"})

#db.insert_text_full_resume({"text": "all content resume", "class": "ACCOUNT"})

df = db.get_text(100)

result = ct.cleanner_process(df["text"])

print(result[0])
print(result[1])
print(result[2])
print(result[3])
#print(items_df)

for item in df["class"]:
    # This does not give a very readable output
    text = item.encode('utf8')
    #print(item)

df = db.get_text_full_resume(2)

#print(items_df)

for item in df["text"]:
    # This does not give a very readable output
    text = item.encode('utf8')
    #print(item)