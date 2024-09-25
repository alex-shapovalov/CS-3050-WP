from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery

def query_parser(query_list, cereal_database):
    # try:
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

            if attribute_one == "name" and attribute_two == "name":
                completed_query = query_ref.where(filter=field_filter_one).select([return_value_one]).where(filter=field_filter_two).select([return_value_two])

            elif attribute_one == "name" and attribute_two != "name":
                completed_query = query_ref.where(filter=field_filter_one).select([return_value_one]).where(filter=field_filter_two)

            elif attribute_one != "name" and attribute_two == "name":
                completed_query = query_ref.where(filter=field_filter_one).where(filter=field_filter_two).select([return_value_two])

            else:
                completed_query = query_ref.where(filter=field_filter_one).where(filter=field_filter_two)

            # "of" queries must be handled differently

        else:
            print("Error: Query contains two many elements (probably using more than 1 \'AND\')")

        docs = completed_query.get()

        for doc in docs:
            print(doc.id, doc.to_dict())

    # except Exception as error:
    #     print(f"Error: {error}")