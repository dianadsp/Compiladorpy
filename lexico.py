import re
import numpy as np

class analizador_lexico:
    
    reserver_words = [  "INTEGER",
                        "FLOAT",
                        "STRING",
                        "LIST",
                        "IF",
                        "ELSE",
                        "WHILE",
                        "FUNCTION",
                        "RETURN",
                        "PRINT",
                        "PLOT"]

    res_types = {
        "INTEGER"   :"t",
        "FLOAT"     :"t",
        "STRING"    :"t",
        "LIST"      :"t",
        "IF"        :"j",
        "ELSE"      :"k",
        "WHILE"     :"w",
        "FUNCTION"  :"f",
        "RETURN"    :"g",
        "PRINT"     :"p",
        "PLOT"      :"p"
     }

    delimiters = ['(',')',',',';','{','}','[',']']
    operadores_one = ['+','-','*','/','=','>','<']
    operadores_two = ['<=','>=','==','!=','+=']
    operators = operadores_one+operadores_two

    op_aritmeticos = ['+','-','*','/']
    op_comparativo = ['>','<']+operadores_two



    def __init__(self):
        pass

    def insert_spaces (self, str_code):
        #inserta espacios en delimitadores
        i = 0
        while (i<len(str_code)):
            if str_code[i] in self.delimiters:
                str_code = str_code[:i]+" "+str_code[i]+" "+str_code[i+1:]
                i +=2
            i += 1
        i = 0
        #inserta espacios en operadores de un caracter
        while (i<len(str_code)):
            if str_code[i] in self.operadores_one:
                str_code = str_code[:i]+" "+str_code[i]+" "+str_code[i+1:]
                i +=2
            i += 1   
        #junta operadores de dos caracteres
        for op in self.operadores_two:
            str_code = str_code.replace(op[0]+"  "+op[1], op)
            str_code = str_code.replace(op[0]+" "+op[1], op)
        #Separa cadena por los espacios en una lista    
        str_code = str_code.split()
        return str_code

    def split_code (self, str_code):
        p_init = 0
        p_finish = len(str_code)
        i = 0
        while i<len(str_code):
            if str_code[i] == '"':
                p_init = i
                i+=1
                break
            i+=1
        while i<len(str_code):
            if str_code[i] == '"' and str_code[i-1] != '\\':
                p_finish = i
                i+=1
                break
            i+=1
        if p_init < len(str_code)-1 and p_finish < len(str_code):
            return self.insert_spaces   (str_code[:p_init])+\
                                        [str_code[p_init:p_finish+1]]+\
                                        self.split_code(str_code[p_finish+1:])
        else:
            return self.insert_spaces (str_code)

    def detect_comment (self, str_code):
        p_init = 0
        p_finish = len(str_code)
        i = 0
        while i<len(str_code):
            if str_code[i] == '#' and str_code[i-1] != '\\':
                p_init = i
                i+=1
                break
            i+=1
        while i<len(str_code):
            if str_code[i] == '\n':
                p_finish = i
                i+=1
                break
            i+=1
        if p_init < len(str_code)-1 and p_finish < len(str_code):
            return self.split_code  (str_code[:p_init])+\
                                    [str_code[p_init:p_finish]]+\
                                    self.detect_comment(str_code[p_finish+1:])
        else:
            return self.split_code (str_code)


    def parse_code (self, list_code):
        op_code = ["ERROR"]*len(list_code)
        op_sint = ["#"]*len(list_code)
        for i, w in enumerate(list_code):
            # Busca palabras delimiters
            if w in self.delimiters:
                p_w = self.delimiters.index(w)
                op_code[i] = "DELIMITER_"+self.delimiters[p_w]
                op_sint[i] = self.delimiters[p_w] 
            # Busca palabras operators
            if w in self.operators:
                p_w = self.operators.index(w)
                op_code[i] = "OPERATOR_"+self.operators[p_w]
                if self.operators[p_w] in self.op_aritmeticos:
                    op_sint[i] = "o"
                elif self.operators[p_w] in self.op_comparativo:
                    op_sint[i] = "a"
                else:
                    op_sint[i] = self.operators[p_w]
            # parse integer
            _patron = r'^[0-9]*$'
            patron = re.compile(_patron)
            if patron.search(w):
                op_code[i] = "INTEGER"
                op_sint[i] = "n"
            # parse decimal
            _patron = r'^\d*\.\d+$'
            patron = re.compile(_patron)
            if patron.search(w):
                op_code[i] = "REAL"
                op_sint[i] = "r"
            # parse strings
            _patron = r'^"[\w\W]*"$'
            patron = re.compile(_patron)
            if patron.search(w):
                op_code[i] = "STRING"
                op_sint[i] = "l"
            # parse identificadores
            _patron = r'^[a-zA-Z][a-zA-Z0-9_]*$'
            patron = re.compile(_patron)
            if patron.search(w):
                op_code[i] = "ID_NAME"
                op_sint[i] = "i"
            # Busca palabras reservadas
            if w in self.reserver_words:
                p_w = self.reserver_words.index(w)
                op_code[i] = "RESERVER_"+self.reserver_words[p_w]
                op_sint[i] = self.res_types[self.reserver_words[p_w]]
            # parse comentarios
            _patron = r'^#[\w\W]*$'
            patron = re.compile(_patron)
            if patron.search(w):
                op_code[i] = "COMMENT"
                op_sint[i] = "#"

        return op_code,op_sint


    def search_position (self, str_code, words):
        list_pos_code = []
        if words != []:
            p_s = 0
            line = 1
            pos = 0
        
            for i in range (len(str_code)):
                if str_code[i:i+len(words[p_s])] == words[p_s]:
                    list_pos_code += [[i,line,pos]]
                    p_s += 1
                    if p_s == len(words):
                        break
                pos += 1
                if str_code[i] == '\n':
                    line += 1
                    pos = 0
        return list_pos_code

    def run (self, _str_code):
        words = self.detect_comment(_str_code)
        tokens, sintax = self.parse_code (words)
        positions = self.search_position (_str_code, words)
        return {"words":words,
                "tokens":tokens,
                "positions": positions,
                "sintax":sintax}
        
ej_code = """

INTEGER entero = 0;
FLOAT fLOAT;

FUNCTION fu&n_hola(){
    LIST INTEGER = [0,1,2];
    STRING _hola ="2H!
    $#ef
    e\\"e$";
    INTEGER i =0;
    WHILE (i<=4.5){
        PRINT (i)
        i=i+1;
        HOLA
        .025
        "3$%&#$\n%sf  df"
        '5'
    }
}

fun_hola();
"""

def main ():
    print (ej_code)
    a_lexico = analizador_lexico()
    r_lexico = a_lexico.run(ej_code)
    words = r_lexico["words"]
    positions = r_lexico["positions"]
    tokens = r_lexico["tokens"]
    for i in range(len(words)):
        print (positions[i],"->",words[i],"->",tokens[i])

if __name__ == "__main__":
    main()
