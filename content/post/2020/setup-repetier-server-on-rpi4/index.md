---
title: "Setup Repetier Server on Rpi4"
date: 2020-05-04T22:20:07-07:00
draft: true
---

# TL;DR

I bought a new Raspberry PI 4 with more memory that is connected to my 3D printer. The old Raspi was a tad slow when if came to uploading, processing the print jobs.
These are my notes on how to install Repetier Server on Raspian from scratch. I know that the company behind Repetier Server has an image with everything, but I wanted to do it myself to understand better how things are working.

https://www.repetier-server.com/booting-into-touchscreen-mode-for-linux/
https://www.waveshare.com/product/displays/lcd-oled/lcd-oled-1/5inch-hdmi-lcd-g.htm
https://www.waveshare.com/wiki/5inch_HDMI_LCD_(H)
https://gist.github.com/dudewheresmycode/154df74824aadef2b8c1b8a6bccb66c7

Download Repetier-Server
wget http://download.repetier.com/files/server/debian-armel/Repetier-Server-0.93.1-Linux.deb -O Repetier-Server-0.93.1-Linux.deb

Install
sudo dpkg -i Repetier-Server-0.93.1-Linux.deb


1  ls
    2  htop
    3  exit
    4  sudo shutdown -h now
    5  ls
    6  wget
    7  wget http://download.repetier.com/files/server/debian-armel/Repetier-Server-0.93.1-Linux.deb -O Repetier-Server-0.93.1-Linux.deb
    8  sudo dpkg -i Repetier-Server-0.93.1-Linux.deb
    9  sudo service RepetierServer start
   10  ifconfig
   11  ls
   12  cd ..
   13  ls
   14  cd ..
   15  ls
   16  cd boot/
   17  ls
   18  cat config.txt
   19  nano config.txt
   20  sudo nano config.txt
   21  sudo reboot
   22  pwd
   23  ls
   24  exit
   25  htop
   26  cd /usr/local/Repetier-Server/
   27  ls
   28  cd www/
   29  ls
   30  cd ..
   31  ls
   32  cd etc/
   33  ls
   34  less RepetierServer.xml
   35  ls -al /var/lib/Repetier-Server/
   36  ls -al /var/lib/Repetier-Server/configs/
   37  ls -al /var/lib/Repetier-Server/database/
   38  ls
   39  pwd
   40  htop
   41  sudo service RepetierServer stop
   42  ifconfig
   43  ls
   44  sudo mv *.xml /var/lib/Repetier-Server/configs/
   45  ls
   46  sudo mv *.xml.bak /var/lib/Repetier-Server/configs/
   47  ls -al /var/lib/Repetier-Server/
   48  mkdir /var/lib/Repetier-Server/Prusa_i3
   49  sudo mkdir /var/lib/Repetier-Server/Prusa_i3
   50  sudo service RepetierServer start
   51  htop
   52  sudo raspi-config
   53  sudo apt get update
   54  sudo apt update
   55  sudo apt upgrade
   56  ifconfig
   57  uname -a
   58  sudo service RepetierServer stop
   59  sudo service RepetierServer start
   60  apt install ffmpeg
   61  sudo apt install ffmpeg
   62  which ffmpeg
   63  v4l2-ctl
   64  v4l2-ctl --list-formats-ext
   65  v4l2-ctl --list-formats-ext /dev/video0
   66  v4l2-ctl --list-formats-ext -d /dev/video0
   67  dmesg
   68  raspistill
   69  raspistill -vf -hf -o cam2.jpg
   70  ls
   71  ls -al
   72  rm cam2.jpg
   73  ls
   74  cat /usr/local/Repetier-Server/etc/RepetierServer.xml
   75  pwd
   76  ls
   77  ls -al
   78  if config
   79  ifconfig
   80  cd /usr/local/Repetier-Server/bin/
   81  ls
   82  ./RepetierInstaller
   83  ./RepetierInstaller -h
   84  ./RepetierInstaller ../etc/RepetierServer.xml
   85  sudo /usr/local/Repetier-Setup/bin/startAllCams
   86  ifconfig
   87  sudo reboot
   88  ls -al /dev/v4l/
   89  ls -al /dev/v4l/by-path/
   90  ls -al /usr/local/bin/
   91  ifconfig
   92  sudo apt-get install libjpeg8-dev imagemagick libv4l-dev v4l-utils make gcc git cmake g++
   93  git clone https://github.com/jacksonliam/mjpg-streamer.git
   94  cd mjpg-streamer/mjpg-streamer-experimental/
   95  cmake -G "Unix Makefiles"
   96  make -j4
   97  sudo make install
   98  sudo su
   99  cd /boot/
  100  ls
  101  nano config.txt
  102  sudo su
  103  ls
  104  cd /boot/
  105  sudo su
  106  nano config.txt
  107  sudo su
  108  ps aux | grep open
  109  /usr/local/Repetier-Setup/bin/runAtBoot
  110  sudo raspi-config
  111  reboot
  112  sudo reboot
  113  htop
  114  less /var/lib/Repetier-Server/logs/server.log
  115  ls -al /boot/
  116  startx
  117  api install chromium-browser rpi-chromium-mods
  118  apt install chromium-browser rpi-chromium-mods
  119  sudo apt install chromium-browser rpi-chromium-mods
  120  sudo raspi-config
  121  mkdir -p ~/.icewm
  122  nano ~/.icewm/startup
  123  touch ~/.xsession
  124  nano ~/.xsession
  125  sudo apt install xinit
  126  sudo reboot
  127  sudo raspi-config
  128  ls
  129  ls -al
  130  less .xsession
  131  less .xsession-errors
  132  sudp apt find icewm
  133  sudo apt find icewm
  134  sudo apt search icewm
  135  sudo apt install icewm
  136  sudo reboot
  137  ls
  138  less .xsession-errors
  139  less .xsession
  140  nano .bashrc
  141  cat .icewm/startup
  142  ls -al .icewm/startup
  143  chmod 755 .icewm/startup
  144  ls -al
  145  ls -al .icewm/startup
  146  sudo reboot
  147  ls
  148  exit