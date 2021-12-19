from tkinter import Button,Label
import settings
import random
import ctypes
import sys
class Cell:
    all=[]
    cell_count_label_object=None
    cell_count=settings.CELL_COUNT
    def __init__(self,x,y,is_mine=False):
        self.is_mine=is_mine
        self.is_opened=False
        self.cell_btn_object=None
        self.is_mine_candidate=False
        self.x=x
        self.y=y
        Cell.all.append(self)
    def create_btn_object(self,location):
        btn =Button(
            location,
            width=12,
            height=4,
            )
        btn.bind('<Button-1>',self.left_click_actions)# left click
        btn.bind('<Button-3>',self.right_click_actions) # right click
        self.cell_btn_object=btn
    @staticmethod
    def create_cell_count_label(location):
        lbl=Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("",30)
            )
        Cell.cell_count_label_object=lbl
        
        
    def left_click_actions(self,event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.showd_cell()
            # If Mines count is equal to the cells left count,player won
            if Cell.cell_count==settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0,'Congratulations! You won','Game Over!',0)
        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self,x,y):
        # Return a cell object based on the value of x,y
        for cell in Cell.all:
            if cell.x==x and cell.y==y:
                return cell


    
    @property
    def surrounded_cells(self):
        cells=[
            self.get_cell_by_axis(self.x-1,self.y-1),
            self.get_cell_by_axis(self.x-1,self.y),
            self.get_cell_by_axis(self.x-1,self.y+1),
            self.get_cell_by_axis(self.x,self.y-1),
            self.get_cell_by_axis(self.x+1,self.y-1),
            self.get_cell_by_axis(self.x+1,self.y),
            self.get_cell_by_axis(self.x+1,self.y+1),
            self.get_cell_by_axis(self.x,self.y+1)
            ]
        cells=[cell for cell in cells if cell is not None]
        return cells
    
    @property
    def surrounded_cells_mines_length(self):
        counter=0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter+=1
        
        return counter
        
    
        
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count-=1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}")

            # if this was a mine candidate,then for safetymwe should
            # configure the background color to SystemButtonFace
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
                )
        # Mark the cell as opened(Use is as the last line of this method)
        self.is_opened=True

    
    
    def show_mine(self):
        
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0,'You Clicked on MIne!','Game Over',0)
        sys.exit()
       
    def right_click_actions(self,event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='orange'
                )
            self.is_mine_candidate=True
        
        else:
            
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
                )
            self.is_mine_candidate=False
    
    @staticmethod
    def randomize_mines():
        picked_cells=random.sample(
            Cell.all,settings.MINES_COUNT
            )
        for picked_cell in picked_cells:
            picked_cell.is_mine=True
    
    def __repr__(self):
        return f"Cell({self.x},{self.y})"
    
