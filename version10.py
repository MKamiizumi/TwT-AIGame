import wx
import time
import pygame
#ffpyplayer for playing audio
from ffpyplayer.player import MediaPlayer

timestr = time.strftime("%Y%m%d-%H%M%S")
f = open("chatgpt_log_"+timestr+".txt", "a")

import wx
import os

import openai 
openai.api_key = "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"
messages = [ {"role": "system", "content": "You are a story teller."} ]

weapon1_description="This is the description of weapon 1"
weapon2_description="This is the description of weapon 2"
weapon3_description="This is the description of weapon 3"

# define global variables
process=1
sentence=0
entered_text="please output 'you didn't enter anything' "
prompt1="not yet defined"
prompt2="not yet defined"

script_count=0
script_count_maximum=0

def generate_gpt_response(messages, message_to_append):
    # 将新的消息添加到消息列表
    messages.append({"role": "user", "content": message_to_append})

    # 调用OpenAI GPT
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 获取并返回回复
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply

class MyFrame(wx.Frame):
    global input_text,button_next
    
    def __init__(self, parent, title):

        # 新尺寸
        new_sizex = 1280
        new_sizey = 720

        # 缩放比例
        scale_x = new_sizex / 1440
        scale_y = new_sizey / 810

        super(MyFrame, self).__init__(parent, title=title, size=(1440,810))
        sizex=1440
        sizey=810

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.BLACK)


        # Create Journal description
        self.journal_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(int(401 * scale_x), int(485 * scale_y)))
        self.journal_text.SetPosition((int(38 * scale_x), int(36 * scale_y)))
        self.journal_text.SetValue("Please click 'next' to begin the game")

        # Create foe description
        self.foe_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(int(368 * scale_x), int(210 * scale_y)))
        self.foe_text.SetPosition((int(995 * scale_x), int(27 * scale_y)))
        self.foe_text.SetValue("Danger! Archive before you go on a fight in this dark world! -- Kouya")
        
        # Create weapon description
        self.weapon_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(int(368 * scale_x), int(210 * scale_y)))
        self.weapon_text.SetPosition((int(995 * scale_x), int(277 * scale_y)))
        self.weapon_text.SetValue("Swords, shields, broken hearts... Power! -- Mahiru")

        # Create kouya's chat
        self.kouya_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(int(400 * scale_x), int(130 * scale_y)))
        self.kouya_text.SetPosition((int(750 * scale_x), int(650 * scale_y)))
        self.kouya_text.SetValue("I'm Kouya")

        # Create hiru's chat
        self.hiru_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(int(400 * scale_x), int(130 * scale_y)))
        self.hiru_text.SetPosition((int(250 * scale_x), int(650 * scale_y)))
        self.hiru_text.SetValue("I'm Mahiru")

        # Create send button
        self.input_text = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(int(1000 * scale_x), int(30 * scale_y)))
        self.input_text.SetPosition((int(220 * scale_x), int(820 * scale_y)))
        self.input_text.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        self.input_text.Hide()

        # Create next button
        self.next = wx.Button(panel, label='next', pos=((int(690 * scale_x), int(800 * scale_y))),size=(int(60 * scale_x), int(40 * scale_y)))

        # Create weapon button
        self.weapon1 = wx.Button(panel, label='weapon 1', pos=((int(590 * scale_x), int(550 * scale_y))),size=(int(70 * scale_x), int(30 * scale_y)))
        self.weapon2 = wx.Button(panel, label='weapon 2', pos=((int(687 * scale_x), int(550 * scale_y))),size=(int(70 * scale_x), int(30 * scale_y)))
        self.weapon3 = wx.Button(panel, label='weapon 3', pos=((int(782 * scale_x), int(550 * scale_y))),size=(int(70 * scale_x), int(30 * scale_y)))
        
        
        # Create developer button
        self.developer = wx.Button(panel, label='developer word', pos=((int(1300 * scale_x), int(810 * scale_y))),size=(int(160 * scale_x), int(30 * scale_y)))

        # Set Background Image
        self.bg_image = wx.Image("picture/ProjectH-Jnew4.jpg", wx.BITMAP_TYPE_ANY)
        self.bg_image = self.bg_image.Scale(new_sizex, new_sizey)
        self.bitmap = wx.StaticBitmap(panel, -1, wx.Bitmap(self.bg_image))


        
        # button click process together
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.next)
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.weapon1)
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.weapon2)
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.weapon3)
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.developer)

        # background music
        audio_file_path='audio/To_the_Moon_Main_Theme.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play(loops=-1)

        # Set developer image
        self.dl_image = wx.Image("picture/developers_word.jpg", wx.BITMAP_TYPE_ANY)
        self.dl_image = self.dl_image.Scale(new_sizex, new_sizey)
        self.bitmap_developer = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(self.dl_image))
        self.bitmap_developer.Hide()
        self.developer_on_or_not=0

    def on_enter(self, event):
        global entered_text
        self.input_text = event.GetEventObject()
        entered_text = self.input_text.GetValue()
        print("you entered: "+entered_text)
        self.input_text.Hide()
        self.next.Show()
             
    def on_button_click(self, event):
        button = event.GetEventObject()
        if button == self.next:
            self.reply_message()
        elif button == self.weapon1:
            self.weapon_text.SetValue(weapon1_description)
        elif button == self.weapon2:
            self.weapon_text.SetValue(weapon2_description)
        elif button == self.weapon3:
            self.weapon_text.SetValue(weapon3_description)
        elif button == self.developer:
            if self.developer_on_or_not:
                self.bitmap_developer.Hide()
                self.developer_on_or_not=0
            else:
                self.bitmap_developer.Show()
                self.developer_on_or_not=1
        
        
    def process_script(self,file_path,input_or_not):
        global script_count, script_count_maximum, Lines, process

        # 仅在开始新剧本时读取文件
        if script_count == 0:
            with open(file_path, 'r') as file1:
                Lines = file1.readlines()
            script_count_maximum = len(Lines)

        # 处理当前剧本的行
        if script_count < script_count_maximum:
            line = Lines[script_count].strip()
            script_count += 1

            if line.startswith("Kouy"):
                self.kouya_text.SetValue(line.strip())
            else:
                self.hiru_text.SetValue(line.strip())

        else:
            # 完成当前剧本，准备进入下一个process
            process += 1
            script_count = 0  # 重置script_count为下一个剧本做准备
            if input_or_not == "input needed":
                self.input_text.Show()
                self.input_text.SetValue("please enter your answer here")
                self.next.Hide()
            else:
                self.input_text.Hide()
                self.next.Show()

    def reply_message(self):
        global process
        global entered_text
        global prompt1,prompt2,prompt3,prompt4,prompt5,prompt6,prompt7,prompt8,prompt9,prompt10,prompt11,prompt12
        global script_count, script_count_maximum
        global weapon1_description,weapon2_description,weapon3_description
        global WpnDesc1, WpnDesc2, WpnDesc3
        global FoeDesc1, FoeDesc2, FoeDesc3
        

        if process == 1: 
            # process 1 stage1_story_background

            text = "Kiara's game begins now"
            self.journal_text.SetValue(text)
            self.process_script('txt_script/stage1_story_background.txt','input needed')
        elif process == 2:

            prompt1 = entered_text
            #process 3 stage1_story_future
            self.process_script('txt_script/stage1_story_future.txt','input needed')
            
        elif process == 3: 

            prompt2 = entered_text
            # stage 1 extract emotions based on prompt 1 and prompt 2
            message = "This is someone's nightmare description: " + prompt1 + ". This is a description of his dream of a good future: " + prompt2 + ". Based on the above two description, please help me extract two emotions to create a character's core conflict."
            f.write("Users:" + message)
            f.write("\n")
            f.write("\n")

            # stage 1 chatgpt extract two emotions
            messages.append({"role": "user", "content": message},) 
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})

            # define output1
            output1 = reply
            f.write("Chatgpt:" + output1)
            f.write("\n")
            f.write("\n")
            

            # stage 1 chatgpt create story
            message = "Now, imagine this character is in his dreams, and this nightmare's environment, era, and ruins' materials are constructed around his temperament and past experiences. Based on the character's temperament, please use your imagination to generate a post-apocalyptic world description.Please include three spots according to the details mentioned in " + prompt1 + "and" + prompt2 + "Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)

            # define output2
            output2 = response
            f.write("Chatgpt:" + output2)
            f.write("\n")
            f.write("\n")
            
            self.journal_text.SetValue(output2)

            process += 1

        elif process == 4: 
            #process 4 stage2_story_explore_a

            self.process_script('txt_script/stage2_story_explore_a.txt','input needed')

        elif process == 5: 

            prompt3 = entered_text
            #process5 chatgpt_journal2
            # stage 2 chatgpt create story
            message = "Based on"+prompt3+", please create more details of the world. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)

            # define Journal2
            Journal2=response
            f.write("Chatgpt:"+Journal2)
            f.write("\n")
            f.write("\n")

            self.journal_text.SetValue(Journal2)

            process += 1

        elif process == 6: 

            self.process_script('txt_script/stage2_story_explore_b.txt','no input needed')


        elif process == 7: 

            self.process_script('txt_script/stage3_story_weapon_a.txt','input needed')

        elif process == 8: 

            # stage 3 user input prompt 4
            prompt4 = entered_text

            # stage 3 chatgpt create story
            message = "Based on"+prompt4+", please generate a description of a weapon. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)

            # define WpnDesc
            WpnDesc1=response
            f.write("Chatgpt:"+WpnDesc1)
            f.write("\n")
            f.write("\n")

            self.weapon_text.SetValue("weapon1 is forged, click button to find details")
            weapon1_description=WpnDesc1

            process += 1


        elif process == 9: 

            self.process_script('txt_script/stage3_story_weapon_b.txt','no input needed')

        elif process == 10: 

            self.process_script('txt_script/stage4_story_enemy_a.txt','input needed')

        elif process == 11: 

            #Stage 4 foedesc1 generate
            # stage 4 user input prompt 5
            prompt5 = entered_text

            # stage 4 chatgpt create story
            message = "Based on"+prompt5+", please generate a description of a foe, together with a word from the foe at the end. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 100 words. "
            response = generate_gpt_response(messages, message)

            # define FoeDesc
            FoeDesc1=response
            f.write("Chatgpt:"+FoeDesc1)
            f.write("\n")
            f.write("\n")

            #等到stage5放出来

            #self.foe_text.SetValue(FoeDesc1)

            process += 1

        elif process == 12: 

            self.process_script('txt_script/stage4_story_enemy_b.txt','no input needed')

        elif process == 13: 

            self.process_script('txt_script/stage5_story_encounter_a.txt','no input needed')

        elif process == 14: 

            # stage 5 chatgpt_foedesc1_release,chatgpt_journal3

            # stage 5 chatgpt create story

            message = "Based on"+WpnDesc1+"and"+FoeDesc1+", please generate a description of a fierce fight of the weapon against the foe, within 50 words. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed."
            response = generate_gpt_response(messages, message)

            # define journal3
            Journal3=response
            f.write("Chatgpt:"+Journal3)
            f.write("\n")
            f.write("\n")

            # Release FoeDesc1, set Journal 3

            self.foe_text.SetValue(FoeDesc1)
            self.journal_text.SetValue(Journal3)

            process += 1

        elif process == 15: 

            #Stage 5 Encounter end

            self.process_script('txt_script/stage5_story_encounter_b.txt','no input needed')

        elif process == 16: 

            #Round 2 begin
            #Stage 6 begin

            self.process_script('txt_script/stage6_story_explore_a.txt', 'input needed')

        elif process == 17: 
            prompt6 = entered_text
            message = "Based on" + prompt6 + ", please create more details of the world. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)
            Journal4 = response
            f.write("Chatgpt:" + Journal4)
            f.write("\n\n")
            self.journal_text.SetValue(Journal4)
            process += 1

        elif process == 18: 
            self.process_script('txt_script/stage6_story_explore_b.txt', 'no input needed')

        elif process == 19: 
            self.process_script('txt_script/stage7_story_weapon_a.txt', 'input needed')

        elif process == 20: 
            prompt7 = entered_text
            message = "Based on" + prompt7 + ", please generate a description of a weapon. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)
            WpnDesc2 = response
            f.write("Chatgpt:" + WpnDesc2)
            f.write("\n\n")
            self.weapon_text.SetValue("weapon2 is forged, click button to find details")
            weapon2_description = WpnDesc2
            process += 1

        elif process == 21: 
            self.process_script('txt_script/stage7_story_weapon_b.txt', 'no input needed')

        elif process == 22: 
            self.process_script('txt_script/stage8_story_enemy_a.txt', 'input needed')

        elif process == 23: 
            prompt8 = entered_text
            message = "Based on" + prompt8 + ", please generate a description of a foe, together with a word from the foe at the end. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 100 words. "
            response = generate_gpt_response(messages, message)
            FoeDesc2 = response
            f.write("Chatgpt:" + FoeDesc2)
            f.write("\n\n")
            process += 1

        elif process == 24: 
            self.process_script('txt_script/stage8_story_enemy_b.txt', 'no input needed')

        elif process == 25: 
            self.process_script('txt_script/stage9_story_encounter_a.txt', 'no input needed')

        elif process == 26: 
            message = "Based on" + WpnDesc2 + "and" + FoeDesc2 + ", please generate a description of a fierce fight of the weapon against the foe, within 50 words. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed."
            response = generate_gpt_response(messages, message)
            Journal5 = response
            f.write("Chatgpt:" + Journal5)
            f.write("\n\n")
            self.foe_text.SetValue(FoeDesc2)
            self.journal_text.SetValue(Journal5)
            process += 1

        elif process == 27: 
            self.process_script('txt_script/stage9_story_encounter_b.txt', 'no input needed')

            #Stage 9 ends

        elif process == 28: 

            #Round 3 Begins
            #Stage 10 Begins

            self.process_script('txt_script/stage10_story_explore_a.txt', 'input needed')

        elif process == 29: 
            prompt9 = entered_text
            message = "Based on" + prompt9 + ", please create more details of the world. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)
            Journal6 = response
            f.write("Chatgpt:" + Journal6)
            f.write("\n\n")
            self.journal_text.SetValue(Journal6)
            process += 1

        elif process == 30: 
            self.process_script('txt_script/stage10_story_explore_b.txt', 'no input needed')

        elif process == 31: 
            self.process_script('txt_script/stage11_story_weapon_a.txt', 'input needed')

        elif process == 32: 
            prompt10 = entered_text
            message = "Based on" + prompt10 + ", please generate a description of a weapon. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 150 words. "
            response = generate_gpt_response(messages, message)
            WpnDesc3 = response
            f.write("Chatgpt:" + WpnDesc3)
            f.write("\n\n")
            self.weapon_text.SetValue("weapon3 is forged, click button to find details")
            weapon3_description = WpnDesc3
            process += 1

        elif process == 33: 
            self.process_script('txt_script/stage11_story_weapon_b.txt', 'no input needed')

        elif process == 34: 
            self.process_script('txt_script/stage12_story_enemy_a.txt', 'input needed')

        elif process == 35: 
            prompt11 = entered_text
            message = "Based on" + prompt11 + ", please generate a description of a foe, together with a word from the foe at the end. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed. Please reply in 100 words. "
            response = generate_gpt_response(messages, message)
            FoeDesc3 = response
            f.write("Chatgpt:" + FoeDesc3)
            f.write("\n\n")
            process += 1

        elif process == 36: 
            self.process_script('txt_script/stage12_story_enemy_b.txt', 'no input needed')

        elif process == 37: 
            self.process_script('txt_script/stage13_story_encounter_a.txt', 'no input needed')

        elif process == 38: 
            message = "Based on" + WpnDesc3 + "and" + FoeDesc3 + ", please generate a description of a fierce fight of the weapon against the foe, within 50 words. Use only descriptive language, akin to a narrative in a novel, without any judgmental words. Do not repeat the words I have already typed."
            response = generate_gpt_response(messages, message)
            Journal7 = response
            f.write("Chatgpt:" + Journal7)
            f.write("\n\n")
            self.foe_text.SetValue(FoeDesc3)
            self.journal_text.SetValue(Journal7)
            process += 1

        elif process == 39: 
            self.process_script('txt_script/stage13_story_encounter_b.txt', 'no input needed')

        elif process == 40: 
            self.process_script('txt_script/stage14_story_boss_a.txt', 'no input needed')

        elif process == 41: 
            self.process_script('txt_script/stage14_story_boss_b.txt', 'no input needed')

        elif process == 42: 
            self.process_script('txt_script/stage15_story_past_a.txt', 'input needed') 

        elif process == 43: 
            prompt12 = entered_text
            self.process_script('txt_script/stage15_story_past_b.txt', 'no input needed') 




            
        return True

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Twinborn: Twilight Alpha v0.1 2023-11-29")
        frame.Show(True)
        return True

app = MyApp(False)
app.MainLoop()
