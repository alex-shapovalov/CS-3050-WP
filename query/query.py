from admin.config import init
from google.cloud.firestore_v1.base_query import FieldFilter

def query_parser(query_list):
    print(f"Received Query List: {query_list}")

    # Initialize database
    cereal_database = init()
    print(f"Cereal Database Initialized: {cereal_database}")

    try:
        # Access database collection
        query_ref = cereal_database.collection('Cereal')

        count = 0

        # For each dictionary in our query_list, grab attribute, operator, and number_name
        # Create query and push it to firestore
        for query in query_list:
            attribute = query.get('attribute')
            operator = query.get('operator')
            number_name = query.get('number_name')

            # Send completed_query to firestore, currently holding program infinitely
            completed_query = query_ref.where(filter=FieldFilter(attribute, operator, number_name))
            docs = completed_query.get()

            print(str(docs))

            # Need to handle 'and' queries here, maybe add 'and' if looping
            # through more than once

            # if count > 1:
            #     concat 'and' at end of the query

            count = count + 1

    except Exception as error:
        print(f"Error: {error}")