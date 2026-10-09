Servers, cloud machines, Docker containers and CI runners all run **Linux**, and you control them through the **terminal**. A few dozen commands let you move around, inspect files, search logs and schedule jobs. That is enough for most data and AI engineering work.

!!! tip "Get a Linux terminal"
    - **Windows:** install **WSL** (Windows Subsystem for Linux). Open PowerShell as Administrator, run `wsl --install`, restart, then open **Ubuntu** from the Start menu.
    - **Mac:** open **Terminal**. macOS isn't Linux, but nearly every command in these lessons works the same way.
    - **Linux:** open your terminal.

!!! note "Practice folder"
    Download [linux-practice.zip](../../../downloads/phase-0/linux-practice.zip) and unzip it into your home folder so you have `~/practice`. In WSL you can reach your Windows Downloads folder at `/mnt/c/Users/<you>/Downloads`:

    ```bash
    cd ~
    unzip /mnt/c/Users/<you>/Downloads/linux-practice.zip   # creates ~/practice
    ```

**By the end of this module you can:** navigate and manage files, read and search data and logs, chain commands with pipes, and schedule a script with cron.
