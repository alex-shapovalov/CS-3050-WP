from parser import Parser
from parser import ParseError

class CerealParser(Parser):
    def start(self):
        return self.expression()

    # return list of tuples  [(,,),(,,)]
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
# calories >= 140
# fiber of "Cherios"   (name, ==, "cherios") select fiber
    # returns tuple (attribute, operator, number/name)
    def constraint(self):
        query = {}

        query["attribute"] = self.match('attribute')

        if query["attribute"] == "manufacturer":
            op = self.keyword('of','==','!=')
        else:
            op = self.keyword('>=','<=','of','>','<','==','!=')
        

        if op == 'of':
            query["operator"] = '=='
            number_name = self.name()
            query["number_name"] = number_name
            query["return_value"] = query["attribute"]
            query["attribute"] = "name"

        elif op in ['>','<','>=','<=','==','!=']:
            query["operator"] = op
            if query["attribute"] == "manufacturer":
                number_name = self.name()
            else:
                number_name = self.number()

            query["number_name"] = number_name
            query["return_value"] = "name"



        return query

    
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

    def attribute(self):
        return self.keyword("calories", "cups", "fiber", "manufacturer", "sugars", "rating")



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
    parser = CerealParser()

    while True:
        try:
            print(parser.parse(input('> ')))
        except KeyboardInterrupt:
            print()
        except (EOFError, SystemExit):
            print()
            break
        except (ParseError, ZeroDivisionError) as e:
            print('Error: %s' % e)