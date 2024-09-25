from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery

database = False

def build_query(query_ref, query_list):
    # If there is only one condition in the query list, process normally
    if len(query_list) == 1:
        query = query_list[0]
        attribute = query.get('attribute')
        operator = query.get('operator')
        number_name = query.get('number_name')

        print(f"Processing query: {attribute} {operator} {number_name}")

        field_filter = FieldFilter(attribute, operator, float(number_name))

        return query_ref.where(filter=field_filter)

    # If there are multiple conditions, tie them together with AND's
    else:
        filters = []

        for query in query_list:
            attribute = query.get('attribute')
            operator = query.get('operator')
            number_name = query.get('number_name')

            print(f"Processing query: {attribute} {operator} {number_name}")

            # Create a FieldFilter for each query condition and add it to the list
            field_filter = FieldFilter(attribute, operator, float(number_name))
            filters.append(field_filter)

            # Combine with AND's
            # https://github.com/googleapis/python-firestore/issues/705
            composite_filter = BaseCompositeFilter(
                operator=StructuredQuery.CompositeFilter.Operator.AND,
                filters=filters
            )

            return query_ref.where(filter=composite_filter)

def query_parser(query_list, cereal_database):
    print(f"Received Query List: {query_list}")

    try:
        # Access database collection
        query_ref = cereal_database.collection('Cereal')

        completed_query = build_query(query_ref, query_list)

        docs = completed_query.get()
        print(str(docs))

        # Print the query results
        for doc in docs:
            print(doc.id, doc.to_dict())

    except Exception as error:
        print(f"Error: {error}")
