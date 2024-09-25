from parser import Parser
from parser import ParseError
from query import query_parser
from admin.config import init

class CerealParser(Parser):
    def start(self):
        return self.expression()

    # returns list of dicts of querys joined by ands (query1,query2...)
    def expression(self):
        rv = []
        rv.append(self.match('constraint'))
        while True:
            op = self.maybe_keyword('and')
            if op is None:
                break

            term = self.match('constraint')

            rv.append(term)

        return rv
    
    # returns dict of query (attribute=, operator=, number_name=, return_value=)
    def constraint(self):
        query = {}

        #check if given attribute is a valid one
        query["attribute"] = self.match('attribute')

        #deals with special case of manufacter. operator has to be of == or !=
        if query["attribute"] == "manufacturer":
            op = self.keyword('of','==','!=')
        else:
            op = self.keyword('>=','<=','of','>','<','==','!=')
        

        #of opperator is similar to ==, ie 'fiber of cherios' = '(name = cherios) select fiber'
        if op == 'of':
            query["operator"] = '=='
            number_name = self.name()
            query["number_name"] = number_name
            query["return_value"] = query["attribute"]
            query["attribute"] = "name"

        #comparrison operators
        elif op in ['>','<','>=','<=','==','!=']:
            query["operator"] = op
            if query["attribute"] == "manufacturer":
                number_name = self.name()
            else:
                number_name = self.number()

            query["number_name"] = number_name
            query["return_value"] = "name"

        return query

    #if input is an attribute returns the attribute, otherwise throws error and tells user
    def attribute(self):
        return self.keyword("calories", "cups", "fiber", "manufacturer", "sugars", "rating")

    #returns name if surounded by '' returns name, otherwise throws error and tells user
    def name(self):
        chars = []
        char = (self.char('"'))

        while True:
            char = self.char()
            if char == '"':
                break

            chars.append(char)


        rv = ''.join(chars)
        return rv


    #if input is a number (can include decimal) returns nubmer, otherwise throws error and tells user
    def number(self):
        chars = []

        chars.append(self.char('0-9'))

        while True:
            char = self.maybe_char('0-9')
            if char is None:
                break

            chars.append(char)

        if self.maybe_char('.'):
            chars.append('.')
            chars.append(self.char('0-9'))

            while True:
                char = self.maybe_char('0-9')
                if char is None:
                    break

                chars.append(char)

        rv = float(''.join(chars))
        return rv



if __name__ == '__main__':
    # Initialize database
    cereal_database = init()
    print(f"Cereal Database Initialized: {cereal_database}")

    parser = CerealParser()

    user_input = ''
    while True:
        try:

            user_input = input('> ')
            if user_input.lower() == 'help':
                print("This program allows you to query cereal data. You can query by attributes such as 'calories' (int), 'cups' (int), 'fiber' (int), 'manufacturer' (string), 'sugars' (int), 'rating' (int). Use operators like '==', '>', '<', '>=' , '<=' , '!=' , 'of' to compare values. When entering a string it must be inside of double quotes. Example queries:\n"
                      "- calories > 100\n"
                      '- fiber of "Cheerios"\n'
                      "- sugars <= 5")
                continue  # Go back to the loop for more input

            if user_input.lower() == 'exit':
                break
            query_parser(parser.parse(user_input), cereal_database)
        except KeyboardInterrupt:
            print()
        except (EOFError, SystemExit):
            print()
        except (ParseError, ZeroDivisionError) as e:
            print('Error: %s' % e)

    print('Program exited successfully')