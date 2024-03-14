from pynput import mouse
from PIL import Image
import pyautogui
import os
import requests
import time
import datetime
from icecream import ic

class Functions():
    def __init__(self):
        self.pause_value = False
        self.check = True
        self.temp_variable = True
        self.get_once = True
        self.send_once = False
        self.start = False
        
        self.first_image = r"first_image.png"
        self.second_image = r"second_image.png"
        self.third_image = r"third_image.png"
        self.current_image = r"current_image.png"
        self.current_path = None
        
        self.custom_region = None
        self.confidence_value = None
        self.platform = None
        self.subject = None
        self.sender = None
        self.starting_point = None
        self.file_dict = None
        
        self.current_no = 1
        self.current_method = "discord"
        
        self.first_image_timestamp = []
    
    def createList(self, text_file):
        with open(text_file, "r") as current_file:
            labels = [[word for word in line.split(", ")][:1][0] for _, line in enumerate(current_file.read().splitlines())]
        with open(text_file, "r") as current_file:
            values = [[word for word in line.split(", ")][1:][0:] for _, line in enumerate(current_file.read().splitlines())]

        return labels, values

    def pause(self, pause_button, pause_value, pop_out=False):
        if not pop_out:
            pause_value.set(not pause_value.get())
            self.pause_value = not self.pause_value
            if pause_value.get():
                pause_button.configure(text="Unpause")   
            else:
                pause_button.configure(text="Pause")
        else:
            self.pause_value = not self.pause_value
            if self.pause_value:
                pause_button.configure(text="⏯")   
            else:
                pause_button.configure(text="⏸")

    def add(self, variable, value, button, is_float = True):
        new_value = variable.get() + value
        variable.set(new_value)
        
        if not is_float:
            self.current_no = new_value
        
        if button is None:
            return
        
        new_text = ""
        for word in button.cget("text").split(": "):
            try:
                float(word)
            except ValueError:
                new_text += word
        new_text += ": " if new_text != "" else new_text
        button.configure(text=f"{new_text}%.2f" % new_value) if is_float == True else button.configure(text=f"{new_text}{new_value}")

    def select_region(self, x, y, button, pressed, region_label, image, canvas):
        if button == mouse.Button.left and pressed:
            self.first_pos = x, y
            print('{} at {}'.format('First position is', (x, y)))
            
        if button == mouse.Button.left and not pressed:
            self.second_pos = x, y
            print('{} at {}'.format('Second position is', (x, y)))
            
            if self.second_pos[0] < self.first_pos[0] and self.second_pos[1] < self.first_pos[1]: 
                self.custom_region = (self.second_pos[0], self.second_pos[1], self.first_pos[0]-self.second_pos[0], self.first_pos[1]-self.second_pos[1])
            elif self.second_pos[1] < self.first_pos[1]:
                self.custom_region = (self.first_pos[0], self.second_pos[1], self.second_pos[0]-self.first_pos[0], self.first_pos[1]-self.second_pos[1])
            elif self.second_pos[0] < self.first_pos[0]:
                self.custom_region = (self.second_pos[0], self.first_pos[1], self.first_pos[0]-self.second_pos[0], self.second_pos[1]-self.first_pos[1])
            else:
                self.custom_region = (self.first_pos[0], self.first_pos[1], self.second_pos[0]-self.first_pos[0], self.second_pos[1]-self.first_pos[1])
            region_label.configure(text=f"{self.custom_region}")
            
            print(f"Current region: {self.custom_region}")
            
            pyautogui.screenshot(region=self.custom_region).save(r"preview.png")
            image.configure(light_image=Image.open(r"preview.png"))
            canvas.configure(image=image)
            
            return False
    
    def change_latest_file(self):
        return self.current_path
    
    def prep_detection(self, firebase):
        self.start = not self.start
        
        if self.current_method == "discord":
            if not self.start and self.send_once:
                self.time_spent()
            
            self.send_once = not self.send_once
            
            if self.start:
                if os.path.exists(self.first_image):
                    os.remove(self.first_image)
                if os.path.exists(self.second_image):
                    os.remove(self.second_image)
                if os.path.exists(self.third_image):
                    os.remove(self.third_image)
        elif self.current_method == "local" and not self.start:
            if os.path.exists(self.current_path + f"\{self.first_image}"):
                os.rename(self.current_path + f"\{self.first_image}", self.current_path + f"\{self.starting_point}.png")
            if os.path.exists(self.current_path + f"\{self.second_image}"):
                os.rename(self.current_path + f"\{self.second_image}", self.current_path + f"\{self.starting_point+1}.png")
            if os.path.exists(self.current_path + f"\{self.third_image}"):
                os.rename(self.current_path + f"\{self.third_image}", self.current_path + f"\{self.starting_point+2}.png")
            
            self.current_no = 1
                
    def start_detection(self, start_menu):
        if self.start:
            if self.get_once and self.current_method == "discord":
                self.get_once = not self.get_once
                self.time = time.time()
            
            image, container,\
            confidence_value,\
            sender, subject_label, subject, platform,\
            starting_point,\
            = start_menu.change_values()
            
            if platform == []:
                platform = self.custom_region if self.custom_region != None else (0, 0, 1366, 768)
            else:
                platform = tuple(map(int, platform))
            
            self.subject = subject
            
            if self.temp_variable:
                self.current_no += starting_point - 1
                self.starting_point = starting_point
                self.temp_variable = not self.temp_variable
                
            self.sender = {'authorization': sender[0]}
            
            if not self.pause_value:
                if self.current_method == "discord":
                    if not os.path.exists(self.first_image):
                        print("No first image. Creating...")
                        pyautogui.screenshot(region=platform).save(self.first_image)
                        for item in subject:
                            with open(self.first_image, "rb") as file:
                                self.file_dict = {'': file}
                                self.post(item, image, container, self.first_image)
                    elif not os.path.exists(self.second_image):
                        if self.locate_on_screen(self.first_image, platform, confidence_value) is None:
                            print("No second image to compare to found. Renaming first image to second image")
                            os.rename(self.first_image, self.second_image)
                    elif not os.path.exists(self.third_image):
                        if self.locate_on_screen(self.second_image, platform, confidence_value) is None:
                            print("No third image to compare to found. Renaming second image to third image")
                            os.rename(self.second_image, self.third_image)
                    else:
                        if self.locate_on_screen(self.first_image, platform, confidence_value) is None:
                            if self.locate_on_screen(self.second_image, platform, confidence_value) is None:
                                if self.locate_on_screen(self.third_image, platform, confidence_value) is None:
                                    print(f"Current picture does not match with the three images. Updating: {self.current_no}")
                                    pyautogui.screenshot(region=platform).save(self.current_image)
                                    for item in subject:
                                        with open(self.current_image, "rb") as file:
                                            self.file_dict = {'': file}
                                            self.post(item, image, container, self.current_image)
                                    os.remove(self.third_image)
                                    os.rename(self.second_image, self.third_image)
                                    os.rename(self.first_image, self.second_image)
                                    os.rename(self.current_image, self.first_image)            
                else:
                    if not os.path.exists(subject_label + f" {datetime.date.today()}"):
                        os.mkdir(subject_label + f" {datetime.date.today()}")
                        self.current_path = f"{subject_label} {datetime.date.today()}"
                    else:
                        self.current_path = f"{subject_label} {datetime.date.today()}"
                    
                    if not os.path.exists(self.current_path + f"\{self.first_image}"):
                        print("No first image. Creating...")
                        pyautogui.screenshot(region=platform).save(self.current_path + f"\{self.first_image}")
                        image.configure(light_image=Image.open(self.current_path + f"\{self.first_image}"))
                        container.configure(image=image)
                        self.current_no += 1
                    elif not os.path.exists(self.current_path + f"\{self.second_image}"):
                        if self.locate_on_screen(self.current_path + f"\{self.first_image}", platform, confidence_value) is None:
                            print("No second image to compare to found. Renaming first image to second image")
                            os.rename(self.current_path + f"\{self.first_image}", self.current_path + f"\{self.second_image}")
                    elif not os.path.exists(self.current_path + f"\{self.third_image}"):
                        if self.locate_on_screen(self.current_path + f"\{self.second_image}", platform, confidence_value) is None:
                            print("No third image to compare to found. Renaming second image to third image")
                            os.rename(self.current_path + f"\{self.second_image}", self.current_path + f"\{self.third_image}")
                    else:
                        if self.locate_on_screen(self.current_path + f"\{self.first_image}", platform, confidence_value) is None:
                            if self.locate_on_screen(self.current_path + f"\{self.second_image}", platform, confidence_value) is None:
                                if self.locate_on_screen(self.current_path + f"\{self.third_image}", platform, confidence_value) is None:
                                    pyautogui.screenshot(region=platform).save(self.current_path + f"\{self.current_image}")
                                    image.configure(light_image=Image.open(self.current_path + f"\{self.current_image}"))
                                    container.configure(image=image)
                                    os.rename(self.current_path + f"\{self.third_image}", self.current_path + f"\{self.current_no}.png")
                                    os.rename(self.current_path + f"\{self.second_image}", self.current_path + f"\{self.third_image}")
                                    os.rename(self.current_path + f"\{self.first_image}", self.current_path + f"\{self.second_image}")
                                    os.rename(self.current_path + f"\{self.current_image}", self.current_path + f"\{self.first_image}")
                                    self.current_no += 1
        return self.current_no
    def locate_on_screen(self, image, platform, confidence_value):
        try:
            return pyautogui.locateOnScreen(image, region=platform, confidence=confidence_value)
        except:
            return None
    def time_spent(self):
        today = datetime.date.today()
        d2 = today.strftime("%B %d, %Y")
        
        seconds = int(time.time() - self.time)
        
        minutes = int(seconds / 60)
        seconds -= minutes * 60
        
        hours = int(minutes / 60)
        minutes -= hours * 60
        
        for item in self.subject:
            requests.post(url='https://discord.com/api/v8/channels/'+item+'/messages', data={'content': f"{d2}\n\nClass lasted for {hours} hour/s, {minutes} minute/s, and {seconds} second/s\n────────────────"}, headers=self.sender)
        
        self.get_once = not self.get_once
        self.temp_variable = not self.temp_variable
        self.current_no = 1
    
    def post(self, subject, image, canvas, image_path):
        if self.first_image_timestamp == []:
            timestamp = requests.post(url='https://discord.com/api/v8/channels/'+subject+'/messages', files=self.file_dict, data={'content': f'{self.current_no}'}, headers=self.sender)
            self.first_image_timestamp = self.take_timestamp(timestamp.json())
        else:
            requests.post(url='https://discord.com/api/v8/channels/'+subject+'/messages', files=self.file_dict, data={'content': f'{self.current_no}'}, headers=self.sender)
        
        image.configure(light_image=Image.open(image_path))
        canvas.configure(image=image)
        self.current_no += 1

    def take_timestamp(self, timestamp):
        starting_date = timestamp['timestamp'].split('-')
        current_timestamp = [int(value) for value in starting_date[:2]]
        current_timestamp.append(int(starting_date[2][:2]))
        return current_timestamp
        
    def manual_screenshot(self, start_menu):
        image, container,\
        confidence_value,\
        sender, subject_label, subject, platform,\
        starting_point,\
        = start_menu.change_values()
        
        if platform == []:
            platform = self.custom_region if self.custom_region != None else (0, 0, 1366, 768)
        else:
            platform = tuple(map(int, platform))
        
        self.subject = subject
        
        if self.temp_variable:
            self.current_no += starting_point - 1
            self.starting_point = starting_point
            self.temp_variable = not self.temp_variable
            
        self.sender = {'authorization': sender[0]}
        
        if self.current_method == "discord":
            pyautogui.screenshot(region=platform).save(self.current_image)
            for item in subject:
                with open(self.current_image, "rb") as file:
                    self.file_dict = {'': file}
                    self.post(item, image, container, self.current_image)
        else:
            if not os.path.exists(subject_label + f" {datetime.date.today()}"):
                os.mkdir(subject_label + f" {datetime.date.today()}")
                self.current_path = f"{subject_label} {datetime.date.today()}"
            else:
                self.current_path = f"{subject_label} {datetime.date.today()}"
            
            pyautogui.screenshot(region=platform).save(self.current_path + f"\{self.current_image}")
            image.configure(light_image=Image.open(self.current_path + f"\{self.current_image}"))
            container.configure(image=image)
            if os.path.exists(self.current_path + f"\{self.third_image}"):
                os.rename(self.current_path + f"\{self.third_image}", self.current_path + f"\{self.current_no}.png")
            if os.path.exists(self.current_path + f"\{self.second_image}"):
                os.rename(self.current_path + f"\{self.second_image}", self.current_path + f"\{self.third_image}")
            if os.path.exists(self.current_path + f"\{self.first_image}"):
                os.rename(self.current_path + f"\{self.first_image}", self.current_path + f"\{self.second_image}")
            os.rename(self.current_path + f"\{self.current_image}", self.current_path + f"\{self.first_image}")
            self.current_no += 1

        return self.current_no

    def delete_previous(self, start_menu):
        image, container,\
        confidence_value,\
        sender, subject_labels, subject, platform,\
        starting_point,\
        = start_menu.change_values()
                
        if platform == []:
            platform = self.custom_region if self.custom_region != None else (0, 0, 1366, 768)
        else:
            platform = tuple(map(int, platform))
        
        self.sender = {'authorization': sender[0]}
        self.subject = subject
        
        if self.current_method == "discord":
            for item in subject:
                data = requests.get(url='https://discord.com/api/v8/channels/'+item+'/messages', headers=self.sender).json()
                for value in data:
                    if value['content'] == str(self.current_no-1) and self.take_timestamp(value) >= self.first_image_timestamp:
                        requests.delete(url='https://discord.com/api/v8/channels/'+item+'/messages/'+value['id'], headers=self.sender)
                        self.current_no -= 1
                        break
        
        return self.current_no

    def replace_current(self, start_menu):
        self.delete_previous(start_menu)
        self.manual_screenshot(start_menu)
        return self.current_no
    
    def change_method(self, method):
        self.current_method = method
    
    def send_note(self, note, start_menu):
        image, container,\
        confidence_value,\
        sender, subject_labels, subject, platform,\
        starting_point,\
        = start_menu.change_values()
        
        self.sender = {'authorization': sender[0]}
        self.subject = subject
        
        note = f"For #{self.current_no-1 if self.current_no != None else None}: {note}"
        
        for item in subject:
            requests.post(url='https://discord.com/api/v8/channels/'+item+'/messages', data={'content': note}, headers=self.sender)