# Week 5 task - Advanced software development - Jarno Liedes - TVT21SPO
# Link to video demonstration: https://youtu.be/QBGtTJFD3is
# Code should be fully runnable right away (No other scripts or files used)

import tkinter as tk
import threading
import time
import numpy as np
import winsound as ws

window = tk.Tk()
window.title('Exercise 5')
window.geometry('800x800')
canvas = tk.Canvas(window, width=800, height=800)

# Monkey's swimming positions
swim_start_pos = 150
swim_end_pos = 650

ernest_text_variable = tk.StringVar()
ernest_text_variable.set("Distance: 0km'")
kernest_text_variable = tk.StringVar()
kernest_text_variable.set("Distance: 0km'")
help_message = ["This", "is", "Ernest","and","Kernest,","we", "are", "trapped","in", "island!", "Help", "us!"] # 20 words -> duplicants not counted!

class Control:
    def __init__(self):
        self.points = 0
        self.ernest_monkeys = []
        self.kernest_monkeys = []
        self.monkey_cache = []
        self.monkey_messages = []

    # Adds a monkey to the list based on the monkey's player (parent)
    def add_monkey(self, monkey):
        owner = monkey.parent.name
        if owner == "Ernest" :
            self.ernest_monkeys.append(monkey)
        else : # Kernest
            self.kernest_monkeys.append(monkey)

        self._check_current_stage(monkey)

    def destroy_all_monkeys(self):
        for ernest_monkey in self.ernest_monkeys :
            ernest_monkey._delete()
        for kernest_monkey in self.kernest_monkeys :
            kernest_monkey._delete()
        canvas.update()    

    # Called always when a monkey successfully swims to the other side
    def _check_current_stage(self, monkey):
        message = monkey.message
        if self.points == 0:
            if self.ernest_monkeys and self.kernest_monkeys: self.i_suppose_i_have_earned_so_much_points(1, []) # Checks if arrays not empty

        elif self.points == 1:
            info3_text_var.set(f'Message: {self.monkey_messages}')
            if message not in self.monkey_messages: # Checks if no duplicants
                self.monkey_messages.append(message)
                if len(self.monkey_messages) == 12: self.i_suppose_i_have_earned_so_much_points(2, [])

        elif self.points == 2 and monkey.current_stage == 2:
            self.monkey_cache.append(monkey)
            count = 0
            for m in self.monkey_cache:
                 if m.parent.name == monkey.parent.name and m.group_id == monkey.group_id: count += 1
                 
            if count >= 5 : self.i_suppose_i_have_earned_so_much_points(3, [])
            else : info3_text_var.set(f"Only {count} monkeys survived in a group")

        elif self.points == 3 and monkey.current_stage == 3 :
            # POHTERI
            if monkey.parent.name == "Ernest" and message not in pohteri.collected_monkey_messages:
                pohteri.add_message(message)
                info3_text_var.set(f"Pohteri: {pohteri.collected_monkey_messages}")
            # ETETERI
            elif monkey.parent.name == "Kernest" and message not in eteteri.collected_monkey_messages:
                eteteri.add_message(message)
                info4_text_var.set(f"Eteteri: {eteteri.collected_monkey_messages}")


    # Determines the stages of gameplay
    def i_suppose_i_have_earned_so_much_points(self, new_points, attributes):
        self.destroy_all_monkeys() # Clear the data of all the monkeys
        def go_level_1():
            info_text_var.set("Send monkeys to the continent with a help message")
            text_points_1.config(bg="green")
            self.points = new_points
            self.monkey_messages.clear() # Clear all the send messages
            self.monkey_cache.clear()

        def go_level_2():
            info_text_var.set("")
            text_points_2.config(bg="green")
            info_text_var.set("Send 10 monkeys to the continent and make sure that atleast half of the grew succeeds\nWATCHOUT SHARKS!")
            info3_text_var.set("")
            btn_kernest_send_monkey.visibility(False)
            btn_ernest_send_monkey.visibility(False)
            btn_kernest_send_10_monkeys.visibility(True)
            btn_ernest_send_10_monkeys.visibility(True)
            self.points = new_points
            self.monkey_messages.clear() # Clear all the send messages
            self.monkey_cache.clear()

        def go_level_3():
            info_text_var.set("Fight for which one succeeds sending more monkeys until help message is send!")
            info2_text_var.set("CONGRATS, HALF OF THE MONKEYS IN A GROUP SURVIVED!")
            info3_text_var.set("Pohteri: []")
            info4_text_var.set("Eteteri: []")
            text_points_3.config(bg="green")
            btn_kernest_send_monkey.visibility(True)
            btn_ernest_send_monkey.visibility(True)
            pohteri.draw()
            handler.pohteri_read_monkey_messages()
            eteteri.draw()
            handler.eteteri_read_monkey_messages()
            self.points = new_points
            self.monkey_messages.clear() # Clear all the send messages
            self.monkey_cache.clear()

        def go_level_4():
            if attributes[0] == ernest.y: info2_text_var.set("ERNEST IS THE WINNER!")
            else: info2_text_var.set("KERNEST IS THE WINNER!")

            btn_kernest_send_monkey.visibility(False)
            btn_ernest_send_monkey.visibility(False)
            btn_kernest_send_10_monkeys.visibility(False)
            btn_ernest_send_10_monkeys.visibility(False)
            info3_text_var.set("")
            info4_text_var.set("")
            self.points = new_points

        def go_level_4_1(): # Mid level action
            info_text_var.set("Ship has been send!")
            info2_text_var.set("")
            text_points_4.config(bg="green")
            time.sleep(3)

        def calculate_winner():
            ernest_monkeys = len(pohteri.collected_monkey_messages)
            kernest_monkeys = len(eteteri.collected_monkey_messages)
            text2 = "Kernest"
            if ernest_monkeys > kernest_monkeys : text2 = "Ernest"

            info2_text_var.set(f'Full message sent first by: {attributes[0]}\n'+
                               f'Most monkeys send: {text2} who got bigger party!')
            info3_text_var.set(f'Ernest send {ernest_monkeys} monkeys which feeds {ernest_monkeys*4} persons')
            info4_text_var.set(f'Kernest send {kernest_monkeys} monkeys which feeds {kernest_monkeys*4} persons')

        def go_level_4_2(): # Mid level action
            info_text_var.set("Ernest and Kernest has been rescued!")
            info2_text_var.set("")
            info3_text_var.set("")
            info4_text_var.set("")
            text_points_4.config(bg="green")
            time.sleep(3)
            calculate_winner()
            go_level_5()

        def go_level_5(): # Game over
            info_text_var.set("CONGRATS, YOU FINISHED GAME!")
            text_points_5.config(bg="green")
            self.points = new_points

        if new_points == 1 : go_level_1()
        elif new_points == 2 : go_level_2()
        elif new_points == 3 : go_level_3()
        elif new_points == 4 : go_level_4()
        elif new_points == 41 : go_level_4_1() # Ship is send
        elif new_points == 42 : go_level_4_2() # Ship returns
        elif new_points == 5 : go_level_5()

        print(f'You got {self.points} points')
        ws.Beep(600,1000)


class Player:
    def __init__(self, name, x, y, text_variable):
        self.name = name
        self.x = x
        self.y = y
        self.monkey_count = 0
        self.monkey_group_count = 0
        self.text_var = text_variable

    def draw_speed(self, km):
        self.text_var.set(f'Distance: {km}km')

    def add_new_monkey_group(self):
        self.monkey_group_count += 1

    def send_a_new_monkey(self):
        self.monkey_count += 1
        self._spawn_monkey(-1) # -1 = Not in group so no group id!

    def send_10_new_monkeys(self):
        # Monkey count is handled in handler
        self._spawn_monkey(self.monkey_group_count) # Count = new group id

    def _spawn_monkey(self, group_id): # Group determines what group monkey belongs (-1 = no group)
        self.draw_speed(0)
        monkey = Monkey(self, self.monkey_count, self.y, group_id)
        monkey.group_id = group_id
        monkey._draw()
        monkey._update()

class Monkey:
    def __init__(self, parent, id, y, group_id):
        self.parent = parent
        self.id = id
        self.group_id = group_id
        self.current_stage = control.points
        self.x = swim_start_pos
        self.y = y
        self.km = 0
        self.message = help_message[np.random.randint(0, len(help_message))]

    def _draw(self):
        self.draw = canvas.create_oval(self.x, self.y, self.x+10, self.y+10, fill="brown")

    def _update(self):
        while self.x < swim_end_pos and self.current_stage == control.points:
            speed = 0.02 # Swimming speed in km/s (0.05 = normal)
            time.sleep(speed)
            canvas.moveto(self.draw, self.x, self.y)
            self.x += 5
            self.km += 1
            self.parent.draw_speed(self.km)

            if self.current_stage >= 2 and self._check_if_shark_bite(): # Shark attacks
                info2_text_var.set(f"{self.parent.name}'s monkey in group {self.id} was eaten by shark!")
                ws.Beep(1000,50) # Death sound
                self._delete()
                return
            else:
                ws.Beep(500,100) # >Normal swimming sound

            window.update()

        control.add_monkey(self)
        self._delete()

    def _check_if_shark_bite(self):
            percent = np.random.randint(0,100)
            if percent == 1: # Shark bites a monkey
                 return True
            return False

    def _delete(self):
        canvas.delete(self.draw)


# Handler for threading actions
class Handler:
    def ernest_send_monkey(self):
        t = threading.Thread(target=ernest.send_a_new_monkey)
        t.start()
    
    def ernest_send_10_monkeys(self):
        ernest.monkey_group_count += 1
        for i in range(10):
            time.sleep(0.1)
            t = threading.Thread(target=ernest.send_10_new_monkeys)
            t.start()
            window.update()

    def kernest_send_monkey(self):
        kernest.monkey_group_count += 1
        t = threading.Thread(target=kernest.send_a_new_monkey)
        t.start()

    def kernest_send_10_monkeys(self):
         for i in range(10):
            time.sleep(0.1)
            t = threading.Thread(target=kernest.send_10_new_monkeys)
            t.start()
            window.update()

    def pohteri_read_monkey_messages(self):
            t = threading.Thread(target=pohteri.read_monkey_messages_loop)
            t.start()

    def eteteri_read_monkey_messages(self):
            t = threading.Thread(target=eteteri.read_monkey_messages_loop)
            t.start()

# Button for sending monkeys to swimming
class Monkey_Button:
    def __init__(self, text, command, x, y, visible):
          self.button = tk.Button(window, text=text,command=command)
          self.x = x
          self.y = y
          self.visibility(visible)

    def visibility(self, isVisible):
        if isVisible:
            self.button.place(anchor = "w", x=self.x,y=self.y) # Sets button visible again on place     
        else :
            self.button.place_forget() # Hides button


class Port_Watcher:
    def __init__(self,x,y, color, player):
         self.x = x
         self.y = y
         self.color = color
         self.ship_is_sent = False
         self.player = player

    def draw(self):
        self.watcher = canvas.create_oval(self.x, self.y, self.x+15, self.y+15, fill=self.color)
        self.collected_monkey_messages = []

    def add_message(self, message):
        self.collected_monkey_messages.append(message)

    def read_monkey_messages_loop(self):
        while len(self.collected_monkey_messages) < 11 :
            time.sleep(0.2)

        self.send_ship()

    def send_ship(self):
        if not pohteri.ship_is_sent and not eteteri.ship_is_sent :
            pohteri.ship_is_sent = True
            eteteri.ship_is_sent = True
            control.i_suppose_i_have_earned_so_much_points(4, [self.y])
            self.ship = Ship(650,self.y, self.player)
            self.ship.draw_ship()
            self.ship.move_to_island()


class Ship:
    def __init__(self,x, y, player):
        self.x = x
        self.y = y
        self.player = player

    def draw_ship(self):
        self.draw = canvas.create_oval(self.x, self.y, self.x+30, self.y+20, fill="green")

    def move_to_island(self):
        while self.x > swim_start_pos :
            speed = 0.05 # Speed in km/s
            time.sleep(speed)
            canvas.moveto(self.draw, self.x, self.y)
            self.x -= 5
            window.update()
        control.i_suppose_i_have_earned_so_much_points(41, [])
        self.move_to_continent()

    def move_to_continent(self):
        while self.x < swim_end_pos :
            speed = 0.05
            time.sleep(speed)
            canvas.moveto(self.draw,self.x, self.y)
            self.x += 5
            window.update()
        control.i_suppose_i_have_earned_so_much_points(42, [self.player])


# Classes
control = Control()
handler = Handler()
ernest = Player("Ernest", 150 ,250, ernest_text_variable)
kernest = Player("Kernest", 150 ,550, kernest_text_variable)
pohteri = Port_Watcher(660, 250, "blue", "Ernest")
eteteri = Port_Watcher(660, 550, "red", "Kernest")

# Draw canvas
canvas.create_rectangle(0, 200, 150, 600, fill='#c2b280') # Island
canvas.create_rectangle(650, 200, 800, 600, fill='green') # Continent
canvas.create_text(70, 185, text="Island", fill="black", font=('Helvetica 15 bold')) # Island text
canvas.create_text(730, 185, text="Continent", fill="black", font=('Helvetica 15 bold')) # Continent text
canvas.place(x=0, y=0)

# Text Variables
info_text_var = tk.StringVar()
info_text_var.set("Send both Ernest's and Kernest's monkey to the continent for testing")
info2_text_var = tk.StringVar()
info2_text_var.set("")
info3_text_var = tk.StringVar()
info3_text_var.set("")
info4_text_var = tk.StringVar()
info4_text_var.set("")

# Upper points texts for "i_suppose_i_have_earned_so_much_points(x)"
frame_upper_text = tk.Frame(window, bg='grey',height=30,width=760, border=True)
frame_upper_text.pack(expand=False, fill="none", side="top", anchor="center", padx=20, pady=20)
text_points_1 = tk.Label(frame_upper_text, text="Points: 1", bg="white", width=20)
text_points_1.pack(side="left", anchor="center")
text_points_2 = tk.Label(frame_upper_text, text="Points: 2", bg="white", width=20)
text_points_2.pack(side="left", anchor="center")
text_points_3 = tk.Label(frame_upper_text, text="Points: 3", bg="white", width=20)
text_points_3.pack(side="left", anchor="center")
text_points_4 = tk.Label(frame_upper_text, text="Points: 4", bg="white", width=20)
text_points_4.pack(side="left", anchor="center")
text_points_5 = tk.Label(frame_upper_text, text="Points: 5", bg="white", width=20)
text_points_5.pack(side="left", anchor="center")
text_info = tk.Label(window, textvariable=info_text_var, height=10, width=70, padx=0, pady=0)
text_info.pack(anchor="center")
text_info2 = tk.Label(window, textvariable=info2_text_var, height=2, width=70, padx=0, pady=0)
text_info2.place(anchor="center", x=400,y=400)
text_info3 = tk.Label(window, textvariable=info3_text_var, height=4, width=70, padx=0, pady=0)
text_info3.place(anchor="center", x=400,y=650)
text_info4 = tk.Label(window, textvariable=info4_text_var, height=4, width=70, padx=0, pady=0)
text_info4.place(anchor="center", x=400,y=700)

# Kernest text and buttons
tk.Label(window, text="Kernest", background="white", width=10).place( x=30,y=520)
btn_kernest_send_monkey = Monkey_Button(text='Send monkey',command=handler.kernest_send_monkey, x=30, y=560, visible=True)
btn_kernest_send_10_monkeys = Monkey_Button(text='+10',command=handler.kernest_send_10_monkeys, x=120, y=560, visible=False)
text_kernest_km = tk.Label(window, textvariable=kernest_text_variable, background="white", width=15).place( x=30,y=575)

# Eernest text and buttons
tk.Label(window, text="Ernest", background="white", width=10).place( x=30,y=215)
btn_ernest_send_monkey = Monkey_Button(text='Send monkey',command=handler.ernest_send_monkey, x=30, y=250, visible=True)
btn_ernest_send_10_monkeys = Monkey_Button(text='+10',command=handler.ernest_send_10_monkeys, x=120,y=250, visible=False)
text_ernest_km = tk.Label(window, textvariable=ernest_text_variable, background="white", width=15, anchor="w").place( x=30,y=265)

window.mainloop()