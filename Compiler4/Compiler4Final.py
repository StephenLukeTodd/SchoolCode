'''
Name: Stephen Luke Todd
Date: 2 - 6 - 2017
Project: Compiler Assignment 4. To even further extend the Pascal0 compiler by introducing the
ability to parse and generate the appropriate p-Code for the following constructs:
*Value parameters
*Reference parameters
###Fixed Getsym and eliminated argument declaration
Additions: 
>Added new reserved words.
>Increased number reserved words to 28  
>Tablevalue now has a new argument for params
>Added in LDA, STI, and LDI commands
>Added in value and reference into enter function
>Added declarations for Value and Reference
>Added in arguments tx0 for Statement, General Expression, expression, statement, factor.
>Added in params for TableValue.
>Added in arguments for enter. 
 
'''
import sys, string

norw = 28      #number of reserved words
txmax = 100   #length of identifier table
nmax = 14      #max number of digits in number
al = 10          #length of identifiers
CXMAX = 500 #maximum allowed lines of assembly code
STACKSIZE = 500
a = []
chars = []
rword = []
table = []         #symbol table
code = []         #code array
stack = [10] * STACKSIZE     #interpreter stack
global infile, outfile, ch, sym, id, num, linlen, kk, line, errorFlag, linelen, codeIndx, prevIndx, codeIndx0
#-------------values to put in the symbol table------------------------------------------------------------
class tableValue():                          
    def __init__(self, name, kind, level, adr, value, params):
        self.name = name
        self.kind = kind
        self.adr = adr
        self.value = value
        self.level = level
        self.params = params
#----------commands to put in the array of assembly code-----------------------------------------------
class Cmd():                            
    def __init__(self, line, cmd, statLinks, value):
        self.line = line
        self.cmd = cmd
        self.statLinks = statLinks
        self.value = value
#-------------function to generate assembly commands--------------------------------------------------
def gen(cmd, statLinks, value):            
    global codeIndx, CXMAX
    if codeIndx > CXMAX:
        print >>outfile, "Error, Program is too long"
        exit(0)
    x = Cmd(codeIndx, cmd, statLinks, value)
    code.append(x)
    codeIndx += 1
#--------------function to change jump commands---------------------------------------
def fixJmp(cx, jmpTo):
    code[cx].value = jmpTo
#--------------Function to print p-Code for a given block-----------------------------
def printCode():
    global codeIndx, codeIndx0
    print>>outfile
    for i  in range(codeIndx0, codeIndx):
        print >>outfile, code[i].line, code[i].cmd, code[i].statLinks, code[i].value
    prevIndx = codeIndx
#-------------Function to find a new base----------------------------------------------
def Base(statLinks, base):
    b1 = base
    while(statLinks > 0):
        b1 = stack[b1]
        statLinks -= 1
    return b1
#-------------P-Code Interpreter-------------------------------------------------------
def Interpret():
    print >>outfile, "Start PL/0"
    top = 0
    base = 1
    pos = 0
    stack[1] = 0
    stack[2] = 0
    stack[3] = 0
    while True:
        instr = code[pos]
        pos += 1
        #       LIT COMMAND
        if instr.cmd == "LIT":    
            top += 1
            stack[top] = int(instr.value)
        #       OPR COMMAND
        elif instr.cmd == "OPR":
            if instr.value == 0:         #end
                top = base - 1
                base = stack[top+2]
                pos = stack[top + 3]
            elif instr.value == 1:         #unary minus
                stack[top] = -stack[top]
            elif instr.value == 2:         #addition
                top -= 1
                stack[top] = stack[top] + stack[top+1]
            elif instr.value == 3:         #subtraction
                top -= 1
                stack[top] = stack[top] - stack[top+1]
            elif instr.value == 4:         #multiplication
                top -= 1
                stack[top] = stack[top] * stack[top+1]
            elif instr.value == 5:         #integer division
                top -= 1
                stack[top] = stack[top] / stack[top+1]
            elif instr.value == 6:         #logical odd function
                if stack[top] % 2 == 0:
                    stack[top] = 1
                else:
                    stack[top] = 0
            # case 7 n/a, used to debuge programs
            elif instr.value == 8:        #test for equality if stack[top-1] = stack[top], replace pair with true, otherwise false
                top -= 1
                if stack[top] == stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 9:         #test for inequality
                top -= 1
                if stack[top] != stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 10:         #test for < (if stack[top-1] < stack[t])
                top -= 1
                if stack[top] < stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 11:        #test for >=
                top -= 1
                if stack[top] >= stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 12:        #test for >
                top -= 1
                if stack[top] > stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 13:        #test for <=
                top -= 1
                if stack[top] <= stack[top+1]:
                    stack[top] = 1
                else:
                    stack[top] = 0
            elif instr.value == 14:        #write/print stack[top]  
                print >>outfile, stack[top],
                top -= 1
            elif instr.value == 15:        #write/print a newline
                print
        #      LOD COMMAND
        elif instr.cmd == "LOD":
            top += 1
            stack[top] = stack[Base(instr.statLinks, base) + instr.value]
        #    STO COMMAND
        elif instr.cmd == "STO":
            stack[Base(instr.statLinks, base) + instr.value] = stack[top]
            top -= 1
        #    CAL COMMAND
        elif instr.cmd == "CAL": 
            stack[top+1] = Base(instr.statLinks, base)
            stack[top+2] = base
            stack[top+3] = pos
            base = top + 1
            pos = instr.value
        #    INT COMMAND
        elif instr.cmd == "INT":
            top = top + instr.value
        #     JMP COMMAND
        elif instr.cmd == "JMP":
            pos = instr.value
        #     JPC COMMAND
        elif instr.cmd == "JPC":
            if stack[top] == instr.statLinks:
                pos = instr.value
            top -= 1
        elif instr.cmd == "CTS":
            top +=1 
            stack[top] = stack[top-1]
        #STI Command added
        elif instr.cmd == "STI": 
            stack[stack[Base(instr.statLinks, base) + instr.value]] = stack[top]
            top -= 1
        #LDI Command added
        elif instr.cmd == "LDI": 
            top += 1 
            stack[top] = stack[stack[Base(instr.statLinks, base) + instr.value]]
        #LDA Command added 
        elif instr.cmd == "LDA": 
            top += 1
            stack[top] = Base(instr.statLinks, base) + instr.value
        if pos == 0:
            break
    print "End PL/0"
#--------------Error Messages----------------------------------------------------------
def error(num):
    global errorFlag;
    errorFlag = 1
    print
    if num == 1: 
        print >>outfile, "Use = instead of :="
    elif num ==2: 
        print >>outfile, "= must be followed by a number."
    elif num ==3: 
        print >>outfile, "Identifier must be followed by ="
    elif num ==4: 
        print >>outfile, "Const, Var, Procedure, or Function must be followed by an identifier."
    elif num ==5: 
        print >>outfile, "Semicolon or comman missing"
    elif num == 6: 
        print >>outfile, "Incorrect symbol after procedure declaration."
    elif num == 7:  
        print >>outfile, "Statement expected."
    elif num == 8:
        print >>outfile, "Incorrect symbol after statment part in block."
    elif num == 9:
        print >>outfile, "Period expected."
    elif num == 10: 
        print >>outfile, "Semicolon between statements is missing."
    elif num == 11:  
        print >>outfile, "Undeclared identifier"
    elif num == 12:
        print >>outfile, "Assignment to a constant or procedure is not allowed."
    elif num == 13:
        print >>outfile, "Assignment operator := expected."
    elif num == 14: 
        print >>outfile, "call must be followed by an identifier"
    elif num == 15:  
        print >>outfile, "Call of a constant or a variable is meaningless."
    elif num == 16:
        print >>outfile, "Then expected"
    elif num == 17:
        print >>outfile, "Semicolon or end expected. "
    elif num == 18: 
        print >>outfile, "DO expected"
    elif num == 19:  
        print >>outfile, "Incorrect symbol following statement"
    elif num == 20:
        print >>outfile, "Relational operator expected."
    elif num == 21:
        print >>outfile, "Expression must not contain a procedure identifier"
    elif num == 22: 
        print >>outfile, "Right parenthesis missing"
    elif num == 23:  
        print >>outfile, "The preceding factor cannot be followed by this symbol."
    elif num == 24:
        print >>outfile, "An expression cannot begin with this symbol."
    elif num == 25:
        print >>outfile, "Constant or Number is expected."
    elif num == 26: 
        print >>outfile, "This number is too large."
    elif num == 27: 
        print >>outfile, "Else is expected."
    #Beginning of error edits
    elif num == 28: 
        print >>outfile, "Left Parenthesis missing"
    elif num == 29: 
        print >>outfile, "DOWNTO or TO expected"
    elif num == 30: 
        print >>outfile, "Number expected."
    elif num == 31: 
        print >>outfile, "Of expected."
    elif num == 32: 
        print >>outfile, "Until expected."
    elif num == 33: 
        print >>outfile, "CEND expected."
    elif num == 34:
        print >>outfile, "Colon expected."
    elif num == 35:
        print >>outfile, "Variable declared is not a constant. "
    elif num == 36: 
        print >>outfile, "Expression expected or delete the comma."
    elif num == 37: 
        print >>outfile, "Identifier expected."
    elif num == 38: 
        print >>outfile, "becomes := expected"
    elif num == 39:
        print >>outfile, "I AM A PLACEHOLDER THAT HAS CRIPPLING DEPRESSION WITH NO PURPOSE IN LIFE."
    elif num == 40: 
        print >>outfile, "Procedure/Function"
    elif num == 41:
        print >>outfile, "Outside the scope of body"
    elif num == 42: 
        print >>outfile, "Comma expected. "
    exit(0)
#---------GET CHARACTER FUNCTION-------------------------------------------------------------------
def getch():
    global  whichChar, ch, linelen, line;
    if whichChar == linelen:         #if at end of line
        whichChar = 0
        line = infile.readline()     #get next line
        linelen = len(line)
        sys.stdout.write(line)
    if linelen != 0:
        ch = line[whichChar]
        whichChar += 1
    return ch
#----------GET SYMBOL FUNCTION---------------------------------------------------------------------
def getsym():
    global charcnt, ch, al, a, norw, rword, sym, nmax, id, num
    while ch == " " or ch == "\n" or ch == "\r":
        getch()
    a = []
    if ch.isalpha():
        k = 0
        while True:
            a.append(string.upper(ch))
            getch()
            if not ch.isalnum():
                break
        id = "".join(a)
        flag = 0
        for i in range(0, norw):
            if rword[i] == id:
                sym = rword[i]
                flag = 1
        if  flag == 0:    #sym is not a reserved word
            sym = "ident"
    elif ch.isdigit():
        k=0
        num=0
        sym = "number"
        while True:
            a.append(ch)
            k += 1
            getch()
            if not ch.isdigit():
                break
        if k>nmax:
            error(30)
        else:
            num = "".join(a)
    elif ch == ':':
        getch()
        if ch == '=':
            sym = "becomes"
            getch()
        else:
            sym = "colon"
    elif ch == '>':
        getch()
        if ch == '=':
            sym = "geq"
            getch()
        else:
            sym = "gtr"
    elif ch == '<':
        getch()
        if ch == '=':
            sym = "leq"
            getch()
        elif ch == '>':
            sym = "neq"
            getch()
        else:
            sym = "lss"
    else:
        sym = ssym[ch]
        getch()
#--------------POSITION FUNCTION----------------------------
def position(tx, id):
    global  table;
    table[0] = tableValue(id, "TEST", "TEST", "TEST", "TEST", [])
    i = tx
    while table[i].name != id:
        i=i-1
    return i
#---------------ENTER PROCEDURE-------------------------------
def enter(tx, k, level, dx):
    global id, num, codeIndx;
    tx[0] += 1
    while (len(table) > tx[0]):
      table.pop()
    ###Added in arguments to pass values by array for ref and val. 
    if k == "const":
        x = tableValue(id, k, level, "NULL", num, [])
    elif k == "variable":
        x = tableValue(id, k, level, dx, "NULL", [])
        dx += 1
    elif k == "procedure":
        x = tableValue(id, k, level, dx, "NULL", [])
    elif k == "function": 
        x = tableValue(id, k, level, dx, "NULL", [])
    #Add in value and reference. 
    elif k == "val": 
        x = tableValue(id, k, level, dx, "NULL", [])
        dx += 1
    elif k == "ref": 
        x = tableValue(id, k, level, dx, "NULL", [])
        dx += 1
    table.append(x)
    return dx
#--------------CONST DECLARATION---------------------------
def constdeclaration(tx, level):
    global sym, id, num;
    if sym=="ident":
        getsym()
        if sym == "eql":
            getsym()
            if sym == "number":
                enter(tx, "const", level, "null")
                getsym()
            else:
                error(2)
        else:
            error(3)
    else:
        error(4)
#-------------VARIABLE DECLARATION--------------------------------------
def vardeclaration(tx, level, dx):
    global sym;
    if sym=="ident":
        dx = enter(tx, "variable", level, dx)
        getsym()
    else:
        error(4)
    return dx
#-------------VAL DECLARATION--------------------------------------
#Added in declarations to handle values. 
def valdeclaration(tx, level, dx):
    global sym;
    if sym=="ident":
        dx = enter(tx, "val", level, dx)
        getsym()
    else:
        error(4)
    return dx
#-------------REF DECLARATION--------------------------------------
#Added in declarations to handle reference. 
def refdeclaration(tx, level, dx):
    global sym;
    if sym=="ident":
        dx = enter(tx, "ref", level, dx)
        getsym()
    else:
        error(4)
    return dx
#-------------BLOCK-------------------------------------------------------------
def block(tableIndex, level):
    global sym, id, codeIndx, codeIndx0;
    tx = [1]
    tx[0] = tableIndex
    tx0 = tableIndex
    dx = 3
    cx1 = codeIndx
    gen("JMP", 0 , 0)
    if level > 0: 
        if sym != "semicolon" and sym != "lparen":
            error(3) #Placeholder error
        if sym == "semicolon": 
            getsym()
        elif sym == "lparen": 
            while True: 
                getsym()
                if sym != "VAL" and sym != "REF": 
                    error(39) #Placeholder error
                Var_Sym = sym 
                while True: 
                    getsym()
                    if sym != "ident": 
                        error(37)
                    if Var_Sym == "VAL": 
                        dx = valdeclaration(tx, level, dx)
                        table[tx0].params.append(False)
                    elif Var_Sym == "REF": 
                        dx = refdeclaration(tx, level, dx)
                        table[tx0].params.append(True)
                    if sym != "comma": 
                        break
                if sym != "semicolon": 
                    break
            if sym != "rparen": 
                error(22) 
            getsym()
            if sym != "semicolon": 
                error(17)
            getsym()


    #Needed to add in that to be able to interpret functions properly. 
    while sym == "PROCEDURE" or sym == "VAR" or sym == "CONST" or sym == "FUNCTION": 
        if sym == "CONST":
            while True:               #makeshift do while in python
                getsym()
                constdeclaration(tx, level)
                if sym != "comma":
                    break
            if sym != "semicolon":
                error(10);
            getsym()
        if sym == "VAR":
            while True:
                getsym()
                dx = vardeclaration(tx, level, dx)
                if sym != "comma":
                    break
            if sym != "semicolon":
                error(10)
            getsym()
        while sym == "PROCEDURE" or sym == "FUNCTION":
            #save sym to look at for a future use
            Savesym = sym 
            getsym()
            if sym == "ident":
            #Checks if Savesym is Procedure or Function
                if Savesym == "PROCEDURE": 
                    enter(tx, "procedure", level, codeIndx)
                    getsym()
                else: 
                    enter(tx, "function", level, codeIndx)
                    getsym()

            else:
                error(4)

            block(tx[0], level+ 1)
            if sym != "semicolon":
                error(10)
            getsym()
    fixJmp(cx1, codeIndx)
    if tx0 != 0:
        table[tx0].adr = codeIndx
    codeIndx0 = codeIndx
    gen("INT", 0, dx)
    statement(tx[0], level, tx0) #process tx0
    gen("OPR", 0, 0)
    #print code for this block
    printCode()
#--------------STATEMENT----------------------------------------
def statement(tx, level, tx0):
    global sym, id, num;
#can also be function
    if sym == "ident": 
        i = position(tx, id)
        if i == 0: 
            error(11)
        if table[i].kind != "variable" and table[i].kind != "function" and table[i].kind != "val" and table[i].kind != "ref" :
            error(39) 

        kind_ident = table[i].kind 
        getsym()
        if sym != "becomes": 
            error(13)
        getsym()
        expression(tx, level, tx0)
        if kind_ident ==  "variable" or kind_ident == "val": 
            gen("STO", level - table[i].level, table[i].adr)
        elif kind_ident =="function": 
            if i != tx0:
                getsym() 
                error(41)
            gen("STO", 0, -1)
        elif kind_ident == "ref": 
            gen("STI", level - table[i].level, table[i].adr)
    ##BEGIN MODIFICATIONS
    elif sym == "CALL":
        getsym()
        if sym != "ident":
            error(14)
        i = position(tx, id)
        if i==0:
            error(11)
        if table[i].kind != "procedure":
            error(15)
        getsym()
        if sym == "lparen": 
            p = 0
            gen("INT", 0, 3)
            while True: 
                getsym()
                if table[i].params[p]:
                    if sym == "ident": 
                        j = position(tx, id)
                        #Set j = to position to prevent variable conflictions
                        if table[j].kind == "variable" or table[j].kind == "val": 
                            gen("LDA", level-table[j].level, table[j].adr)
                        elif table[j].kind == "ref": 
                            gen("LOD", level-table[j].level, table[j].adr)
                    else: 
                        error(39)
                    getsym()
                else: 
                    expression(tx, level, tx0)
                p += 1
                if sym != "comma": 
                    break
            if sym != "rparen":  
                error(39)
            getsym()
            gen("INT", 0, -1*(3+p))
        gen("CAL", level - table[i].level, table[i].adr)
        ###END MODIFICATIONS
    elif sym == "IF":
        getsym()
        GeneralExpression(tx, level, tx0)

        cx1 = codeIndx
        gen("JPC", 0, 0)
       
        if sym != "THEN":
            error(16)
        getsym()
        #Pass tx(n)
        statement(tx, level, tx0) #Added ability to pass 

        if sym == "ELSE":
            getsym()
            cx2 = codeIndx
            gen("JMP", 0,0)
            fixJmp(cx1, codeIndx)
            #Pass tx(n)
            statement(tx, level, tx0)
            fixJmp(cx2, codeIndx)
        else: 
            fixJmp(cx1, codeIndx)
	###Imported Else

    elif sym == "BEGIN":
        while True:
            getsym()
            statement(tx, level, tx0)
            if sym != "semicolon":
                break
        if sym != "END":
            error(17)
        getsym()

    elif sym == "WHILE":
        getsym()
        cx1 = codeIndx
        GeneralExpression(tx, level, tx0)
        cx2 = codeIndx
        gen("JPC", 0, 0)
        if sym != "DO":
            error(18)
        getsym()
        #Pass tx(n)
        statement(tx, level, tx0)
        
        gen("JMP", 0, cx1)
        fixJmp(cx2, codeIndx)

###Imported REPEAT
    elif sym == 'REPEAT':
        cx1 = codeIndx
        while True:
            getsym()
            #Pass tx(n)
            statement(tx, level, tx0)
            if sym != 'semicolon':
                break
        if sym != 'UNTIL':
            error(29)
        getsym()
        GeneralExpression(tx, level, tx0)

        gen("JPC", 0, cx1)

###Imported FOR
    
    elif sym == "FOR":
        getsym()
        if sym != 'ident':
            error(37)
        i = position(tx, id)
        if i==0:
            error(11)
        if table[i].kind != "variable":
            error(12)
        getsym()
        if sym != 'becomes':
            error(38) 
        getsym()
        expression(tx, level, tx0)

        gen("STO", level-table[i].level, table[i].adr)

        if sym != 'DOWNTO' and sym != 'TO':
            error(29)
        SymFor = sym
        
        getsym()
        expression(tx, level, tx0)
        
        cx1 = codeIndx
        gen("CTS", 0, 0)
        gen("LOD", level - table[i].level, table[i].adr)
        if SymFor == 'TO': 
            gen("OPR", 0, 11) ###GREATER THAN OR EQUAL TO OPERATION
        elif SymFor == 'DOWNTO': 
            gen("OPR", 0, 13) ###LESSTHAN OR EQUAL TO OPERATION
        cx2 = codeIndx
        gen("JPC", 0, 0)

        if sym != 'DO':
            error(1)
        getsym()
        statement(tx, level, tx0)

        gen("LOD", level - table[i].level, table[i].adr)
        gen("LIT", 0, 1)
        if SymFor == 'TO': 
            gen("OPR", 0, 2) ###ADDITION OPERATION
        elif SymFor == 'DOWNTO': 
            gen("OPR", 0, 3) ###SUBTRACTION OPERATION
        gen("STO", level-table[i].level, table[i].adr)
        gen("JMP", 0, cx1)
        fixJmp(cx2, codeIndx)
        gen("INT", 0, -1)
    
###Imported CASE

    elif sym == "CASE":
        getsym()
        expression(tx, level, tx0)
        if sym != "OF": 
            error(31)
        Case_Counter = 0
        while True: 
            Case_Counter = Case_Counter + 1
            getsym()
            if sym != "number" and sym != "ident": 
                break 

            gen("CTS", 0, 0)

            if sym == "ident":
                i = position(tx, id)
                if i == 0: 
                    error(11)
                elif table[i].kind != "const": 
                    error(25)
                else: 

                    gen("LIT", 0, table[i].value)

            elif sym == "number": 
                gen("LIT", 0, num)
            
            getsym()

            gen("OPR", 0, 8)
            cx1 = codeIndx
            gen("JPC", 0, 0)

            if sym != "colon":
                error(34)
            getsym()
            
            statement(tx, level, tx0)
            if sym != "semicolon": 
                error(17)

            if Case_Counter == 1: 
                cx2 = codeIndx
                gen("JMP", 0, 0)
            else: 
                gen("JMP", 0, cx2)
            fixJmp(cx1, codeIndx)

        if sym != 'CEND':
            error(33)
        getsym()
        
        fixJmp(cx2, codeIndx)
        gen("INT", 0, -1)
        
###Imported WRITE
    elif sym == "WRITE":
        sym1 = sym  
        getsym()
        if sym != 'lparen': 
            error(28)
        while True: 
            getsym()
            expression(tx, level, tx0)
            gen("OPR", 0, 14)
            if sym != 'comma': 
                break
        if sym != 'rparen': 
            error(22)
        getsym()
        if sym1 == "WRITELN": 
            gen("OPR", 0, 15)

    elif sym == "WRITELN":
        sym1 = sym  
        getsym()
        if sym != 'lparen': 
            error(28)
        while True: 
            getsym()
            expression(tx, level, tx0)
            gen("OPR", 0, 14)
            if sym != 'comma': 
                break
        if sym != 'rparen': 
            error(22)
        getsym()
        if sym1 == "WRITELN": 
            gen("OPR", 0, 15)

#--------------EXPRESSION--------------------------------------
#Working
def expression(tx, level, tx0):
    global sym;
    if sym == "plus" or sym == "minus": 
        addop = sym
        getsym()
        term(tx, level, tx0)
        if (addop == "minus"):         #if minus sign, do negate operation
            gen("OPR", 0, 1)
    else:
        term(tx, level, tx0)
    
    while sym == "plus" or sym == "minus" or sym == "OR":
        addop = sym
        getsym()
        term(tx, level, tx0)
        
             #subtract operation
        #Add in case for minus. 
        if(addop == "minus"): 
            gen("OPR", 0, 3)
        else: 
            gen("OPR", 0, 2)

#-------------TERM----------------------------------------------------
#Working
def term(tx, level, tx0):
    global sym;
    factor(tx, level, tx0)
    while sym=="times" or sym=="slash" or sym == "AND":
        mulop = sym
        getsym()
        factor(tx, level, tx0)
            #divide operation
        #Add in case for divide. 
        if mulop == "slash": 
            gen("OPR", 0, 5)
        else: 
            gen("OPR", 0, 4)

#-------------FACTOR--------------------------------------------------
def factor(tx, level, tx0):
    global sym, num, id;
    #can also be a val or ref
    if sym == "ident":
        i = position(tx, id)
        if i==0:
            error(11)
        if table[i].kind == "const":
            gen("LIT", 0, table[i].value)
        elif table[i].kind == "variable" or table[i].kind == "val":
            gen("LOD", level-table[i].level, table[i].adr)
        elif table[i].kind == "ref":
            gen("LDI", level-table[i].level, table[i].adr)
        elif table[i].kind == "procedure" or table[i].kind == "function":
            error(39)
        getsym()
    elif sym == "number":
        gen("LIT", 0, num)
        getsym()
    elif sym == "lparen":
        getsym()
        GeneralExpression(tx, level, tx0)
        if sym != "rparen":
            error(22)
        getsym()

    #CALL method
    elif sym == "CALL":
        getsym()
        if sym != "ident":
          error(14)
        i = position(tx, id)
        if i==0:
          error(11)
        if table[i].kind != "function":
          error(39)
        getsym()
        gen("INT", 0, 1)
        if sym == "lparen":
            p = 0
            gen("INT", 0, 3)
            while True:
                getsym()
                if table[i].params[p]:
                    if sym == "ident":
                        #Target cases accounted for. 
                        j = position(tx,id)
                        if table[j].kind == "variable" or table[j].kind == "val":
                            gen("LDA", level - table[j].level, table[j].adr)
                        elif table[j].kind == "ref":
                            gen("LOD", level - table[j].level, table[j].adr)
                    else:
                        error(39)
                    getsym()
                else:
                    expression(tx, level, tx0)
                p+=1
                if sym != "comma":
                    break
            if sym != "rparen":
                error(22)
            getsym()
            gen("INT", 0, -1*(3+p))
        gen("CAL",level - table[i].level, table[i].adr)

    #add not to factor
    elif sym == "NOT":
        getsym()
        factor(tx,level, tx0)
        gen("LIT", 0, 0)
        gen("OPR", 0, 8)
    else:    
        error(24)    
#-----------GeneralExpression-------------------------------------------------
def GeneralExpression(tx, level, tx0):
    #renamed from condition
    global sym;
    if sym == "ODD":
        getsym()
        expression(tx, level, tx0)
        gen("OPR", 0, 6)
    else:
        expression(tx, level, tx0)
        temp = sym
        if (temp in ["eql","neq","lss","leq","gtr","geq"]):
            #error(20)
            
            getsym()
            expression(tx, level, tx0)
            if temp == "eql":
                gen("OPR", 0, 8)
            elif temp == "neq":
                gen("OPR", 0, 9)
            elif temp == "lss":
                gen("OPR", 0, 10)
            elif temp == "geq":
                gen("OPR", 0, 11)
            elif temp == "gtr":
                gen("OPR", 0, 12)
            elif temp == "leq":
                gen("OPR", 0, 13)
#-------------------MAIN PROGRAM------------------------------------------------------------#
rword.append('AND') 
rword.append('BEGIN')
rword.append('CALL')
rword.append('CASE')
rword.append('CEND')
rword.append('CONST')
rword.append('DO')
rword.append('DOWNTO')
rword.append('ELSE')
rword.append('END')
rword.append('FOR')
rword.append('FUNCTION') 
rword.append('IF')
rword.append('NOT') 
rword.append('ODD')
rword.append('OF')
rword.append('OR') 
rword.append('PROCEDURE')
rword.append('REF') #*
rword.append('REPEAT')
rword.append('THEN')
rword.append('TO')
rword.append('UNTIL')
rword.append('VAL') #*
rword.append('VAR')
rword.append('WHILE')
rword.append('WRITE')
rword.append('WRITELN')
#Words added in were Val and Ref. 

#Added NOT, OR, AND, FUNCTION
ssym = {'+' : "plus",
             '-' : "minus",
             '*' : "times",       
             '/' : "slash",
             '(' : "lparen",
             ')' : "rparen",
             '=' : "eql",
             ',' : "comma",
             '.' : "period",
             '#' : "neq",
             '<' : "lss",
             '>' : "gtr",
             '"' : "leq",
             '@' : "geq",
             ';' : "semicolon",
             ':' : "colon",
             }
charcnt = 0
whichChar = 0
linelen = 0
ch = ' '
kk = al                
a = []
id= '     '
errorFlag = 0
table.append(0)    #making the first position in the symbol table empty
sym = ' '       
codeIndx = 0         #first line of assembly code starts at 1
prevIndx = 0
infile =    sys.stdin       #path to input file
outfile =  sys.stdout     #path to output file, will create if doesn't already exist

getsym()            #get first symbol
block(0, 0)             #call block initializing with a table index of zero
if sym != "period":      #period expected after block is completed
    error(9)
print  
if errorFlag == 0:
    print >>outfile, "Successful compilation!\n"
    
Interpret()
