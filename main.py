import customtkinter as ctk
import os
import json
from typing import NoReturn

from user import data
import tkinter as tk
from conf.settings import *
from content.pages import WelcomePage, LoginPage, RegisterPage, ContentPage
from sec.encryption import decrypt_the_content


# Load the json file
# There is only 2 config files: config.json and data.json.
# They are in appropriate user directories to specific OS respectively.
configjson = data.load_config(USER_CONFIG)
datajson = data.load_data(USER_DATA)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.framedict = {}
        self.active_frame = None
        self.configjson = configjson
        self.datajson = datajson

        self.username = None
        self.userkey = None
        self.decrypted_content:dict = None
        self.popup = None
        self.unsaved_changes = False

        self.title(APP_NAME)
        self.geometry("700x500")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.welcomepage = WelcomePage(self)
        self.loginpage = LoginPage(self)
        self.registerpage = RegisterPage(self)
        self.contentpage = ContentPage(self)

        self.welcome_check()

    # Show welcome screen if not shown
    def welcome_check(self) -> NoReturn:
        if not configjson["welcome_shown"]:
            self.add_frame("welcomepage", self.welcomepage)
            self.change_page(None, self.welcomepage)
            data.save_config(USER_CONFIG,"welcome_shown",True)
        else:
            self.add_frame("loginpage", self.loginpage)
            self.change_page(None, self.loginpage)

    # Forget previous page
    # Grid next page
    def change_page(self, from_page, to_page):
        if from_page is not None:
            from_page.grid_forget()
        if to_page is not None:
            to_page.grid(row=0, column=0)

    # Add a object to frame dictionary with string key
    def add_frame(self,name:str, frame:object):
        self.framedict[name] = frame

    def reload_data(self):
        self.datajson = data.load_data(USER_DATA)
        if self.username and self.userkey:
            self.decrypted_content = decrypt_the_content(self.datajson[self.username]["content"], self.userkey)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")

    # My additional settings
    ctk.set_widget_scaling(1.25)
    ctk.DrawEngine.preferred_drawing_method='polygon_shapes'

    app = MainWindow()
    app.mainloop()

