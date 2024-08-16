# DASHBOARD TUI
The application has servers in binary format for Windows, Linux and FreeBSD. The client is available for FreeBSD and Linux only. Installation and configuration are described below.

## Screenshots

![FreeBSD][1]
![Linux][2]
![Windows][3]
![Menu][4]

[1]: https://github.com/AltairGeo/info-dashboard/blob/main/screenshots/freebsd.png "FreeBSD"
[2]: https://github.com/AltairGeo/info-dashboard/blob/main/screenshots/linux.png "Linux"
[4]: https://github.com/AltairGeo/info-dashboard/blob/main/screenshots/menu.png "Menu"
[3]: https://github.com/AltairGeo/info-dashboard/blob/main/screenshots/windows.png "Windows"

## Instruction

# Server


For linux:
```
wget https://github.com/AltairGeo/info-dashboard/releases/download/Server_and_client/dashtui-server-linux

#Changing launch rights on the server
chmod +x dashtui-server-linux

#Start server
./dashtui-server-linux

#And server started!
#But we also need to create a config, otherwise we will have a standard password and port.

#Paste in $HOME/.config/dashserver.json this:

{
    ip: "",
    port: 1419,
    password: "your password here"
}
```



