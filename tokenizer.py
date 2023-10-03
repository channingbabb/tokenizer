import re


def analyze_file(file_name):
    # Read the input file
    with open(file_name, 'r') as f:
        input_text = f.read()

    # Remove single-line comments
    input_text = re.sub(r'//.*', '', input_text)

    # Remove multi-line comments
    input_text = re.sub(r'/\*.*?\*/', '', input_text, flags=re.DOTALL)

    # Tokenize the input text
    symbols = ['(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', '/', '&', '|', '<', '>', '~']

    reserved_words = ['class', 'constructor', 'method', 'function', 'int', 'boolean', 'char', 'void', 'var', 'static', 'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']

    # Define regular expressions for various token types
    token_patterns = [
        (r'\b(?:' + '|'.join(map(re.escape, reserved_words)) + r')\b', 'keyword'),
        (r'[A-Za-z_]\w*', 'identifier'),
        (r'\d+', 'integerConstant'),
        (r'"[^"\n]*"', 'stringConstant'),
        (r'[{}()\[\].,;+\-*/&|<>=~]', 'symbol')
    ]

    # Write the output to an XML file
    output_file_name = file_name.rsplit('.', 1)[0] + '.xml'
    with open(output_file_name, 'w') as f:
        f.write('<tokens>\n')
        for line in input_text.splitlines():
            line = line.strip()
            if not line:
                continue
            token = ''
            while line:
                for pattern, token_type in token_patterns:
                    match = re.match(pattern, line)
                    if match:
                        token = match.group(0)
                        line = line[len(token):].strip()
                        if token_type == 'stringConstant':
                            token = token[1:-1]  # Remove surrounding double quotes
                        f.write(f'<{token_type}>{token}</{token_type}>\n')  # Remove spaces between tags
                        break
        f.write('</tokens>\n')

# Get user input for filename
file_name = input('Enter the file name: ')

# Call the analyze_file function
analyze_file(file_name)
