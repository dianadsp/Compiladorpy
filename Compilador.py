
import lexico
import sintactico
import tkinter as tk
from tkinter.font import Font



s_code = """
#Esto es un comentario
&Esto _es %un $ERROR

FLOAT max_count = 10.0;
INTEGER max_tabla = 200;
STRING str_p = "Hola Mundo";
LIST L_tabla = [100,"Adios",max_tabla,3.14];

"""


s_code2 = """
#Esto es un comentario
&Esto _es %un $ERROR

FLOAT max_count = 10.0;
FLOAT max_tabla = 12.1;

FUNCTION tabla_multi(FLOAT max_c, FLOAT max_t){
    INTEGER i = 0;
    INTEGER J = 0;
    WHILE (i<=max_c){
        WHILE (J<=max_t){
            PRINT (i," X ",j,"=",i*j);
            j=j+1;
        }
        PRINT ("\\n");
        i = i+1;
    }
}

tabla_multi(max_count, max_tabla);
"""

class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, scroll, **kwargs):
        super().__init__(master, **kwargs)
 
        self.text_widget = text_widget
        self.text_widget.bind('<KeyPress>', self.on_key_release)
        scroll.bind('<B1-Motion>', self.on_key_release)
        self.text_widget.bind('<FocusIn>', self.on_key_release)
        self.text_widget.bind('<MouseWheel>', self.on_key_release)
 
        self.insert(1.0, '1')
        self.configure(state='disabled')
 
    def on_key_release(self, event=None):
        p, q = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index("end"))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))
 
        self.configure(state='normal', width=width, bd=3,
                       height=30, bg="#17202A", fg='#AED6F1')
        self.delete(1.0,"end")
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')


# create a Pad class
class Pad(tk.Frame):
  
    # constructor to add buttons and text to the window
    def __init__(self, _lexico, parent, *args, **kwargs):
        self.lexico = _lexico
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
  
        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side="top",anchor="nw")

        # adding the text 
        self.text = tk.Text(self, bg="#2B2B2C", fg='#FFFFFF', bd=3, 
                            insertbackground="white",height=30, width=65)
        self.text.insert("end", s_code)
        self.text.focus()

        self.text.pack(padx=3, fill="both", expand=True, side="left")
        self.text.bind("<KeyRelease>", self.exe_lexico)

        self.scrollbary = tk.Scrollbar(self)
        self.scrollbary.pack(side='left', fill='y')

        #configuring a tag called start
        self.text.tag_configure("commet", foreground="#99A3A4")
        self.text.tag_configure("reserver", foreground="#68B1E1")
        self.text.tag_configure("delimiter", foreground="red")
        self.text.tag_configure("operator", foreground="#616FFF")
        self.text.tag_configure("string", foreground="#6AAA0F")
        self.text.tag_configure("integer", foreground="#C7F487")
        self.text.tag_configure("real", foreground="#8FEED8")
        self.text.tag_configure("null", background="red",foreground="white")

        
        self.text.config(yscrollcommand=self.scrollbary.set)
        self.scrollbary.config(command=self.text.yview)
        
        self.line = LineNumbers(parent, self.text,self.scrollbary, width=1)
        self.line.pack(side="left",anchor="s",fill="y", expand=True)
        #self.line.config(yscrollcommand=self.scrollbary.set)

        self.scrollbar2 = tk.Scrollbar(self)
        self.scrollbar2.pack(side='right', fill='y')

        self.text2 = tk.Text(self,height=30, width=40, bg="#2B2B2C", fg='#FFFFFF')
        self.text2.focus()
        self.text2.pack(fill="both",expand=True, side="right")
        self.text2.config(yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.text2.yview)

        self.text2.tag_configure("string", foreground="#6AAA0F")
        self.text2.tag_configure("token", foreground="#616FFF")
        self.text2.tag_configure("null", background="red",foreground="white")
        self.exe_lexico_event()


    def gen_finish_pos (self,word, init_line, init_pos):
        pos = init_pos
        line = init_line
        for w in word:
            if w == '\n':
                line += 1
                pos=0
            else:
                pos+=1
        return line,pos

    def exe_lexico(self, event):
        self.line.on_key_release()
        self.clear()
        s_code = self.text.get("1.0","end")
        r_lexico = self.lexico.run(s_code)
        words = r_lexico["words"]
        positions = r_lexico["positions"]
        tokens = r_lexico["tokens"]
        sintax = r_lexico["sintax"]
        str_expr = "".join(sintax).replace("#","")+"$"
        sintactico.main (str_expr)
        print ("Expresion Sintactica:", str_expr,"\n\n")

        self.text2.config(state="normal")
        self.text2.delete("1.0","end")
        self.text2.insert("end", "Resultado de Analizador Lexico:\n\n")

        pos_str = 3
        for i in range(len(words)):
            #print (positions[i],"->",words[i],"->",tokens[i])
            self.text2.insert("end", str(positions[i][1])+","+str(positions[i][2])+"|"+words[i]+"|->"+tokens[i]+"\n")
            init_p = len(str(positions[i][1]))+len(str(positions[i][2]))+2
            init_str2 = str(pos_str)+'.'+str(init_p)

            fline, fpos = self.gen_finish_pos (words[i],pos_str,init_p)
            pos_str = fline+1
            end_p = init_p+len(words[i])
            end_str2 =  str(fline)+'.'+str(fpos)

            self.text2.tag_add('string',init_str2 , end_str2)

            init_str2 = str(fline)+'.'+str(fpos+3)
            end_str2 =  str(fline)+'.'+str(fpos+3+len(tokens[i]))
            if tokens[i] != "ERROR":
                self.text2.tag_add('token',init_str2 , end_str2)
            else:
                self.text2.tag_add('null',init_str2 , end_str2)

            init_str = str(positions[i][1])+'.'+str(positions[i][2])
            end_str =  str(positions[i][1])+'.'+str(positions[i][2]+len(words[i]))
            if tokens[i][:4] == 'RESE':
                self.text.tag_add('reserver',init_str , end_str)
            if tokens[i][:4] == 'DELI':
                self.text.tag_add('delimiter',init_str , end_str)
            if tokens[i][:4] == 'OPER':
                self.text.tag_add('operator',init_str , end_str)
            if tokens[i][:4] == 'INTE':
                self.text.tag_add('integer',init_str , end_str)
            if tokens[i][:4] == 'REAL':
                self.text.tag_add('real',init_str , end_str)
            if tokens[i][:4] == 'NULL':
                self.text.tag_add('null',init_str , end_str)
            if tokens[i][:4] == 'COMM':
                self.text.tag_add('commet',init_str , end_str)
            if tokens[i][:4] == 'STRI':
                init_str = str(positions[i][1])+'.'+str(positions[i][2])
                fline, fpos = self.gen_finish_pos(words[i],positions[i][1],positions[i][2])
                end_str = str(fline)+'.'+str(fpos)
                self.text.tag_add('string',init_str , end_str)
        self.text2.config(state="disabled")

    def exe_lexico_event(self):
        self.exe_lexico("")

    # Metodo para limpiar los tags
    def clear(self):
        self.text.tag_remove("reserver",  "1.0", 'end')
        self.text.tag_remove("delimiter",  "1.0", 'end')
        self.text.tag_remove("operator",  "1.0", 'end')
        self.text.tag_remove("string",  "1.0", 'end')
        self.text.tag_remove("char",  "1.0", 'end')
        self.text.tag_remove("integer",  "1.0", 'end')
        self.text.tag_remove("real",  "1.0", 'end')
        self.text.tag_remove("null",  "1.0", 'end')
        self.text.tag_remove("commet",  "1.0", 'end')


def main():
    root = tk.Tk()
    root.title("Compilador de Diana Patiño")  #Cambiar titulo
    root.iconbitmap("icono.ico") #Cambiar el icono
    a_lexico = lexico.analizador_lexico()
    Pad(a_lexico, root).pack(expand=1, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main()
