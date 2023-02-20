import tkinter as tk
import numpy as np
import random
from threading import Timer


#Still have some bugs

class App(tk.Tk):
    def __init__(self):
        self.win = super().__init__()
        self.title("Connect 4")
        self.geometry("800x650")
        self.maxsize(width=800,height=650)
        self.minsize(width=800,height=650)
        self.play_img = tk.PhotoImage(file="Files/playbut.png")
        self.unfilled_img = tk.PhotoImage(file="Files/Unfilled.png")
        self.filled_img = tk.PhotoImage(file="Files/Filled.png")
        self.dwn_img = tk.PhotoImage(file="Files/downbut.png")
        self.agent_img = tk.PhotoImage(file="Files/agentfill.png")
        self.redline_img = tk.PhotoImage(file="Files/newRedline.png")
        self.redlinemain_img = tk.PhotoImage(file="Files/redmainchk.png")
        self.redhoriz_img = tk.PhotoImage(file="Files/Redmainhoriz.png")
        self.redcounter_img = tk.PhotoImage(file="Files/redcounter.png")
        self.main_canvas = tk.Canvas(self.win,width=800,height=650,bg="black")
        self.main_canvas.grid(row=0)
        self.heading = self.main_canvas.create_text(400,100,text="Connect 4",font="Verdana 50",fill="white")
        self.play_but = tk.Button(self.win,image=self.play_img,bg = "black",borderwidth=0,command=self.screen_set)
        self.main_canvas.create_window(400,200,window=self.play_but)

    def screen_set(self):
        self.main_canvas.delete(self.heading)
        self.play_but.destroy()
        self.board_arr = np.array([0 for i in range(42)]).reshape(7,6)
        self.chk_arr = np.array(["" for i in range(42)]).reshape(7,6)
        self.agent_arr = self.chk_arr
        x_axis = 120
        y_axis = 100     
        for col in range(7):
            x_axis += 70
            for row in range(6):
                y_axis += 70
                exec(f"self.p{row}{col}=self.main_canvas.create_image(x_axis,y_axis,image=self.unfilled_img)")
            y_axis = 100        
        x_axis = 120
        for dwn_but in range(7):
            x_axis += 70
            exec(f"self.dbut{dwn_but}=tk.Button(self.win,image=self.dwn_img,bg='black',borderwidth=0,command = lambda :app.drop_piece({dwn_but}))\nself.main_canvas.create_window({x_axis},90,window=self.dbut{dwn_but})")

    def drop_piece(self,col,is_agent=False):
        for d_but in range(7):
                exec(f"self.dbut{d_but}.config(command='')")    
        for drop_ind ,drop_to in enumerate(reversed(self.board_arr[col])):    
            if not all(self.board_arr[col]):
                if drop_to == 0:
                    self.board_arr[col][5-drop_ind]=1      
                    if not is_agent:
                        self.chk_arr[col][5-drop_ind]="P"
                        self.agent_arr[col][5-drop_ind]="P"
                        exec(f"self.main_canvas.itemconfig(self.p{5-drop_ind}{col},image=self.filled_img)")
                        self.t = Timer(0.5,self.agent)
                        self.t.start()
                    else:
                        self.chk_arr[col][5-drop_ind]="A"
                        self.agent_arr[col][5-drop_ind]="A"
                        exec(f"self.main_canvas.itemconfig(self.p{5-drop_ind}{col},image=self.agent_img)")        
                    break
        self.winner_decide(self.chk_arr)    
                   
    def agent(self):
        avb_cols = []
        for col in range(7):
            if not all(self.board_arr[col]):
                avb_cols.append(col)        
        self.agent_help(avb_cols)
        try:    
            for d_but in range(7):
                exec(f"self.dbut{d_but}.config(command=lambda :app.drop_piece({d_but}))")
        except Exception:
            pass 

    def agent_help(self, avb_cols):
        try:
            for select_col in avb_cols:
                for drop_ind ,drop_to in enumerate(reversed(self.agent_arr[select_col])):    
                    if not all(self.board_arr[select_col]):
                        if drop_to == "":
                            self.agent_arr[select_col][5-drop_ind]="P"
                            if self.winner_decide(self.agent_arr,True):
                                self.agent_arr[select_col][5-drop_ind]=""
                                self.drop_piece(select_col,True)
                                return 1
                            else:
                                self.agent_arr[select_col][5-drop_ind]=""
                            break        
                   
            else:
                self.drop_piece(random.choice(avb_cols),True)
            # self.drop_piece(random.choice(avb_cols),True)
                
        except IndexError:
            print("Tie!")       

    def winner_decide(self,winner_arr,is_agent=False):
        #Vertical check
        for i in range(7):
            if list(winner_arr[i]).count("") <= 2:
                for pieces in range(3):
                    if winner_arr[i][pieces] == winner_arr[i][pieces+1] and winner_arr[i][pieces+1] == winner_arr[i][pieces+2] and winner_arr[i][pieces+2]==winner_arr[i][pieces+3]:
                        if winner_arr[i][pieces]=="P":
                            print("You Won!")
                            self.connect_pieces("v",eval(f"self.main_canvas.coords(self.p{pieces}{i})"),is_agent)
                            return True
                        elif winner_arr[i][pieces] == "A":
                            print("Agent Won!")
                            self.connect_pieces("v",eval(f"self.main_canvas.coords(self.p{pieces}{i})"),is_agent)
                            return True
                        break
        #Horizontal check            
        for i in range(4):
            for pieces in range(6):
                if winner_arr[i][pieces] == winner_arr[i+1][pieces] and winner_arr[i+1][pieces] == winner_arr[i+2][pieces] and winner_arr[i+2][pieces] == winner_arr[i+3][pieces]:
                    if winner_arr[i][pieces] == "P":
                        print("You Won!")
                        self.connect_pieces("h",eval(f"self.main_canvas.coords(self.p{pieces}{i})"),is_agent)
                        return True
                    elif winner_arr[i][pieces] == "A":
                        print("Agent Won!")
                        self.connect_pieces("h",eval(f"self.main_canvas.coords(self.p{pieces}{i})"),is_agent)
                        return True
        #Main diagonal check            
        for i in range(4):
            for pieces in range(3):
                if winner_arr[i][pieces] == winner_arr[i+1][pieces+1] and winner_arr[i+1][pieces+1] == winner_arr[i+2][pieces+2] and winner_arr[i+2][pieces+2] == winner_arr[i+3][pieces+3]:
                    if winner_arr[i][pieces] == "P":
                        print("You Won!")
                        self.connect_pieces("m",eval(f"self.main_canvas.coords(self.p{pieces}{i})"),is_agent)
                        return True
                    elif winner_arr[i][pieces] == "A":
                        print("Agent Won!")
                        self.connect_pieces("m",eval(f"self.main_canvas.coords(self.p{pieces}{i})"),is_agent)                       
                        return True            
        #Counter diagonal check     
        for i in range(4):
            for pieces in range(-1,-4,-1):
                if winner_arr[i][pieces] == winner_arr[i+1][pieces-1] and winner_arr[i+1][pieces-1] == winner_arr[i+2][pieces-2] and winner_arr[i+2][pieces-2] == winner_arr[i+3][pieces-3]:
                    if winner_arr[i][pieces] == "P":
                        print("You Won!")
                        self.connect_pieces("c",eval(f"self.main_canvas.coords(self.p{abs(pieces)+1}{i+3})"))
                        return True
                    elif winner_arr[i][pieces] == "A":
                        print("Agent Won!")
                        self.connect_pieces("c",eval(f"self.main_canvas.coords(self.p{abs(pieces)+1}{i+3})"))
                        return True

    def connect_pieces(self,direct,cord,is_agent=False):
        if not is_agent:
            for d_but in range(7):
                exec(f"self.dbut{d_but}.destroy()")
            self.t.cancel()
            if direct == "v":
                self.main_canvas.create_image( cord[0]-3,cord[1], image = self.redline_img, anchor = "nw")
            elif direct == "h":
                self.main_canvas.create_image( cord[0]-1,cord[1]-4, image = self.redhoriz_img, anchor = "nw")
            elif direct == "m":
                self.main_canvas.create_image( cord[0]-1,cord[1], image = self.redlinemain_img, anchor = "nw")
            elif direct == "c":
                self.main_canvas.create_image( cord[0],cord[1], image = self.redcounter_img, anchor = "ne")
                        
if __name__ == "__main__":
    app = App()
    app.mainloop()