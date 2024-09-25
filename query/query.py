from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery

def query_parser(query_list, cereal_database):
    try:
        # Access database collection
        query_ref = cereal_database.collection('Cereal')
        print(str(query_list))

        if len(query_list) == 1:
            query = query_list[0]
            attribute = query.get('attribute')
            operator = query.get('operator')
            number_name = query.get('number_name')
            return_value = query.get('return_value')

            field_filter = FieldFilter(attribute, operator, number_name)

            completed_query = query_ref.where(filter=field_filter)

            # "of" queries must be handled differently
            if attribute == "name":
                completed_query = completed_query.select([return_value])
            else:
                pass

        # If there are multiple conditions, tie them together with AND's
        else:
            return_value_map = {}
            completed_query = query_ref

            def recursive_and(completed_query, index):
                # Base case: If index reaches the end of query_list, return the completed query
                if index >= len(query_list):
                    return completed_query

                # Get the current query item
                query = query_list[index]
                attribute = query.get('attribute')
                operator = query.get('operator')
                number_name = query.get('number_name')
                return_value = query.get('return_value')

                # Store every instance of "of" queries
                if attribute == "name":
                    return_value_map[number_name] = return_value

                field_filter = FieldFilter(attribute, operator, number_name)

                # Chain together where for "and"
                completed_query = query_ref.where(filter=field_filter)

                return recursive_and(completed_query, index + 1)

            completed_query = recursive_and(completed_query, 0)

            # Once recursion is done, apply select() if there is a 'name' query
            if return_value_map:
                of = list(return_value_map.values())
                completed_query = completed_query.select(of)

        docs = completed_query.get()

        for doc in docs:
            print(doc.id, doc.to_dict())

    except Exception as error:
        print(f"Error: {error}")