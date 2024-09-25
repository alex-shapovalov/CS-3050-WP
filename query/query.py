from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery

def query_parser(query_list, cereal_database):
    # try:
        # Access database collection
        query_ref = cereal_database.collection('Cereal')

        # If we aren't dealing with an "AND" statement
        if len(query_list) == 1:
            query = query_list[0]
            attribute = query.get('attribute')
            operator = query.get('operator')
            number_name = query.get('number_name')
            return_value = query.get('return_value')

            field_filter = FieldFilter(attribute, operator, number_name)

            completed_query = query_ref.where(filter=field_filter)

            # "OF" queries must be handled differently
            if attribute == "name":
                completed_query = completed_query.select([return_value])
            else:
                pass

            docs = completed_query.get()

            for doc in docs:
                print(doc.id, doc.to_dict())

        # Hardcoded "AND"s to only work with a singular "AND"
        elif len(query_list) == 2:
            query_one = query_list[0]
            attribute_one = query_one.get('attribute')
            operator_one = query_one.get('operator')
            number_name_one = query_one.get('number_name')
            return_value_one = query_one.get('return_value')

            query_two = query_list[1]
            attribute_two = query_two.get('attribute')
            operator_two = query_two.get('operator')
            number_name_two = query_two.get('number_name')
            return_value_two = query_two.get('return_value')

            field_filter_one = FieldFilter(attribute_one, operator_one, number_name_one)
            field_filter_two = FieldFilter(attribute_two, operator_two, number_name_two)

            completed_query_exists = False

            # If both are "OF" statements
            if attribute_one == "name" and attribute_two == "name":
                completed_query_one = query_ref.where(filter = field_filter_one).select([return_value_one])
                completed_query_two = query_ref.where(filter = field_filter_two).select([return_value_two])

            # If one is an "OF" statement
            elif attribute_one == "name":
                completed_query_one = query_ref.where(filter = field_filter_one).select([return_value_one])
                completed_query_two = query_ref.where(filter = field_filter_two)

            # If one is an "OF" statement
            elif attribute_two == "name":
                completed_query_one = query_ref.where(filter = field_filter_one)
                completed_query_two = query_ref.where(filter = field_filter_two).select([return_value_two])

            # Neither is an "OF" statement, run a normal "AND" query
            else:
                completed_query = query_ref.where(filter=field_filter_one).where(filter=field_filter_two)
                completed_query_exists = True

            if completed_query_exists == True:
                docs = completed_query.get()

                for doc in docs:
                    print(doc.id, doc.to_dict())

            else:
                docs_one = completed_query_one.get()
                for doc in docs_one:
                    print(doc.id, doc.to_dict())

                docs_two = completed_query_two.get()
                for doc in docs_two:
                    print(doc.id, doc.to_dict())

        else:
            print("Error: Query contains two many elements (probably using more than 1 \'AND\')")