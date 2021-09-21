import re


s_code = """

INTEGER entero = 0;
FLOAT fLOTANTE;

FUNCTION fun_hola(){
    LIST INTEGER = [0,1,2];
    STRING hola ="Hola";
    INTEGER i =0;
    WHILE (i<=4.5){
        PRINT (i)
        i=i+1;
    }
}

fun_hola();

"""

reserver_words = [  "INTEGER",
                    "FLOAT",
                    "CHAR",
                    "STRING",
                    "LIST",
                    "IF",
                    "ELSE",
                    "WHILE",
                    "FUNCTION",
                    "PRINT"]

delimiters = ['(',')',',',';','{','}','[',']']
operadores_one = ['+','-','*','/','=','>','<']
operadores_two = ['<=','>=','==','!=']
operators = operadores_one+operadores_two

def split_code (str_code):
    #inserta espacios en delimitadores
    i = 0
    while (i<len(str_code)):
        if str_code[i] in delimiters:
            str_code = str_code[:i]+" "+str_code[i]+" "+str_code[i+1:]
            i +=2
        i += 1
    i = 0
    #inserta espacios en operadores de un caracter
    while (i<len(str_code)):
        if str_code[i] in operadores_one:
            str_code = str_code[:i]+" "+str_code[i]+" "+str_code[i+1:]
            i +=2
        i += 1   
    #junta operadores de dos caracteres
    for op in operadores_two:
        str_code = str_code.replace(op[0]+"  "+op[1], op)
        str_code = str_code.replace(op[0]+" "+op[1], op)

    return str_code.split()

def parse_code (list_code):
    op_code = ["NULL"]*len(list_code)
    # parse identificadores
    for i, w in enumerate(list_code):
        _patron = r'\w+'
        patron = re.compile(_patron)
        if patron.search(w):
            op_code[i] = "ID"
    # Busca palabras reservadas
    for i, w in enumerate(list_code):
        if w in reserver_words:
            p_w = reserver_words.index(w)
            op_code[i] = "RESERVER_"+reserver_words[p_w]
    # Busca palabras delimiters
    for i, w in enumerate(list_code):
        if w in delimiters:
            p_w = delimiters.index(w)
            op_code[i] = "DELIMITER_"+delimiters[p_w]
    # Busca palabras operators
    for i, w in enumerate(list_code):
        if w in operators:
            p_w = operators.index(w)
            op_code[i] = "OP_"+operators[p_w]
    # parse integer
    for i, w in enumerate(list_code):
        _patron = r'\d+'
        patron = re.compile(_patron)
        if patron.search(w):
            op_code[i] = "INTEGER"
    # parse decimal
    for i, w in enumerate(list_code):
        _patron = r'\d*\.\d+'
        patron = re.compile(_patron)
        if patron.search(w):
            op_code[i] = "DECIMAL"
    # parse strings
    for i, w in enumerate(list_code):
        _patron = r'"\w+"'
        patron = re.compile(_patron)
        if patron.search(w):
            op_code[i] = "STRING"


    return op_code 
    
   
words = split_code(s_code)
tokens = parse_code (words)

print (s_code)

for i in range(len(words)):
    print (words[i],"->",tokens[i])



