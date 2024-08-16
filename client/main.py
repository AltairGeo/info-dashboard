from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Grid, Horizontal, Container, Center
from textual.widgets import Button, Static, Label, Footer, Header, Input, ProgressBar
import sqlite3 as sq
import logos
import client
import asyncio
import os


#For linux and freebsd
#DB_PATH = os.path.join(os.environ['HOME'], '.local/lib/servers.db')


#For windows
DB_PATH = "./servers.db"


class DashBoard(Screen):
    CSS_PATH = "Dashboard.tcss"
    BINDINGS = [("x", 'exit', 'Exit from DashBoard')]

    

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static()
        yield Grid(
                Container(Static(id="os_icon",shrink=True, expand=True),id="OS"),
                Container(
                    Container(Label("CPU:"),ProgressBar(total=100,show_eta=False, id="cpubar"), id="CpuBAR"),
                    Label("Cpu cores:", id="cores"),
                    Label("Uptime:", id="uptime"),
                    Label("Non", id="Arch"),
                    id="CPU"),
                Container(
                    Label("Total RAM", id="totalramlabel"),
                    Container(Label("RAM:", id="label_ram"),ProgressBar(total=100,show_eta=False, id="rambar")),
                    Label("Total swap:", id='totalswap'),
                    Container(Label("Swap:", id='usedswap'), ProgressBar(total=100, show_eta=False, id='swapbar'))
                , id="RAM"),
                Container(Label("Total space in root:", id="total_space"),
                Container(Label("Used: ", id="used_space"),ProgressBar(total=100, show_eta=False, id="spacebar")),
                Label("Disk speed:"),
                Label(id="disk_read"),
                Label(id="disk_write"),
                Label(),
                Label("Network speed:"),
                Label(id="download"),
                Label(id="upload"),
                id="DRIVE"),
                id="Base"
            )


    async def on_mount(self) -> None:
    
        self.query_one("#RAM").border_title = "RAM & SWAP"
        self.query_one("#DRIVE").border_title = "DISK & NETWORK"
        try:
            db = sq.connect(DB_PATH)
            cursor = db.cursor()
            cursor.execute("""
            SELECT * FROM servers
            WHERE ID = ?
            """, (self.idis, ))
            for i in cursor:
                self.ip = i[3]
                self.port = int(i[4])
                self.passwd = i[2]

            cursor.close()
            db.close()

            firtly_data = await client.get_first_data(self.ip, self.port, self.passwd)
            self.title = str(firtly_data['hostname'])
            if firtly_data['platform'] == "linux":
                self.query_one("#os_icon").update(logos.tux)
                self.query_one("#OS").styles.color="green";
                self.query_one("#OS").add_class("grid-linux")
                self.query_one("#CPU").add_class("grid-linux")
                self.query_one("#RAM").add_class("grid-linux")
                self.query_one("#DRIVE").add_class("grid-linux")

                #self.query_one("#OS").add_class()

            elif firtly_data['platform'] == "win32":
                self.query_one("#os_icon").update(logos.windows)
                self.query_one("#OS").styles.color="blue"
                self.query_one("#OS").add_class("grid-windows")
                self.query_one("#CPU").add_class("grid-windows")
                self.query_one("#RAM").add_class("grid-windows")
                self.query_one("#DRIVE").add_class("grid-windows")

            elif firtly_data['platform'] == "darwin":
                self.query_one("#os_icon").update(logos.macos)
                self.query_one("#OS").styles.color="yellow"

            elif firtly_data['platform'][0:7] == "freebsd":
                self.query_one("#os_icon").update(logos.bsd)
                self.query_one("#OS").styles.color="red"
                self.query_one("#OS").add_class("grid-bsd")
                self.query_one("#CPU").add_class("grid-bsd")
                self.query_one("#RAM").add_class("grid-bsd")
                self.query_one("#DRIVE").add_class("grid-bsd")
            else:
                self.query_one("#os_icon").update(logos.windows)
            cpu = firtly_data['cpu'] + " "
            self.query_one("#CPU").border_title = cpu   
            self.query_one("#Arch").update(firtly_data['arch'])
            self.query_one("#cores").update(f"CORES: {str(firtly_data['cpu_cores'])}")

            #self.run_worker(self.update_indicators(self.ip, self.port, self.passwd))
            #self.run_worker(self.update_net(self.ip, self.port, self.passwd))
            asyncio.create_task(self.update_indicators(self.ip, self.port, self.passwd))
            asyncio.create_task(self.update_net(self.ip, self.port, self.passwd))
        except Exception as e:
            self.app.pop_screen()
            self.notify("Connection error!")

    async def update_net(self, ip: str, port: int, passw: str) -> None:
        while True:
            try: 
                net = await client.get_network_speed(ip, port, passw)
                self.query_one("#download").update(f"Download {net[0]} kb/s")
                self.query_one("#upload").update(f"Upload {net[1]} kb/s")
                self.query_one("#disk_read").update(f"Disk read:  {round(net[2])} mb/s")
                self.query_one("#disk_write").update(f"Disk write: {round(net[3])} mb/s")
                await asyncio.sleep(1)
            except Exception as e:
                break

    async def update_indicators(self, ip: str, port: int, passw: str) -> None:
        while True:
            try:

                indi = await client.get_indicat(ip, port, passwd=passw)
                self.query_one("#uptime").update(f"uptime: {indi['uptime'].split(sep='.')[0]}")
                self.query_one("#cpubar").update(progress=int(indi['cpu_load']))
                self.query_one("#totalramlabel").update(f"Total RAM:{indi['ram_total']} MB")
                self.query_one("#rambar").update(progress=int(indi['ram_percent']))
                self.query_one("#label_ram").update(f"RAM: {indi['ram_used']} MB")
                self.query_one("#totalswap").update(f"Total swap: {indi['swap_total']} MB")
                self.query_one("#usedswap").update(f"Swap: {indi['swap_used']} MB")
                self.query_one("#swapbar").update(progress=int(indi['swap_percent']))
                self.query_one("#total_space").update(f"Total space in root: {indi['/'][0]} MB")
                self.query_one("#used_space").update(f"Use: {indi['/'][1]} MB")
                space_percent = indi['/'][1] / (indi['/'][0] / 100)
                self.query_one("#spacebar").update(progress=space_percent)

                await asyncio.sleep(1)
            except Exception as e:
                break


    def __init__(self, idi=None, ip=None, port=None, passwd=None, icon=None)-> None:
        super().__init__()
        self.idis = idi
        self.ip = ip 
        self.port = port
        self.passwd = passwd

    def set_idis(self, idis):
        self.idis = idis

    def action_exit(self) -> None:
        self.app.pop_screen()


class Addserver(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter name:", id="servername", type='text')
        yield Input(placeholder="Enter password:", id='serverpass', password=True)
        yield Input(placeholder="Enter IP:", id='serverip', type='text')
        yield Input(placeholder="Enter port:", id='serverport', type='integer')

        with Horizontal(id='aserv-container'):
            yield Button.success("Ok", id="OK")
            yield Button.error("Cancel", id="CANCEL")
            

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "CANCEL":
            self.app.pop_screen()
        if button_id == "OK":
            self.servname = self.query_one("#servername", Input).value
            servpass = self.query_one("#serverpass", Input).value
            servipad = self.query_one("#serverip", Input).value
            servport = int(self.query_one("#serverport", Input).value)
            
            
            db = sq.connect(DB_PATH)
            cur = db.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS servers (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            PASS TEXT,
            IP TEXT,
            PORT INTEGER
            )
            """)
            cur.execute("""
            INSERT INTO servers (NAME, PASS, IP, PORT) VALUES (?, ?, ?, ?);
            """, (self.servname, servpass, servipad, servport))
            db.commit()
            cur.close()
            
            cursor = db.cursor()
            cursor.execute("""
            SELECT ID FROM servers
            WHERE NAME = ?
            """, (self.servname,))
            for i in cursor:
                idss = i[0]
            self.query_one("#servername", Input).value = ""
            self.query_one("#serverpass", Input).value = ""
            self.query_one("#serverip", Input).value = ""
            self.query_one("#serverport", Input).value = ""
            
            
            self.app.pop_screen()
            self.app.query_one("#servers").mount(ServerWidg(ids=idss,  name=str(self.servname)))
            self.notify("Successfully!")
            cur.close()
            db.close()




class ServerWidg(Static):
    def __init__(self, name, ids):
        super().__init__()
        self.name_serv = name
        self.idi = ids    

    def compose(self) -> ComposeResult:
        yield Label(self.name_serv, id='server_name')
        yield Button("Enter!", id='ENTER', variant='error')
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ENTER":
            self.app.push_dashboard(self.idi)
            #self.app.push_screen(DashBoard())
            #self.app.get_screen("DashBoard").set_idis(self.idi)
            #app.push_screen(DashBoard(idis=self.idi))

    def return_id(self):
        return self.idi


class Tuapp(App):
    log_file = "error.log"
    log_level = "ERROR"
    CSS_PATH = "tuapp.tcss"
    
    BINDINGS = [
                ("d", "toggle_dark", "Toggle dark mode"),
                ("a", "push_screen('AddServer')", "Add server to list"),
                ("R", "remove_server", "Remove last server in list")
                ]
    SCREENS = {"AddServer": Addserver(), "DashBoard": DashBoard(idi=None)}
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Grid(id='servers')

    
    def initi(self):
        db = sq.connect(DB_PATH)
        cur = db.cursor()
        try:
            cur.execute("""
            SELECT * FROM servers;
            """)
            for i in cur:
                print(i)
                self.query_one("#servers").mount(ServerWidg(name=i[1],ids=i[0]))
            cur.close()
            db.close()
        except:
            cur.close()
            db.close()

        

    def on_mount(self) -> None:
        self.action_reload()
        self.title = 'Dashtui'  
    
    def action_reload(self) -> None:
        self.initi()

    def push_dashboard(self, idis):
        self.push_screen(DashBoard(idi=idis))

    
    def action_remove_server(self) -> None:
        servers = self.query("ServerWidg")
        if servers:
            ids = servers.last().return_id()
            db = sq.connect(DB_PATH)
            cur = db.cursor()
            cur.execute("""
            DELETE FROM servers
            WHERE ID = ?
            """, (ids, ))
            db.commit()
            cur.close()
            db.close()
            servers.last().remove()

if __name__ == "__main__":
    app = Tuapp()
    app.run()
