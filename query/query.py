from ..admin.config import init

def query_parser(dictionary):
    # Remove this later, testing to see if function is receiving info correctly
    print(f"Received Dictionary: {dictionary}")

    cereal_database = init()
    print(f"Cereal Database Initialized: {cereal_database}")

    # 1. Take the dictionary and assign variables to various fields:
    try:
        calories = dictionary.get('calories')
        cups = dictionary.get('cups')
        fiber = dictionary.get('fiber')
        manufacturer = dictionary.get('manufacturer')
        sugars = dictionary.get('sugars')
        rating = dictionary.get('rating')

        # Verifying fields received correctly
        print(f"calories: {calories}\n"
              f"cups: {cups}\n"
              f"fiber: {fiber}\n"
              f"manufacturer: {manufacturer}\n"
              f"sugars: {sugars}\n"
              f"rating: {rating}")

    # 2. Send to firestore in the following format and print:

        # Originally had this line below which also matched what you had, ...
            #parsed_query = cereal_database.where(calories, cups, fiber, manufacturer, sugars, rating)
        # but external source said .where needs 3 arguments (field_path, op_string, value)
        # So I edited it. Not sure if we need to specify the collection or not
        parsed_query = cereal_database.collection('Cereal') \
            .where('calories', '==', calories).where('cups', '==', cups) \
            .where('fiber', '==', fiber).where('manufacturer', '==', manufacturer) \
            .where('sugars', '==', sugars).where('rating', '==', rating)
        query_stream = parsed_query.stream()

        for query in query_stream:
            print(f'{query.id} => {query.to_dict()}')

    except Exception as error:
        print(f"Error: {error}")