# Week 8 task - Advanced Software Development Techniques - Jarno Liedes - TVT21SPO
# Link to video demonstration: https://youtu.be/9xb-v7t1iiI
# Code is ready to be tested right away (No other scripts or files used)

import numpy as np
import tkinter as tk
import threading
import winsound as ws
import time

class Colors:
    def __init__(self):
        self.water = '#1ca3ec'
        self.sand1 = '#FFEBCD'
        self.sand2 = '#D3AE74'
        self.sand3 = '#AC7B2F'
        self.sand4 = '#7C5210'
        self.stats = 'blue'
        self.monkey = '#A8795A'

win_width = 800
win_height = 800
window = tk.Tk()
window.title('Exercise 8')
window.geometry(f'{win_width}x{win_height}')
colors = Colors()
canvas = tk.Canvas(window, width=800, height=800, bg=colors.water)
canvas.place(x=0, y=0)
threads_stop_flag = False

class Handler:
    def start_control_points_listener(self, controller):
        t = threading.Thread(target=controller.thread_points_listener)
        t.start()
        
    def monkey_spawn_update_thread(self, monkey):
        t = threading.Thread(target=monkey.thread_monkey_update)
        t.start()

    def island_monkey_listener(self, island):
        t = threading.Thread(target=island.island_monkey_listener)
        t.start()

    def island_stats_listener(self, island):
        t = threading.Thread(target=island.island_stats_listener)
        t.start()

handler = Handler()
semaphore_single = threading.Semaphore(1)

class Points :
    def __init__(self):
        self.frame = tk.Frame(window, bg='grey',height=30,width=760, border=True)
        self.frame.pack(expand=False, fill="none", side="top", anchor="center", padx=15, pady=15)
        self.array = []
        self._draw_points_bar()
        self.set_green(0)
    
    def _draw_points_bar(self):
        list = [0, 5, 10, 15 ,20]
        for i in list:
            new_label = tk.Label(self.frame, text=f"Points: {i}", bg="white", width=20)
            new_label.pack(side="left", anchor="center")
            self.array.append(new_label)

    def set_green(self, index):
        self.array[index].config(bg="green")

    def set_color(self, index, color):
        self.array[index].config(bg=color)

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


class Control:
    def __init__(self):
        self.points = 0
        self.island_counter = 1 # First island is created automatically in Map class
        self.reset_press_counter = 0
        self.points_obj = Points()
        self.listener_active_flag = True
        self.monkey_can_die_of_laughter = False
        self.monkey_travel_teaching_enabled = False
        self.button_lock = False
        self.monkeys_death_by_laugh = 0
        self.monkeys_death_by_shark = 0
        handler.start_control_points_listener(self)

    def thread_points_listener(self):
        while self.listener_active_flag:
            self.check_if_going_to_next_level()
            time.sleep(0.5)

    def i_suppose_i_have_earned_so_much_points(self, points):
        def get_index_of_points(points):
            list = [0, 5, 10, 15, 20]
            return list.index(points)
        index = get_index_of_points(points)
        self.points = points
        self.points_obj.set_green(index)

    def check_if_going_to_next_level(self):

        def check_points_1(): # First hidden step -> press reset button
            if self.reset_press_counter > 0:
                info_text_var.set("Create 10 islands randomly")
                self.points = 1

        def check_points_5() : # Spawn 10 islands and hit the reset
            if map.island_count > 9:
                info_text_var.set("Good! Islands will be reset automatically")
                self.button_lock = True
                time.sleep(5)
                self.i_suppose_i_have_earned_so_much_points(5)
                self.button_lock = False
                self.btn_reset_all()
                self.monkey_can_die_of_laughter = True
                info_text_var.set("Let a monkey die of laughter or be eaten by shark")
                info_text_var2.set("")

        def check_points_10() :
            if self.monkeys_death_by_laugh > 0 or self.monkeys_death_by_shark > 0:
                if self.monkeys_death_by_shark > 0: 
                    info_text_var.set(f"Nice! Monkey was eaten by a shark...")
                else:
                    info_text_var.set(f"Nice! Monkey died of laughter...")
                info_text_var2.set("")
                self.button_lock = True
                time.sleep(5)
                self.button_lock = False
                self.monkey_travel_teaching_enabled = True
                self.btn_reset_all()
                map.set_island_stats_visible()
                info_text_var.set("Now teach other island habitants how to travel")
                self.i_suppose_i_have_earned_so_much_points(10)
                

        def check_points_15() :
            if map.traveling_islands_count >= 2:
                info_text_var.set("Teach at least 2 more islands about the traveling")
                info_text_var2.set("")
                self.i_suppose_i_have_earned_so_much_points(15)

        def check_points_20() :
            if map.traveling_islands_count >= 4: # Added limit (4) so demonstration video wouldn't be too long
                info_text_var.set("Wow, I did it!\n(You can continue until all the islands know about traveling)")
                info_text_var2.set("")
                self.i_suppose_i_have_earned_so_much_points(20)

        def secret_ending() : # When all the possible islands know about the traveling
            if map.traveling_islands_count >= 10:
                info_text_var.set("Congrats, you finished the game!")
                info_text_var2.set("")
                for i in range(5):
                    self.points_obj.set_color(i, "violet")

        if self.points == 0 : check_points_1()
        elif self.points == 1 : check_points_5()
        elif self.points == 5 : check_points_10()
        elif self.points == 10: check_points_15()
        elif self.points == 15: check_points_20()
        elif self.points == 20: secret_ending()

    def btn_create_island(self):
        if not self.button_lock :
            self.island_counter += 1
            map.create_new_island()
        else: info_text_var2.set("Can't create island - button is locked")

    def btn_reset_all(self):
        if not self.button_lock :
            self.monkeys_death_by_laugh = 0
            self.monkeys_death_by_shark = 0
            self.reset_press_counter += 1
            self.island_counter = 0
            map.reset_all()
        else: info_text_var2.set("Can't reset - button is locked")

class Map:
    def __init__(self):
        self.islands = []
        self.island_count = 0
        self.traveling_islands_count = 0
        self.swimming_monkeys = []
        self.spawn_area_indexes = []
        self.area_cordinates = []
        self._set_cordinates()
        self.create_new_island()
    
    def _set_cordinates(self):
        def draw_canvas_borders(_x1,_y1,_x2,_y2):
            canvas.create_rectangle(_x1, _y1, _x2, _y2) # Set off
            tk.Label(window, text=f'{index}', height=1, width=1, anchor="center",bg=colors.water).place(x=_x1+2,y=_y1+2) # Set off

        add = 200
        x1 = 0
        x2 = x1 + add
        y1 = 100
        y2 = y1 + add
        new_y1 = y1
        new_y2 = y1
        index = 0

        for x in range(4):
            island_area_cordinates = Map_Area_Cordinates(index,x1,y1,x2,y2)
            self.area_cordinates.append(island_area_cordinates)
            draw_canvas_borders(x1,y1,x2,y2)
            index += 1
            new_y1 = y1 + add
            new_y2 = y2 + add
            for y in range(2):
                island_area_cordinates = Map_Area_Cordinates(index,x1,new_y1,x2,new_y2)
                self.area_cordinates.append(island_area_cordinates)
                draw_canvas_borders(x1, new_y1, x2, new_y2)
                index += 1
                new_y1 += add
                new_y2 += add

            x1 += add
            x2 += add

    def check_if_spawn_area_is_available(self, index):
        for i in self.spawn_area_indexes:
            if i == index:
                return False
        self.spawn_area_indexes.append(index)
        return True

    def get_spawn_area_by_index(self, index):
        return self.area_cordinates[index]

    def create_new_island(self):
        global threads_stop_flag
        max_islands = 10
        if len(self.spawn_area_indexes) >= max_islands: 
            return
        if threads_stop_flag : threads_stop_flag = False
        
        def make_a_new_position():
            rand_index = np.random.randint(0,12)
            while not self.check_if_spawn_area_is_available(rand_index) :
                rand_index = np.random.randint(0,12)
            area = self.get_spawn_area_by_index(rand_index)
            rand_x = np.random.randint(area.x1, area.x2)
            rand_y = np.random.randint(area.y1, area.y2)
            return [rand_x, rand_y]

        new_pos = make_a_new_position()
        width = np.random.randint(70,130)
        height = np.random.randint(70,130)
        self.island_count += 1
        map_index = 0
        new_island = Island(number=self.island_count, map_index=map_index, name=f'S{self.island_count}', center_pos=new_pos, width=width, height=height)
        self.islands.append(new_island)

    def check_if_out_of_bounds(self, x, y):
        if x <= 0 or x >= win_width or y <= 100 or y >= win_height-100 :
            return True
        return False

    def check_if_on_any_island(self, x, y):
        for i in self.islands:
            if i.x1 <= x and i.x2 >= x and i.y1 <= y and i.y2 >= y:
                return True
        return False
    
    def get_island_by_position(self, x, y):
        for i in self.islands:
            if i.x1 <= x and i.x2 >= x and i.y1 <= y and i.y2 >= y:
                return i
        return self.islands[0]
    
    def set_island_stats_visible(self):
        for i in self.islands:
            i.show_stats = True
            i.draw_island_text_stats()

    def add_swimming_monkey(self, monkey):
        self.swimming_monkeys.append(monkey)

    def remove_swimming_monkey(self, monkey):
        for i in self.swimming_monkeys:
         if i == monkey:
             self.swimming_monkeys.remove(i)
             break

    def reset_all(self):
        global threads_stop_flag
        threads_stop_flag = True
        self.island_count = 0
        self.traveling_islands_count = 0
        self.spawn_area_indexes = []
        for i in self.islands:
            i.delete_island()
        self.islands.clear()
        for i in self.swimming_monkeys :
            i.delete()
        self.swimming_monkeys.clear()


class Map_Area_Cordinates:
    def __init__(self, my_index, x1, y1, x2, y2):
        self.cordinates = [x1,y1,x2,y2]
        padding = 70
        self.index = my_index
        self.x1 = x1+padding
        self.y1 = y1+padding
        self.x2 = x2-padding
        self.y2 = y2-padding


class Dock:
    def __init__(self, name, x, y, visible):
        self.name = name
        self.x = x
        self.y = y
        self.visible = visible
        self.sprite = 0
        if visible : self.draw()

    def draw(self):
        size = 5
        self.sprite = canvas.create_rectangle(self.x-size, self.y-size, self.x+size, self.y+size, fill="blue")

    def get_position(self):
        return [self.x, self.y]

    def delete(self):
        self.delete()


class Island:
    def __init__(self, number, map_index, name, center_pos, width, height):
        self.number = number
        self.map_index = map_index
        self.name = name
        self.position = center_pos
        self.width = width
        self.height = height
        self.color = colors.sand2
        self.spawn = []
        self.docks = []
        self.monkeys = []
        self.monkey_count = 0
        self.can_send_swimmers = False
        if control.points >= 5 and self.number == 1:
            self.can_send_swimmers = True
            map.traveling_islands_count += 1
        self.show_stats = control.points >= 10
        self._set_cordinates()
        self._set_spawn()
        self._draw_island()
        self._create_docks()
        self.create_monkeys()
        self.set_island_monkey_listener()
        self.set_island_stats_listener()
        canvas.tag_lower("island")
        canvas.tag_raise("stats")

    def _set_cordinates(self):
        self.x1 = self.position[0] - (self.width/2)
        self.y1 = self.position[1] - (self.height/2)
        self.x2 = self.position[0] + (self.width/2)
        self.y2 = self.position[1] + (self.height/2)

    def _set_spawn(self):
        coastline = 50
        x1 = self.position[0] - coastline
        y1 = self.position[1] - coastline
        x2 = self.position[0] + coastline
        y2 = self.position[1] + coastline
        self.spawn = [x1,y1,x2,y2]

    def _draw_island(self):
        self.sprite = canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2, fill=self.color, tags="island")
        self.text_name = canvas.create_text(self.position[0], self.position[1]-7, fill=colors.stats, text="", font=("Helvetica", 10, "bold"), tags="stats")
        self.text_stats = canvas.create_text(self.position[0], self.position[1]+7, fill=colors.stats, text="", font=("Helvetica", 10, "bold"), tags="stats")
        self.draw_island_text_stats()

    def draw_island_text_stats(self):
        if self.show_stats:
            self.monkey_count = len(self.monkeys)
            canvas.itemconfig(self.text_stats, text=f'Count: {self.monkey_count}')
            canvas.itemconfig(self.text_name, text=self.name)

    def _create_docks(self):
        self.docks.append(Dock("North", self.position[0], self.position[1]-self.height/2, self.can_send_swimmers))
        self.docks.append(Dock("East", self.position[0]+self.width/2, self.position[1], self.can_send_swimmers))
        self.docks.append(Dock("West", self.position[0]-self.width/2, self.position[1], self.can_send_swimmers))
        self.docks.append(Dock("East", self.position[0], self.position[1]+self.height/2, self.can_send_swimmers))

    def set_docks_visible(self):
        if not self.can_send_swimmers:
            for i in self.docks:
                i.draw()
            self.can_send_swimmers = True
            map.traveling_islands_count += 1

    def get_dock_cordinates(self, direction_index): # 0 = North, 1 = East, 2 = South, 3 = West
        return self.docks[direction_index]

    def create_monkeys(self):
        self.monkey_count = 10
        for i in range(self.monkey_count):
            rand_x = np.random.randint(self.x1+5, self.x2-5)
            rand_y = np.random.randint(self.y1+5, self.y2-5)
            monkey = Monkey(id=i,home_island=self,x=rand_x,y=rand_y)
            self.add_new_monkey(monkey)
            handler.monkey_spawn_update_thread(monkey=monkey)

    def set_island_monkey_listener(self): # THREAD
        handler.island_monkey_listener(self)

    def island_monkey_listener(self): # THREAD
        global threads_stop_flag
        while not threads_stop_flag :
            if self.can_send_swimmers and len(self.monkeys) > 0:
                self.send_monkey_to_swimming()
            time.sleep(10)

    def set_island_stats_listener(self): # THREAD
        handler.island_stats_listener(self)

    def island_stats_listener(self):
        global threads_stop_flag
        while not threads_stop_flag :
            if self.show_stats:
                self.monkey_count = len(self.monkeys)
                canvas.itemconfig(self.text_name, text=self.name)
                canvas.itemconfig(self.text_stats, text=f'Count: {self.monkey_count}')
            time.sleep(1)

    def check_if_is_on_my_spawn(self, x,y):
        if x > self.spawn[0] and x < self.spawn[2] and y > self.spawn[1] and y < self.spawn[3] :
            return True
        return False
    
    def add_new_monkey(self, monkey):
        self.monkeys.append(monkey)

    def add_monkey_from_another_island(self, monkey):
        if control.monkey_travel_teaching_enabled :
            self.set_docks_visible()
            self.can_send_swimmers = True
        self.monkeys.append(monkey)
        rand_x = np.random.randint(self.x1+5, self.x2-5)
        rand_y = np.random.randint(self.y1+5, self.y2-5)
        monkey.x = rand_x
        monkey.y = rand_y
        canvas.moveto(monkey.sprite, x=monkey.x, y=monkey.y)
        
    def remove_monkey_from_island(self, monkey):
        if monkey in self.monkeys:
            self.monkeys.remove(monkey)

    def send_monkey_to_swimming(self):
        direction = np.random.randint(0,4)
        dock_position = self.docks[direction].get_position()
        index = np.random.randint(0, len(self.monkeys))
        monkey = self.monkeys[index] # Choose a random monkey from island
        canvas.itemconfig(monkey.sprite, fill="brown")
        map.add_swimming_monkey(monkey)
        self.remove_monkey_from_island(monkey)
        monkey.set_monkey_to_dock_ready_for_swimming(x=dock_position[0], y=dock_position[1], direction=direction)
        info_text_var2.set(f"Sending monkey {monkey.id} to swimming from {self.name}")

    def destroy_all_monkeys(self):
        for i in self.monkeys :
            i.delete()
        self.monkeys.clear()

    def destroy_all_docks(self):
        for i in self.docks:
            canvas.delete(i.sprite)
        self.docks.clear()

    def delete_island(self):
        self.destroy_all_monkeys()
        self.destroy_all_docks()
        canvas.delete(self.sprite)
        canvas.delete(self.text_name)
        canvas.delete(self.text_stats)


class Monkey:
    def __init__(self, home_island, id, x, y):
        self.parent_island = home_island
        self.home_island = home_island
        self.id = id
        self.x = x
        self.y = y
        self.next_move = [0, 0]
        self.color = colors.monkey
        self.is_swimming = False
        self.alive_flag = True
        self.direction = -1 # Not facing in any direction
        self.wait_time = 10
        self.frequency = np.random.randint(200,1000) # Monkey voice/sound
        self.draw()

    def draw(self):
        self.sprite = canvas.create_oval(self.x, self.y, self.x+10, self.y+10, fill=self.color, tags="monkey")

    def set_monkey_to_dock_ready_for_swimming(self,x,y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        step = 5

        if self.direction == 0: # North
            self.next_move = [0, -step]
        elif self.direction == 1: # East
            self.next_move = [step, 0]
        elif self.direction == 2: # South
            self.next_move = [-step, 0]
        else: # West
            self.next_move = [0, step]

        self.is_swimming = True
        if self.is_swimming : self.wait_time = 1
        else: self.wait_time = 10

    def thread_monkey_update(self):
        global threads_stop_flag
        while not threads_stop_flag and self.alive_flag:
            semaphore_single.acquire()
            if not self.is_swimming :
                self.monkey_idle_update()
            else:
                self.monkey_swimming_update()
            semaphore_single.release()
            time.sleep(self.wait_time)

    def monkey_idle_update(self):
            if self._check_one_percent_possibility() and control.monkey_can_die_of_laughter: # Checks if monkey dies at laughter
                canvas.itemconfig(self.sprite, fill="red")
                info_text_var2.set(f"Monkey {self.id} died of laughter in the island {self.parent_island.name}")
                control.monkeys_death_by_laugh += 1
                self.parent_island.remove_monkey_from_island(self)
                ws.Beep(self.frequency,1000)
                self.delete()
            else: # Idle screaming
                canvas.itemconfig(self.sprite, fill="white")
                ws.Beep(self.frequency,50)
            canvas.itemconfig(self.sprite, fill=self.color)

    def monkey_swimming_update(self): #direction: 0 = North, 1 = East, 2 = South, 3 = West
        self.x += self.next_move[0]
        self.y += self.next_move[1]
        canvas.moveto(self.sprite, self.x, self.y)
        canvas.itemconfig(self.sprite, fill="brown")
        ws.Beep(300,60)
        canvas.itemconfig(self.sprite, fill=self.color)
        if map.check_if_on_any_island(x=self.x, y=self.y): # Checks if monkey lands on a ISLAND
            self.parent_island = map.get_island_by_position(self.x, self.y)
            self.parent_island.add_monkey_from_another_island(self)
            self.x += self.next_move[0]*2
            self.y += self.next_move[1]*2
            self.is_swimming = False
            map.remove_swimming_monkey(self)
            self.wait_time = 10
        elif self._check_one_percent_possibility() or map.check_if_out_of_bounds(x=self.x, y=self.y): # Shark eats or out of bounds
                canvas.itemconfig(self.sprite, fill="red")
                info_text_var2.set(f"Monkey {self.id} was eaten by shark")
                control.monkeys_death_by_shark += 1
                map.remove_swimming_monkey(self)
                ws.Beep(self.frequency,1000)
                self.delete()

    def _check_one_percent_possibility(self):
        percent = np.random.randint(0, 100)
        return percent == 1

    def delete(self):
        self.alive_flag = False
        canvas.delete(self.sprite)

# Classes
control = Control()
map = Map()

# Labels
info_text_var = tk.StringVar()
info_text_var.set("Press reset button to clear all the islands")
info_text_var2 = tk.StringVar()
info_text_var2.set("")
text_info = tk.Label(window, textvariable=info_text_var, height=2, width=50, anchor="center", bg="white", font=("Arial", 12) )
text_info.place(x=405,y=65, anchor="center")
text_info2 = tk.Label(window, textvariable=info_text_var2, height=1, width=40, anchor="center", bg=colors.water, font=("Arial", 10) )
text_info2.place(x=405,y=750, anchor="center")

# Buttons
tk.Button(window, text='New Island',command=control.btn_create_island).place(x=60,y=760, anchor="center")
tk.Button(window, text='Reset All',command=control.btn_reset_all).place(x=740,y=760, anchor="center")

window.update()
window.mainloop()