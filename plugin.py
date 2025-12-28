from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from os import system
import socket # Added for internet check

def getIconPath():
    return "/usr/lib/enigma2/python/Plugins/Extensions/KhaledPanel/icon.png"

class KhaledPanelScreen(Screen):
    skin = """
    <screen name="KhaledPanelScreen" position="0,0" size="1920,1080" title="Khaled Tools Panel" flags="wfNoBorder">
        <eLabel position="0,0" size="1920,100" backgroundColor="#202020" zPosition="-1" />
        <widget name="header" position="0,0" size="1920,100" font="Regular;45" halign="center" valign="center" transparent="1" />
        
        <widget name="menu" position="100,200" size="1720,600" font="Regular;40" itemHeight="100" scrollbarMode="showOnDemand" transparent="1" />
        
        <eLabel position="0,850" size="1920,230" backgroundColor="#101010" zPosition="-1" />
        <widget name="status" position="0,850" size="1920,100" font="Regular;35" halign="center" valign="center" transparent="1" />

        <ePixmap pixmap="skin_default/buttons/red.png" position="100,980" size="300,50" alphatest="on" />
        <widget name="key_red" position="100,980" zPosition="1" size="300,50" font="Regular;25" halign="center" valign="center" transparent="1" />
        
        <ePixmap pixmap="skin_default/buttons/blue.png" position="1520,980" size="300,50" alphatest="on" />
        <widget name="key_blue" position="1520,980" zPosition="1" size="300,50" font="Regular;25" halign="center" valign="center" transparent="1" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self["header"] = Label("KHALED TOOLS SYSTEM")
        self["status"] = Label("Checking connection...")
        self["key_red"] = Label("Close")
        self["key_blue"] = Label("Restart GUI")
        
        self.list = [
            ("1. Update Khaled FullSat Channels", "update_channels"),
            ("2. Update EPG", "EPG"),
            ("3. Update Picons", "update_picons"),
            ("4. Update Satellites", "Satellites")
        ]
        
        self["menu"] = MenuList(self.list)
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.runTool,
            "cancel": self.close,
            "red": self.close,
            "blue": self.restartGUI
        }, -1)
        
        # Immediate check on opening
        self.onLayoutFinish.append(self.updateStatus)

    def checkInternet(self):
        try:
            # Try to connect to Google DNS to verify internet access
            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except socket.error:
            return False

    def updateStatus(self):
        if self.checkInternet():
            self["status"].setText("Online - Select a tool and press OK")
        else:
            self["status"].setText("OFFLINE - Please check your network!")

    def runTool(self):
        if not self.checkInternet():
            self.session.open(MessageBox, "Error: No internet connection. Scripts cannot download data.", MessageBox.TYPE_ERROR)
            return

        selection = self["menu"].getCurrent()
        if selection:
            title = selection[0]
            action = selection[1]
            
            scripts = {
                "update_channels": "/media/hdd/Script_New_Edition/TOOL/TOOL-Khaled_Channels_fullsat.sh",
                "EPG": "/media/hdd/Script_New_Edition/TOOL/TOOL-KhaledEpg.sh",
                "update_picons": "/media/hdd/Script_New_Edition/TOOL/TOOL-Khaledpicon_fullsat.sh",
                "Satellites": "/media/hdd/Script_New_Edition/TOOL/TOOL-Satellites_org.sh"
            }
            
            if action in scripts:
                self.session.openWithCallback(self.askedToRestart, Console, title=title, cmdlist=[scripts[action]])

    def askedToRestart(self, result=None):
        self.session.openWithCallback(self.restartConfirmed, MessageBox, "Script execution finished.\nDo you want to restart Enigma2 to apply changes?", MessageBox.TYPE_YESNO)

    def restartConfirmed(self, answer):
        if answer:
            system("killall -9 enigma2")

    def restartGUI(self):
        system("killall -9 enigma2")

def main(session, **kwargs):
    session.open(KhaledPanelScreen)

def Plugins(**kwargs):
    return [PluginDescriptor(name="Khaled Tools Panel", description="Full Screen Panel with Auto-Check", where=PluginDescriptor.WHERE_PLUGINMENU, icon=LoadPixmap(getIconPath()), fnc=main)]

