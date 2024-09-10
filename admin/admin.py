from config import init
import json

def main():
    cereal_database = init()

    with open('../cereal.json') as cereal:
        cereal_data = json.load(cereal)

    try:
        for field in cereal_data:
            # https://stackoverflow.com/questions/66370426/best-way-to-send-json-data-from-api-to-firestore-with-python
            doc_ref = cereal_database.collection('Cereal').document(field["name"])
            doc_ref.set(field)
        print("Successfully cereal added data into Firestore")
    except Exception as error:
        print(f"Failed: {error}")

main()