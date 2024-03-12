import optparse
import re
import subprocess
import flet as ft


class MacChanger:
    def __init__(self, interface, new_mac):
        self.interface = interface
        self.new_mac = new_mac

    def validate_mac(self):
        if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", self.new_mac.lower()):
            return True
        else:
            return False

    def change_mac(self):
        if not self.interface:
            print("[-] Please specify an interface.")
            return
        elif not self.new_mac:
            print("[-] Please specify a new mac.")
            return
        elif not self.validate_mac():
            print("[-] Please provide a valid MAC address.")
            return
        else:
            print("[+] Changing MAC address for " + self.interface + " to " + self.new_mac)
            print("""
 _______   __          __       __   ______    ______                                                                          
|       \ |  \        |  \     /  \ /      \  /      \                                                                         
| $$$$$$$\ \$$        | $$\   /  $$|  $$$$$$\|  $$$$$$\                                                                        
| $$__| $$|  \ ______ | $$$\ /  $$$| $$__| $$| $$   \$$                                                                        
| $$    $$| $$|      \| $$$$\  $$$$| $$    $$| $$                                                                              
| $$$$$$$\| $$ \$$$$$$| $$\$$ $$ $$| $$$$$$$$| $$   __                                                                         
| $$  | $$| $$        | $$ \$$$| $$| $$  | $$| $$__/  \                                                                        
| $$  | $$| $$        | $$  \$ | $$| $$  | $$ \$$    $$                                                                        
 \$$   \$$ \$$         \$$      \$$ \$$   \$$  \$$$$$$                                                                         
                                                                                                                               
                                                                                                                               
                                                                                                                               
  ___  __  _______                                                                                      __        __    __     
 /   \|  \|       \                                                                                    |  \      |  \  |  \    
|  $$$\ $$| $$$$$$$\ __    __         ______   _______   __    __   ______   ______    ______          | $$____   \$$ _| $$_   
| $$\$$ $$| $$__/ $$|  \  |  \       |      \ |       \ |  \  |  \ /      \ |      \  /      \  ______ | $$    \ |  \|   $$ \  
 \$$ \$$$ | $$    $$| $$  | $$        \$$$$$$\| $$$$$$$\| $$  | $$|  $$$$$$\ \$$$$$$\|  $$$$$$\|      \| $$$$$$$\| $$ \$$$$$$  
          | $$$$$$$\| $$  | $$       /      $$| $$  | $$| $$  | $$| $$   \$$/      $$| $$  | $$ \$$$$$$| $$  | $$| $$  | $$ __ 
          | $$__/ $$| $$__/ $$      |  $$$$$$$| $$  | $$| $$__/ $$| $$     |  $$$$$$$| $$__| $$        | $$__/ $$| $$  | $$|  \
          | $$    $$ \$$    $$       \$$    $$| $$  | $$ \$$    $$| $$      \$$    $$ \$$    $$        | $$    $$| $$   \$$  $$
           \$$$$$$$  _\$$$$$$$        \$$$$$$$ \$$   \$$  \$$$$$$  \$$       \$$$$$$$ _\$$$$$$$         \$$$$$$$  \$$    \$$$$ 
                    |  \__| $$                                                       |  \__| $$                                
                     \$$    $$                                                        \$$    $$                                
                      \$$$$$$                                                          \$$$$$$                                 
""")
            try:
                subprocess.check_call(["sudo", "ifconfig", self.interface, "down"])
                subprocess.check_call(["sudo", "ifconfig", self.interface, "hw", "ether", self.new_mac])
                subprocess.check_call(["sudo", "ifconfig", self.interface, "up"])
            except subprocess.CalledProcessError as e:
                print(f"[-] Failed to change MAC address: {e}")


def core_execution():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    mac_changer = MacChanger(options.interface, options.new_mac)
    mac_changer.change_mac()


def main(page: ft.Page):
    t = ft.Text(value="Hello, world!", size=80, color="green")
    page.add(t)
    page.update()
    pass


ft.app(target=main)

if __name__ == "__main__":
    main()
