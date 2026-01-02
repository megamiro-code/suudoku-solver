import tkinter as tk
from tkinter import ttk
import numpy as np
import random

class Sudoku(tk.Frame):

    def __init__(self,master):
        super().__init__(master)

        self.frame1=tk.Frame(master,relief="raised",background="#000000",pady=5,padx=5)
        self.frame2=tk.Frame(master,relief="raised",background="#FFFFFF",pady=5,padx=5)
        self.frame1.place(x=0,y=0,width=648,height=649)
        self.frame2.place(x=648,y=0,width=1000,height=700)
        self.base_matrix = np.array([ [0 for i in range(9)] for j in range(9)])
        self.create_widged()
        self.calculate_flag=True
        self.tentative_matrixs=[]
        self.judge_matrixs=[]
        self.text=""
        self.no_answer_flag=False
        self.clear=False

    #ボタン類の作成
    def create_widged(self):
        #radiobuttonの設置
        self.Ivar = tk.IntVar()
        self.Ivar.set(0)
        for i in range(10):
            if i==0:
                radiobutton=tk.Radiobutton(self.frame2,variable=self.Ivar,text ="クリア",value=i,background="#F0F0F0")
            else:
                radiobutton=tk.Radiobutton(self.frame2,variable=self.Ivar,text =f"{i}を入力",value=i,background="#F0F0F0")
            radiobutton.place(x=0, y=i*50+50,width=80, height=40)

        #buttonの設置
        for i in range(9):
            for j in range(9):
                button = tk.Button(self.frame1,width=8, height=4, text="",font=("",50))
                button_func=self.which_number(i,j,button)
                button.place(x=65*i+(i//3)*3+45,y=65*j+(j//3)*3+45,width=65, height=65)
                button.config(command=button_func)

        #行ラベルの設置
        for i in range(9):
            self.column_label = tk.Label(self.frame1, text=f"{i+1}",font=("",25),background="#FFFFFF")
            self.column_label.place(x=65*i+(i//3)*3+45,y=2,width=64, height=41)
        
        #列ラベルの設置
        for i in range(9):
            self.row_label = tk.Label(self.frame1, text=f"{i+1}",font=("",25),background="#FFFFFF")
            self.row_label.place(y=65*i+(i//3)*3+45,x=2,width=41, height=64)

        
        #計算ボタンの設定    
        calculate_button = tk.Button(self.frame2, text="計算開始",font=("",25),command=self.calculate,background="#AAAAFF")
        calculate_button.place(x=0, y=550,width=200, height=80)

        #解答マップの設置背景
        self.map_label = tk.Label(self.frame2,width=8, height=4, text="",font=("",25),background="#000000")
        self.map_label.place(x=215,y=105,width=300, height=300)

        #解答マップ設置
        for i in range(9):
            for j in range(9):
                text=self.base_matrix[j,i]
                if text==0:
                    text=""
                self.map_label = tk.Label(self.frame2,width=8, height=4, text=f"{text}",font=("",25),background="#FFFFFF")
                self.map_label.place(x=31*i+(i//3)*3+223,y=31*j+(j//3)*3+113,width=30, height=30)

        #注意ラベルの設置
        self.warning_label = tk.Label(self.frame2,width=8, height=4, text="※ドラッグすると正しく入力されません",font=("",10),background="#FFFFFF",anchor="w")
        self.warning_label.place(x=0,y=10,width=300, height=25)

        #自由ラベルの設置
        self.free_label= tk.Label(self.frame2,width=8, height=4, text="",font=("",15),background="white")
        self.free_label.place(x=150,y=450,width=400, height=50)


    def free_label_apdate(self,text,color):
        self.free_label= tk.Label(self.frame2,width=8, height=4, text=text,font=("MSゴシック",20),background="#FFFFFF",foreground=color)
        self.free_label.place(x=150,y=450,width=400, height=50)

    #マップラベルの更新
    def map_label_apdate(self,matrix):
        for i in range(9):
            for j in range(9):
                text=matrix[j,i]
                if text==0:
                    text=""
                self.map_label = tk.Label(self.frame2,width=8, height=4, text=f"{text}",font=("",25),background="#FFFFFF")
                self.map_label.place(x=31*i+(i//3)*3+223,y=31*j+(j//3)*3+113,width=30, height=30)
        
    #ボタンの判別およびテキスト変更
    def which_number(self,i,j,button):
        def x():
            self.base_matrix[j,i]=self.Ivar.get()
            if self.Ivar.get()!=0:
                button.config(text=self.Ivar.get())
            else:
                button.config(text="")
            #計算前はbase計算後はanswer
            if self.calculate_flag:
                self.map_label_apdate(self.base_matrix)
            else:
                self.answer_matrix=np.copy(self.base_matrix)
                self.map_label_apdate(self.answer_matrix)
        return x

    #任意の場所に入りうる値の取得
    def search_possible_number(self,c,r,matrix):
        column = matrix[c,:]
        row = matrix[:,r]
        box = matrix[(c//3)*3:((c//3)+1)*3,(r//3)*3:((r//3)+1)*3]
        box_v = box.reshape(-1)
        possible_list=[i+1 for i in range(9)]
        for i in range(9):
            if i+1 in column or i+1 in row or i+1 in box_v:
                possible_list.remove(i+1)
        return possible_list

    #唯一的に値が入る場合その値の決定
    def conclude_number(self):
        for i in range(9):
            count_list=[]
            # print(self.judge_matrix[i,:],"self.judge_matrix[i,:]")
            # print(type(self.judge_matrix[i,:]),"type self.judge_matrix[i,:]")
            for num,p_list in enumerate(self.judge_matrix[i,:]):
                #print(p_list,"p_list1")
                count_list+=[num for j in range(len(p_list))]
            column=np.array(sum(self.judge_matrix[i,:].tolist(),[]))
            unique_column, counts = np.unique(column, return_counts=True)
            if 1 in counts:
                for number in unique_column[counts==1]:
                    change_index=count_list[int(np.where(column==number)[0][0])]
                    self.tentative_matrix[i,change_index]=number
                    #print(f"{i+1}行、{change_index+1}列を{number}に置換 行")
                return True

        for i in range(9):
            count_list=[]
            # print(self.judge_matrix[:,i],"self.judge_matrix[:,i]")
            # print(type(self.judge_matrix[:,i]),"tyepe self.judge_matrix[:,i]")
            for num,p_list in enumerate(self.judge_matrix[:,i]):
                #print(p_list,"p_list2")
                count_list+=[num for j in range(len(p_list))]
            row=np.array(sum(self.judge_matrix[:,i].tolist(),[]))
            unique_row, counts = np.unique(row, return_counts=True)
            if 1 in counts:
                for number in unique_row[counts==1]:
                    change_index=count_list[int(np.where(row==number)[0][0])]
                    self.tentative_matrix[change_index,i]=number
                    #print(f"{change_index+1}行、{i+1}列を{number}に置換 列")
                return True
            
        for i in range(3):
            for j in range(3):
                # print(self.judge_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1),"self.judge_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1)")
                # print(type(self.judge_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1)),"type self.judge_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1)")
                count_list=[]
                for num,p_list in enumerate(self.judge_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1)):
                    #print(p_list,"p_list3")
                    count_list+=[num for j in range(len(p_list))]
                box=np.array(sum(self.judge_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1).tolist(),[]))
                unique_box, counts = np.unique(box, return_counts=True)
                if 1 in counts:
                    for number in unique_box[counts==1]:
                        change_index=count_list[int(np.where(box==number)[0][0])]
                        self.tentative_matrix[i*3+change_index//3,j*3+change_index%3]=number
                        #print(f"{(i*3+change_index//3)+1}行、{(j*3+change_index%3)+1}列を{number}に置換 BOX")
                    return True
        return False
    
    #行列を埋める関数
    def fill_number(self):
        self.clear=False
        new_tentative_matrixs2=[]
        new_judge_matrixs2=[]
        for matrix in self.tentative_matrixs:
            self.tentative_matrix=np.copy(matrix)
            flag=True
            zero_possible_flag=False
            while flag:
                possible_found_flag=True
                self.judge_matrix=[[[10 for i in range(10)] for i in range(9)] for j in range(9)]
                c_array=np.where(self.tentative_matrix==0)[0]
                r_array=np.where(self.tentative_matrix==0)[1]
                # print(c_array,"c_array")
                # print(r_array,"r_array")
                for c,r in zip(c_array,r_array):
                    result=self.search_possible_number(c,r,self.tentative_matrix)
                    self.judge_matrix[c][r]=result
                    if result==[]:
                        zero_possible_flag=True
                        print(f"{c+1}行、{r+1}列にどの数字も挿入できないため行列が削除されました")
                        print(self.tentative_matrix)     
                        break 
                    if len(result)==1:
                        self.tentative_matrix[c,r]=result[0]
                        #print(f"{c+1}行、{r+1}列を{result[0]}に置換")
                        possible_found_flag=False
                if zero_possible_flag:
                    break
                #ここは全部埋まっていたら正解としているが改良が不必要やんけ
                if self.judge_matrix == [[[10 for i in range(10)] for i in range(9)] for j in range(9)]:   
                    self.answer_matrix=np.copy(self.tentative_matrix)
                    self.clear=True
                    break
                if possible_found_flag:
                    self.judge_matrix=np.array(self.judge_matrix,dtype=object)
                    flag=self.conclude_number()
            if self.clear:
                break
            if zero_possible_flag==False:
                new_tentative_matrixs2.append(self.tentative_matrix)
                new_judge_matrixs2.append(self.judge_matrix)          
        self.tentative_matrixs=new_tentative_matrixs2
        self.judge_matrixs=new_judge_matrixs2
        #候補上限
        candidate_number = 100
        if len(self.tentative_matrixs)>candidate_number:
            num=len(self.tentative_matrixs)//candidate_number
            for i in range(num+2):
                r=random.randint(0,1)
                del self.tentative_matrixs[r::2]
                del self.judge_matrixs[r::2]

            print(f"{candidate_number}以上の候補が見つかったため、候補を絞りました。")



    #入る可能性のある値を仮置きする
    def insert_possible_number(self):
        new_tentative_matrixs=[]
        for judge_matrix,tentative_matrix in zip(self.judge_matrixs,self.tentative_matrixs):
            judge_list=[]
            for i in range(9):
                judge_list+=[len(column) for column in judge_matrix[i] ]
            c=judge_list.index(min(judge_list))//9
            r=judge_list.index(min(judge_list))%9
            tentative_list=judge_matrix[c,r]
            #print(f"{c+1}行、{r+1}列を、{tentative_list}のいずれかに置換")
            for i in range(len(tentative_list)):
                new_tentative_matrix=np.copy(tentative_matrix)
                new_tentative_matrix[c,r]=tentative_list[i]
                new_tentative_matrixs.append(new_tentative_matrix)  
        print("==========================================================")
        self.tentative_matrixs=new_tentative_matrixs

    #入力された値が正しいかどうか判断。
    def check_input(self):
        for i in range(9):
            column = self.base_matrix[i,:]
            original = column[column!=0]
            processed ,count_list=np.unique(column[column!=0],return_counts=True)
            if not np.array_equal(np.sort(original),np.sort(processed)):
                self.text=f"{i+1}行目で{processed[count_list>1][0]}が重複しています。"
                return True
            
        for i in range(9):
            row = self.base_matrix[:,i]
            original = row[row!=0]
            processed ,count_list=np.unique(row[row!=0],return_counts=True)
            if not np.array_equal(np.sort(original),np.sort(processed)):
                self.text=f"{i+1}列目で{processed[count_list>1][0]}が重複しています。"
                return True
            
        for i in range(3):
            for j in range(3):
                box = self.base_matrix[i*3:(i+1)*3,j*3:(j+1)*3].reshape(-1)
                original = box[box!=0]
                processed ,count_list=np.unique(box[box!=0],return_counts=True)
                if not np.array_equal(np.sort(original),np.sort(processed)):
                    self.text=f"左から{j+1}番目、上から{i+1}番目の\nBOXで{processed[count_list>1][0]}が重複しています。"
                    return True
                
        return False 
    
    def check_no_answer(self):
        if self.tentative_matrixs==[]:
            self.text="解なし"
            self.free_label_apdate(self.text,"red")
            self.no_answer_flag=True

    
    #計算開始ボタンの関数
    def calculate(self):
        self.no_answer_flag = False 
        self.clear = False
        if self.check_input():
            self.free_label_apdate(self.text,"red")
            return
        else:
            self.text="計算中"
            self.free_label_apdate(self.text,"black")

        self.tentative_matrixs=[]
        self.judge_matrixs=[]
        self.calculate_flag=False
        self.answer_matrix=np.copy(self.base_matrix)
        self.tentative_matrixs.append(self.answer_matrix)
        if np.array_equal(self.answer_matrix, np.array([ [0 for i in range(9)] for j in range(9)])):
            self.judge_matrix=np.array([[[i+1 for i in range(9)] for i in range(9)] for j in range(9)])
            self.judge_matrixs.append(self.judge_matrix)
        else:
            self.fill_number()
            self.check_no_answer()
        if self.no_answer_flag:
            print(self.tentative_matrixs)
            print("可能な解が見つかりませんでした。最初期")
            return
        if self.clear==True:
            #正解画面を表示
            print("==========================================================")
            print(self.answer_matrix)
            print("self.answer_matrix仮置きなし")
            print("==========================================================")
            self.map_label_apdate(self.answer_matrix)
            self.text="計算完了"
            self.free_label_apdate(self.text,"black")
        else:
            print("==========================================================")
            #print("仮置き直前の行列")
            #print(self.tentative_matrixs)
            count=0
            count_limit=100
            while self.clear==False and count<count_limit:
                count+=1
                print(f"仮置き{count}回目")
                print("==========================================================")
                #self.map_label_apdate(self.answer_matrix)

                if self.tentative_matrixs==[]:
                    self.no_answer_flag=True
                self.insert_possible_number()
                self.fill_number()
                if self.no_answer_flag:
                    print("可能な解がありませんでした。")
                    return
                print("==========================================================")
                for i,mat in enumerate(self.tentative_matrixs):
                    print(f"第{i+1}候補")
                    print(mat)
                print("==========================================================")

            self.map_label_apdate(self.answer_matrix)
            #print(self.tentative_matrixs,"self.tentative_matrixs")

            if count==count_limit:
                self.text="計算上限。ごめんなさい(;_:)"
                print("正解となる行列が多数存在し計算できませんでした。")
                print("==========================================================")
                print("正解の可能性のある行列")
                for i,m in enumerate(self.tentative_matrixs):
                    print(f"第{i+1}候補")
                    print(m)
                    print("")
                print("==========================================================")
            else:
                self.text="計算完了"
                print("正解の行列")
                print(self.answer_matrix)
                print("==========================================================")
            self.free_label_apdate(self.text,"black")
########################################正解となりえない行列を見分ける関数を作ろう#########################


root=tk.Tk()
root.title("入力画面")
root.geometry("1200x700")
root.configure(bg="#FFFFFF")
app = Sudoku(master=root)
app.mainloop()