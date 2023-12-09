# Week 6 task - Advanced software development - Jarno Liedes - TVT21SPO
# Link to video demonstration: https://youtu.be/z3Aj5UXXfAE
# 100 meters long trenches are scaled half the size shorter -> looks better on the screen.
# Code should be fully runnable right away (No other scripts or files used)
# Tips: Choosing a value that is not between 0-99 will set the digging position randomly.

import numpy as np
import tkinter as tk
import threading
import winsound as ws
import time

window = tk.Tk()
window.title('Exercise 6')
window.geometry('800x800')
canvas = tk.Canvas(window, width=800, height=800)
canvas.place(x=0, y=0)

# Trench absolute y-positions
trench_ocean_side = 50
trench_pool_side = 550 # Trench is 500 long
trench_left_x = 250
trench_right_y = 550


class Smart_Digger:
    def __init__(self):
        self.current_index = -1
        self.current_list_number = 0
        self.index_list0 = [5,15,25,35,45,55,64,74,84,93]
        self.index_list1 = [10,20,30,40,50,60,70,80,90,99]
        self.current_list = self.index_list0
        self.uses = 0

    def get_smart_index(self):
        if self.current_list_number == 0 and self.current_index >= 9:
            self.current_index = -1
            self.current_list_number = 1
            self.current_list = self.index_list1
            self.uses += 1
        elif self.current_list_number == 1 and self.current_index >= 9:
            self.current_index = -1
            self.current_list_number = 0
            self.current_list = self.index_list0
            self.uses += 1

        index = self.current_index
        self.current_index += 1 # Every 10th
        return self.current_list[index]

    def reset(self):
        self.current_run = 0
        self.current_index = 0
        

class Colors:
    def __init__(self):
        self.water = '#1ca3ec'
        self.sand1 = '#FFEBCD'
        self.sand2 = '#D3AE74'
        self.sand3 = '#AC7B2F'
        self.sand4 = '#7C5210'


class Points :
    def __init__(self):
        self.frame = tk.Frame(window, bg='grey',height=30,width=760, border=True)
        self.frame.pack(expand=False, fill="none", side="top", anchor="center", padx=15, pady=15)
        self.array = []
        self._create_points()
    
    def _create_points(self):
        for i in range(5):
            new_label = tk.Label(self.frame, text=f"Points: {i+1}", bg="white", width=20)
            new_label.pack(side="left", anchor="center")
            self.array.append(new_label)

    def set_green(self, number):
        self.array[number-1].config(bg="green")


class Control:
    def __init__(self):
        self.points = 0
        self.points_obj = Points()
        self.fastest_digger = ""

    def i_suppose_i_have_earned_so_much_points(self, points):
        self.points = points
        self.points_obj.set_green(points)

    def check_if_going_to_next_level(self):
        def check_lvl_1():
            self.i_suppose_i_have_earned_so_much_points(1)

        def check_lvl_2():
            self.i_suppose_i_have_earned_so_much_points(2)
            info_text_var.set("Dig few times the trench on both sides")
            ws.Beep(600,1000)

        def check_lvl_3():
            if ernest.times_digged >= 5 and kernest.times_digged >= 5:
                self.i_suppose_i_have_earned_so_much_points(3)
                handler.reset_all_trenches()
                info_text_var.set("Trenches are now refilled with sand. \n Use 'automated monkey digging button'")
                ernest.btn_find_monkey.visibility(True)
                kernest.btn_find_monkey.visibility(True)
                ernest.btn_automated_monkey.visibility(True)
                kernest.btn_automated_monkey.visibility(True)
                ws.Beep(600,1000)

        def check_lvl_4():
            if ernest.smart_digger.uses >= 1 or kernest.smart_digger.uses >= 1:
                btn_reset_trench.visibility(False)
                self.i_suppose_i_have_earned_so_much_points(4)
                info_text_var.set("Now race who fills the pool first!")
                ws.Beep(600,1000)
            
        def check_lvl_5():
            if pool.is_finished :
                self.i_suppose_i_have_earned_so_much_points(5)
                info_text_var.set(f"CONGRATS, WINNER IS {self.fastest_digger}")
                if self.fastest_digger == "Ernest":
                    ws.Beep(400,10000)
                else:
                    ws.Beep(1000,10000)
            
        if self.points == 0 : check_lvl_1()
        elif self.points == 1 : check_lvl_2()
        elif self.points == 2: check_lvl_3()
        elif self.points == 3: check_lvl_4()
        elif self.points == 4: check_lvl_5()


class Custom_Button:
    def __init__(self, text, command, x, y, anchor, visible):
        self.button = tk.Button(window, text=text,command=command)
        self.x = x
        self.y = y
        self.anchor = anchor
        self.visibility(visible)

    def visibility(self, isVisible):
        if isVisible:
            self.button.place(anchor = self.anchor, x=self.x,y=self.y) # Sets button visible again on place
        else :
            self.button.place_forget() # Hides button


class Player:
    def __init__(self, name, player_pos, trench, color):
        self.name = name
        self.color = color
        self.start_pos = player_pos
        self.trench = trench
        self.text_var = tk.StringVar()
        self.text_var.set("")
        self.current_trench_index = 0
        self.x = player_pos[0]
        self.y = player_pos[1]
        self.speed = 0.002
        self.monkeys = []
        self.times_digged = 0
        self.is_moving = False
        self.smart_digger = Smart_Digger()
        
        if name == "Ernest":
            tk.Label(window, text=name, background="white", width=8, anchor="center").place( x=270,y=365)
            self.info = tk.Label(window, text="Number 0-99:", background="white", width=12, anchor="n").place( x=270,y=400)
            self.input = tk.Entry(window, textvariable=self.text_var, width=8)
            canvas.create_window(330, 433, window=self.input,anchor="center")
            self.btn_find_monkey = Custom_Button(text='Get monkey',command=handler.ernest_find_monkey, x=270, y=460, anchor='w', visible=True)
            self.btn_automated_monkey = Custom_Button(text='+10 (auto)',command=handler.ernest_automated_monkey, x=270, y=490, anchor='w', visible=False)
            self.digging_pos_x = trench_left_x - 20
            self.forest_position = [0,400]
        else : # Kernest
            tk.Label(window, text=name, background="white", width=8, anchor="center").place( x=460,y=365)
            self.info = tk.Label(window, text="Number 0-99:", background="white", width=12, anchor="center").place( x=460,y=400)
            self.input = tk.Entry(window, textvariable=self.text_var, width=8)
            canvas.create_window(520, 433, window=self.input, anchor="center")
            self.btn_find_monkey = Custom_Button(text='Get monkey',command=handler.kernest_find_monkey, x=460, y=460, anchor='w', visible=True)
            self.btn_automated_monkey = Custom_Button(text='+10 (auto)',command=handler.kernest_automated_monkey, x=460, y=490, anchor='w', visible=False)
            self.digging_pos_x = trench_right_y + 20
            self.forest_position = [780,400]
        self.draw()

    def draw(self):
        self.sprite = canvas.create_oval(self.x, self.y, self.x+15, self.y+15, fill=self.color)

    def button_find_a_new_monkey(self): # Find a monkey button
        if not self.is_moving :
            self.is_moving = True
            self.btn_find_monkey.visibility(False)
            self._actions_set_monkey_to_work(single=True)
            self.return_to_start_position()
            self.btn_find_monkey.visibility(True)
            self.is_moving = False

    def button_automated_monkeys(self): # Automated button
        if not self.is_moving :
            self.is_moving = True
            self.btn_automated_monkey.visibility(False)
            for i in range(10):
                if not self.is_moving : break
                self._actions_set_monkey_to_work(single=False)
                time.sleep(1)

            self.return_to_start_position()
            self.btn_automated_monkey.visibility(True)
            self.is_moving = False

    def _actions_set_monkey_to_work(self, single):
        monkey = self._spawn_a_monkey()
        self._find_a_monkey(monkey.x, monkey.y)
        self.monkeys.append(monkey)
        self._move_monkey_to_position(single)
        monkey.set_ready_for_shoveling(self.x, self.y, self.current_trench_index)
        handler.monkey_start_shoveling(monkey)
        self.return_to_start_position()

    def _spawn_a_monkey(self):
        if control.points < 3 :
            return Monkey(self, self.trench, self.forest_position[0], self.forest_position[1])
        # Money spawn at random position based on player's position
        random_x = 0
        random_y = np.random.randint(50, 500)
        if self.x < 400 : random_x = np.random.randint(5, 200) # left player
        else: random_x = np.random.randint(600, 780) # right player
        return Monkey(self, self.trench, random_x, random_y)

    def _find_a_monkey(self, monkey_x, monkey_y):
        step_y = 1
        step_x = 1
        if self.y > monkey_y : step_y = -1
        if self.x > monkey_x : step_x = -1

        while not self.y == monkey_y : # Vertical movement
            self.y += step_y
            canvas.moveto(self.sprite, self.x, self.y)
            time.sleep(self.speed)

        while not self.x == monkey_x : # Horizontal movement
            self.x += step_x
            canvas.moveto(self.sprite, self.x, self.y)
            time.sleep(self.speed)
        time.sleep(1)

    def _get_digging_position(self, single):
        if single :
            if self.text_var.get().isnumeric() :
                number = int(self.text_var.get())
                if  number >= 0 and number <= 99 :
                    self.current_trench_index = int(self.text_var.get())
                    return self.trench.get_position_by_index(self.current_trench_index)
            
            random_number = np.random.randint(0, 99)
            self.current_trench_index = random_number
            return self.trench.get_position_by_index(self.current_trench_index)
        
        else :
            self.current_trench_index = self.smart_digger.get_smart_index()
            return self.trench.get_position_by_index(self.current_trench_index)
    
    def _move_monkey_to_position(self, single):
        digging_pos_y = self._get_digging_position(single)
        step_x = 1
        step_y = 1
        if self.x > 400 : step_x = -1
        if self.y > digging_pos_y : step_y = -1

        while not self.y == digging_pos_y : # Move vertically
            self.y += step_y
            canvas.moveto(self.sprite, self.x, self.y)
            canvas.moveto(self.monkeys[-1].sprite, self.x, self.y)
            time.sleep(self.speed)

        self.x = round(self.x)
        
        while not self.x == self.digging_pos_x : # Move horizontally
            self.x += step_x
            canvas.moveto(self.sprite, self.x, self.y)
            canvas.moveto(self.monkeys[-1].sprite, self.x, self.y)
            time.sleep(self.speed)

        time.sleep(2)

    def return_to_start_position(self):
        step_x = 1
        step_y = 1
        if self.x > self.start_pos[0] : step_x = -1
        if self.y > self.start_pos[1] : step_y = -1

        while not self.x == self.start_pos[0]:
            self.x += step_x
            canvas.moveto(self.sprite, self.x, self.y)
            time.sleep(self.speed)
        
        while not self.y == self.start_pos[1]:
            self.y += step_y
            canvas.moveto(self.sprite, self.x, self.y)
            time.sleep(self.speed)

    def monkey_add_shoveling_count(self):
        self.times_digged += 1
        control.check_if_going_to_next_level()

    def destroy_all_monkeys(self):
        for m in self.monkeys:
            m.alive = False
            m.destroy()
            del(m)


class Monkey:
    def __init__(self, parent, trench, x, y):
        self.parent = parent
        self.trench = trench
        self.x = x
        self.y = y
        self.color = "brown"
        self.alive = True
        self.draw()

    def draw(self):
        self.sprite = canvas.create_oval(self.x, self.y, self.x+10, self.y+10, fill=self.color)

    def set_ready_for_shoveling(self, x, y, index):
        self.x = x
        self.y = y
        self.current_trench_index = index
        self.shovel_pos = self.y # index
    
    def start_shoveling_thread(self):
        speed = 1 # shoveling speed in m/s
        while self.current_trench_index >= 0 and self.alive and self.trench.check_if_no_water_by_index(self.current_trench_index):
            self._update_digging_position()
            ws.Beep(500,100)
            time.sleep(speed)
            if self.alive:
                self.trench.dig_at_position(self.current_trench_index)
                self.parent.monkey_add_shoveling_count()
                self.current_trench_index -= 1
                speed += speed
        canvas.delete(self.sprite)

    def _update_digging_position(self):
            self.y = self.trench.get_position_by_index(self.current_trench_index)
            canvas.moveto(self.sprite, self.x, self.y)

    def destroy(self):
        self.alive = False


class Trench:
    def __init__(self,owner, x, y):
        self.owner = owner
        self.x = x
        self.y = y
        self.pit_width = 10
        self.pit_height = 5 # Height is scaled smaller (looks better in screen)
        self.map = np.ones(100) # 1x100 array which will be scaled in draw() -function
        self.rectangles = []
        self.current_smart_index = 0
        self.rectangle_positions = []
        self.water_is_flowing = False
        self.draw()

    def draw(self):
        new_pos_y = self.y+self.pit_height
        for i in self.map:
            color = colors.sand1
            if i == 1: color = colors.sand1
            else : color = colors.sand2

            rectangle = canvas.create_rectangle(self.x, self.y, self.x + self.pit_width, new_pos_y, fill=color)
            self.rectangles.append(rectangle)
            self.rectangle_positions.append(self.y)
            self.y = new_pos_y
            new_pos_y += self.pit_height

    def reset_trench(self):
        index = 0
        for i in self.map:
            canvas.itemconfig(self.rectangles[index], fill=colors.sand1)
            self.map[index] = 1
            index+=1

    def get_position_by_index(self, index):
        return self.rectangle_positions[index]

    def get_value_by_index(self, index):
        return self.map[index]
    
    def check_if_no_water_by_index(self,index):
        return self.map[index] > -100
    
    def set_water_at_position(self, index):
        self.map[index] = -100 # Water index
        canvas.itemconfig(self.rectangles[index], fill=colors.water)
        if not self.water_is_flowing and self.map[-1] == -100:
            self.water_is_flowing = True
            
    def dig_at_position(self, index):
        if not self.map[index] <= -100: # no water
            self.map[index] -= 1
            color = self._get_sand_color_by_number(self.map[index])
            canvas.itemconfig(self.rectangles[index], fill=color)

    def _get_sand_color_by_number(self, numb):
        if numb == 1: return colors.sand1
        elif numb == 0: return colors.sand2
        elif numb == -1: return colors.sand3
        elif numb <= -100: return colors.water
        else : return colors.sand4


class Pool:
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.matrix = np.zeros((60, 20))
        self.water_is_flowing = False
        self.flow_speed = 0.01
        self.tiles = []
        self.is_finished = False
        self.draw()

    def draw(self):
        size = 10 # Tile size
        x1 = self.x
        x2 = self.x + size
        for x in range(60):
            y1 = self.y
            y2 = self.y + size
            for y in range(20):
                if self.matrix[x,y] == 0:
                    tile = canvas.create_rectangle(x1, y1, x2, y2, fill=colors.sand1)
                    self.tiles.append(tile)
                y1+=size
                y2=y1+size
            x1=x2
            x2+=size

    def ernest_trench_water_listener(self):
        while not ocean_ernest.water_is_flowing_to_pool :
            time.sleep(2)
        
        self._fill_pool_with_water()

    def kernest_trench_water_listener(self):
        while not ocean_kernest.water_is_flowing_to_pool :
            time.sleep(2)
        self._fill_pool_with_water()
        
    def _fill_pool_with_water(self):
        if not self.water_is_flowing:
            self.water_is_flowing = True
            self._draw_water()
        else:
            self.flow_speed -= self.flow_speed
        
    def _draw_water(self):
        for t in self.tiles :
            canvas.itemconfig(t, fill=colors.water)
            time.sleep(self.flow_speed)
        self.matrix = np.ones((60, 20))
        self.is_finished = True
        control.check_if_going_to_next_level()
    

class Ocean:
    def __init__(self, trench):
        self.trench = trench
        self.my_index = 0
        self.index_cache = []
        self.active = False
        self.water_is_flowing_to_pool = False

    def set_active(self, active):
        self.active = active

    def set_trench_listener(self):
        self.active = True

        while self.active and self.my_index < 100 :
            if self.trench.get_value_by_index(self.my_index) < 1 :
                self.trench.set_water_at_position(self.my_index)
                self.index_cache.append(self.my_index)
                self.my_index += 1

            time.sleep(0.5)

        if self.my_index >= 100 :
            control.fastest_digger = self.trench.owner
            self.water_is_flowing_to_pool = True

    def reset(self):
        self.active = False
        self.my_index = 0

# Threading actions
class Handler:
    def ernest_find_monkey(self):
        t = threading.Thread(target=ernest.button_find_a_new_monkey)
        t.start()

    def kernest_find_monkey(self):
        t = threading.Thread(target=kernest.button_find_a_new_monkey)
        t.start()

    def ernest_automated_monkey(self):
        t = threading.Thread(target=ernest.button_automated_monkeys)
        t.start()

    def kernest_automated_monkey(self):
        t = threading.Thread(target=kernest.button_automated_monkeys)
        t.start()

    def monkey_start_shoveling(self, monkey):
        t = threading.Thread(target=monkey.start_shoveling_thread)
        t.start()

    def set_ocean_listeners(self):
        t0 = threading.Thread(target=ocean_ernest.set_trench_listener)
        t0.start()

        t1 = threading.Thread(target=ocean_kernest.set_trench_listener)
        t1.start()

    def set_pool_listeners(self):
        t0 = threading.Thread(target=pool.ernest_trench_water_listener)
        t0.start()
        t1 = threading.Thread(target=pool.kernest_trench_water_listener)
        t1.start()

    def reset_all_trenches(self):
        ernest.is_moving = False
        kernest.is_moving = False
        ocean_ernest.reset()
        ocean_kernest.reset()
        ernest.smart_digger.reset()
        kernest.smart_digger.reset()
        ernest.destroy_all_monkeys()
        kernest.destroy_all_monkeys()
        ernest.trench.reset_trench()
        kernest.trench.reset_trench()
        handler.set_ocean_listeners()

# Color palette
colors = Colors()

# Canvas background
canvas.create_rectangle(0, 0, 800, 800, fill=colors.water) # Ocean
canvas.create_rectangle(0, trench_ocean_side, 800, 800, fill=colors.sand1) # Island

# Classes
control = Control()
handler = Handler()
pool = Pool(100, trench_pool_side)
ernest_trench = Trench(owner="Ernest", x=trench_left_x,y=trench_ocean_side)
kernest_trench = Trench(owner="Kernest", x=trench_right_y,y=trench_ocean_side)
ernest = Player("Ernest",[200,300],ernest_trench, "green")
kernest = Player("Kernest",[600,300],kernest_trench, "red")
ocean_ernest = Ocean(ernest_trench)
ocean_kernest = Ocean(kernest_trench)
info_text_var = tk.StringVar()
info_text_var.set("Set your first monkey for digging")
text_info = tk.Label(window, textvariable=info_text_var, height=5, width=40, anchor="center", bg=colors.sand1)
text_info.place(x=405,y=120, anchor="center")
btn_reset_trench = Custom_Button(text="Reset all", command=handler.reset_all_trenches, x=400, y=770, anchor='center', visible=True)
control.check_if_going_to_next_level()
handler.set_ocean_listeners()
handler.set_pool_listeners()

window.mainloop()