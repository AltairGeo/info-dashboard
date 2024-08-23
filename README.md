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

# Instruction

## Server


For linux:
```
wget https://github.com/AltairGeo/info-dashboard/releases/download/Server_and_client/dashtui-server-linux

#Changing launch rights for the server
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

For freeBSD:
```
wget https://github.com/AltairGeo/info-dashboard/releases/download/Server_and_client/dashtui-server-freebsd

#Changing launch rights for the server
chmod +x dashtui-server-freebsd

#Start server
./dashtui-server-freebsd

#And server started!
#But we also need to create a config, otherwise we will have a standard password and port.

#Paste in $HOME/.config/dashserver.json this:

{
    ip: "",
    port: 1419,
    password: "your password here"
}
```

For Windows just download dash server.exe from releases and start him.


## Client

For linux & FreeBSD
~~~
#Firtsly get the client binary

#For linux
wget https://github.com/AltairGeo/info-dashboard/releases/download/Server_and_client/dashtui-linux-client

#For freebsd
wget https://github.com/AltairGeo/info-dashboard/releases/download/Server_and_client/dashtui-bsd-client

#Change run permissons
chmod +x dashtui-bsd-client #For bsd
#OR
chmod +x dashtui-linux-client #For linux


#Copy to /usr/bin

cp dashtui-bsd-client /usr/bin # for bsd
cp dashtui-linux-client /usr/bin # for linux
~~~


There is no working binary file for windows. But you can run the client for windows as a .py file instead of an .exe file. You can install dependencies using the pip -r requirements.txt command.
