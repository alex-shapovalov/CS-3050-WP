# 
class Parser:
    def __init__(self):
        self.cache = {}

    def parse(self, text):
        self.text = text
        self.pos = -1
        self.len = len(text) - 1
        rv = self.start()
        self.assert_end()
        return rv
    
    def assert_end(self):
        if self.pos < self.len:
            raise ParseError(self.pos + 1,
            'Expected end of string but got %s',
            self.text[self.pos + 1]
            )
    
    def eat_whitespace(self):
        while self.pos < self.len and self.text[self.pos + 1] in " \f\v\r\t\n":
            self.pos += 1
    
    # Define which characters are acceptable
    def split_char_ranges(self, chars):
        # Check if chars already in cache, return if they are
        try:
            return self.cache[chars]
        except KeyError:
            pass

        rv = []
        index = 0
        length = len(chars)

        while index < length:
            # identify if chars is a range, eg 'a-c'
            if index + 2 < length and chars[index + 1] == '-':
                # first char must be less than last, so 'c-a' will raise exception
                if chars[index] >= chars[index + 2]:
                    raise ValueError('Bad character range')
                # append range to list, move to end/next range
                rv.append(chars[index:index + 3])
                index += 3
            # if not a range, add single character to list
            else:
                rv.append(chars[index])
                index += 1
        
        self.cache[chars] = rv
        return rv

    # chars = None allows us to extract a character without restricting to a specific set 
    def char(self, chars = None):
        # current position is past string length, throw exception
        if self.pos >= self.len:
            raise ParseError(
                self.pos + 1,
                'Expected %s but got end of string',
                'character' if chars is None else '[%s]' % chars
            )
        
        next_char = self.text[self.pos + 1]
        # if no restrictions, return character
        if chars == None:
            self.pos += 1
            return next_char
        # generate char range restrictions
        for char_range in self.split_char_ranges(chars):
            # if single char (not a range), check if next char matches
            if len(char_range) == 1:
                if next_char == char_range:
                    self.pos += 1
                    return next_char
            # if next char is in range, return it
            elif char_range[0] <= next_char <= char_range[2]:
                self.pos += 1
                return next_char
        # next char doesn't pass restrictions, or some other error
        raise ParseError(
            self.pos + 1,
            'Expected %s but got %s',
            'character' if chars is None else '[%s]' % chars,
            next_char
        )

    
    def keyword(self, *keywords):
        self.eat_whitespace()
        if self.pos >= self.len:
            raise ParseError(
                self.len + 1,
                'Expected %s but got end of string',
                ','.join(keywords)
            )
        # check if keyword exists in string
        for keyword in keywords:
            # define index values to check in string
            low = self.pos + 1
            high = low + len(keyword)

            # if substring within indexs matches keyword, return it
            if self.text[low:high] == keyword:
                self.pos += len(keyword)
                self.eat_whitespace()
                return keyword
        
        # doesn't match keyword, raise exception
        raise ParseError(
            self.pos + 1,
            'Expected %s but got %s',
            ','.join(keywords),
            self.text[self.pos + 1],
        )


    def match(self, *rules):
        self.eat_whitespace()
        last_error_pos = -1
        last_exception = None
        last_error_rules = []

        for rule in rules:
            initial_pos = self.pos
            try:
                rv = getattr(self, rule)()
                self.eat_whitespace()
                return rv
            except ParseError as e:
                self.pos = initial_pos

                if e.pos > last_error_pos:
                    last_exception = e
                    last_error_pos = e.pos
                    last_error_rules.clear()
                    last_error_rules.append(rule)
                elif e.pos == last_error_pos:
                    last_error_rules.append(rule)

        if len(last_error_rules) == 1:
            raise last_exception
        else:
            raise ParseError(
                last_error_pos,
                'Expected %s but got %s',
                ','.join(last_error_rules),
                self.text[last_error_pos]
            )


    
    def maybe_char(self, chars=None):
        try:
            return self.char(chars)
        except ParseError:
            return None

    def maybe_match(self, *rules):
        try:
            return self.match(*rules)
        except ParseError:
            return None

    def maybe_keyword(self, *keywords):
        try:
            return self.keyword(*keywords)
        except ParseError:
            return None
            

class ParseError(Exception):
    def __init__(self, pos, msg, *args):
        self.pos = pos
        self.msg = msg
        self.args = args
    
    def __str__(self):
        return f"{self.msg % self.args} at position {self.pos}"

