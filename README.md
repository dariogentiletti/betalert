# BetAlert v0.2

Welcome to **BetAlert** -- please make sure you look at the license before using this repository.

The purpose of this software is to provide an advanced notification system on your computer to be updated every second on the latest tipster websites.

The current version of BetAlert only provides notifications from *Soccer-Rating.com*'s tipster pages.
# Requirements:
```
* requests
* re
* notify2 *(for Ubuntu version)*
* win10toast *(for Windows version)*
* BeautifulSoup
* time
* sys 
```

# Installation:

## Ubuntu 18.04:
* Clone the repo (or click Download on the top right of the main page)
* Navigate in the folder that matches your OS (*ubuntu*)
* Run the following command in the terminal
```
python3 betalert.py
```

#### (Optional, to add the tipsters you want to be notified of)

Edit the file data.py in the *ubuntu/* folder, making sure to follow the original format:
```
tipsters_url = { "name of the tipster" : "URL of the tipster from http://www.soccer-rating.com/picks?top=1"}
```

## Windows 10:
* Clone the repo (or click Download on the top right of the main page)
* Navigate in the folder that matches your OS (*windows*)
* Open the folder 'dist'
* Launch the executable file

#### (Optional, to add tipsters you want to be notified of)

The default are two of the main tipsters of Soccer-Rating.com. To edit the tipsters you want to be alerted from Soccer-Rating.com, you need to change the file *data.py* in the *windows/* folder.
When changing, it is important to follow the same format of the original one
```
tipsters_url = { "name of the tipster" : "URL of the tipster from http://www.soccer-rating.com/picks?top=1"}
```
After, rebuild the executable. To rebuild the executable, open a terminal in the *betalert/windows/* folder and run:

```
pyinstaller --onefile betalert_win.py
```

Completed the script, you will be able to find the new executable file in the *betalert/windows/dist/* folder.

# Roadmap:
* [X] Build a Windows 10 version
* [X] Make an executable of the python script
* Integrate an user-friendly GUI
* Add a dynamic way to add tipsters through GUI
