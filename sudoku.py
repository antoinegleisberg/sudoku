from random import shuffle, randint
from copy import deepcopy

def line(S,i):
    res = []
    for j in range(9):
        if S[i][j] != 0:
            res.append(S[i][j])
    return(res)

def column(S,j):
    res = []
    for i in range(9):
        if S[i][j] != 0:
            res.append(S[i][j])
    return(res)

def block(S,i,j):
    blocx = i//3
    blocy = j//3
    res = []
    for k in range(3):
        for h in range(3):
            cell = S[3*blocx+k][3*blocy+h]
            if cell != 0:
                res.append(cell)
    return(res)


def possible_numbers(S, i, j):
    if S[i][j]!=0:
        return [S[i][j]]

    res = []
    line_numbers = line(S,i)
    column_numbers = column(S,j)
    block_numbers = block(S,i,j)
    for k in range(1,10):
        if not k in line_numbers and not k in column_numbers and not k in block_numbers:
            res.append(k)
    return(res)


def next(i,j):
    if j==8:
        return(i+1,0)
    return(i,j+1)


def solve(S,i=0,j=0):
    """
    Solves the input sudoku grid S
    Returns True if the grid has a solution, False otherwise
    """
    if i == 9:
        return True
    elif S[i][j] > 0:
        x,y = next(i,j)
        return solve(S,x,y)

    L=possible_numbers(S,i,j)
    shuffle(L)
    for k in L:
        S[i][j]=k
        a,b = next(i,j)
        if solve(S,a,b):
            return True
    S[i][j]=0
    return False


def test_grid_complete(S):
    for i in range(9):
        for j in range(9):
            if S[i][j]==0:
                return False
    return True


def remove_numbers(S,n):
    """
    Parameters:
        S, List[List[int]]: the sudoku grid to remove numbers from
        n, int: how many numbers to remove from S
    """
    possible_indexes=[]
    for i in range(9):
        for j in range(9):
            if S[i][j] != 0:
                possible_indexes.append((i,j))
    shuffle(possible_indexes)
    for row, col in possible_indexes[:n]:
        S[row][col] = 0


def create_game_grid(n):
    """
    Creates a sudoku grid with n blanks
    """
    S=[[0 for i in range(9)] for j in range(9)]
    solve(S)
    remove_numbers(S,n)
    return S


def show(S):
    import tkinter as tk
    window = tk.Tk()
    window.resizable(width=False, height=False)
    window.geometry("+10+10")
    window.title("sudoku")

    clavier = None
    def entrerNb(i,j):
        nonlocal clavier
        clavier = tk.Toplevel()
        clavier.geometry("+450+50")
        for k in range(1,10):
            but = tk.Button(master=clavier, command=lambda k=k:nouvNombre(i,j,k), text=str(k))
            but.grid(row=(k-1)//3, column=(k-1)%3, ipadx=10, ipady=10)

    def nouvNombre(i,j,x):
        Scopy = deepcopy(S)
        Scopy[i][j]=x
        #print("appel nouvNb, i,j,x = ",i,j,x)
        if solve(Scopy) and x in possible_numbers(S,i,j):
            S[i][j]=x
            canvas.delete("all")
            createCanvas()
            clavier.destroy()
        else:
            print("erreur")

    def funcAide():
        i=randint(0,8)
        j=randint(0,8)
        while S[i][j]!=0:
            i=randint(0,8)
            j=randint(0,8)
        Scopy=deepcopy(S)
        solve(Scopy)
        S[i][j]=Scopy[i][j]
        canvas.delete("all")
        createCanvas()

    canvas=None
    def createCanvas():
        nonlocal canvas
        canvas = tk.Canvas(master=window, width=600, height=500, bg='white')
        canvas.grid(column=0,row=0)
        for i in range(10):
            l=2
            if i%3==0:
                l=5
            canvas.create_line(20+40*i,20,20+40*i,380,width=l)
            canvas.create_line(20,20+40*i,380,20+40*i,width=l)
        termine = True
        for i in range(9):
            for j in range(9):
                if S[i][j] != 0:
                    canvas.create_text(40+40*j,40+40*i,text=S[i][j])
                else:
                    termine = False
                    but = tk.Button(master=canvas, command=lambda i=i,j=j:entrerNb(i,j), text='', bg='white')
                    but.place(x=22+40*j,y=22+40*i,width=38,height=38)

        aide = tk.Button(master=canvas, command=funcAide, text="Hint")
        aide.place(x=500,y=300,height=40,width=70)

        if termine:
            canvas.create_text(210,420,text="Bravo !",font="Times 40", fill="red")
            aide.destroy()
    createCanvas()

    window.mainloop()


def play(n: int = 30):
    S = create_game_grid(n)
    show(S)

if __name__ == "__main__":
    play()


#surligner tous les chiffres identiques quand on clique dessus
#permettre de mettre des notes
#afficher les chiffres que l'on a tous trouvés
#compteur erreurs
#aide
