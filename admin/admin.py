from config import init

cereal_database = init()

cereal_data = {
    'test' : 'test',
}

try:
    cereal_database.collection("Cereal").add(cereal_data)
    print("Done")
except Exception as error:
    print(f"Failed {error}")