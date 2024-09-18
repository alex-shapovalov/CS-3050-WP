from ..admin.config import init

def query_parser(dictionary):
    # Remove this later, testing to see if function is receiving info correctly
    print(str(dictionary))

    cereal_database = init()

    # 1. Take the dictionary and assign variables to various fields:


    # 2. Send to firestore in the following format and print:

    # parsed_query = cereal_database.where(var1, var2, var3, ..., varx)
    # query_stream = parsed_query.stream()

    # for query in query_stream:
    #     print(f'{query.id} => {query.to_dict()}')