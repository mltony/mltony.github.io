---
layout: post
title: "Debugging NVDA with VSCode"
date:  2024-02-24
categories: debug python NVDA VSCode
---
# Debugging NVDA with VSCode
I've recently spent some time debugging NVDA code while implementing some new features. And I thought I'd share my setup - maybe someone will find this useful. Here I'll describe how to debug NVDA running on a virtual machine inside VMWare Player, but these instructions are applicable to debugging any python application in general.

Why debugging is cool? When you connect to a running instance of NVDA with a debugger you can instantly get much more information about its current state. Here are some scenarios where I find debugging especially useful:
* Setting a breakpoint on a method to figure out where it's called from. Once your breakpoint is hit you can easily inspect call stack in VSCode.
* Stepping through your function to understand at which point its internal state starts to deviate from intended.
* Stepping through someone else's code to better understand how it works.

Why do we need to debug in VMWare? Welll once your program - NVDA in this case - hits a breakpoint, it'll be frozen - thus you can't debug the instance of NVDA that you're running. So we need to debug another instance, running on another computer. I didn't have another computer readily available, so a virtual machine is another good option. But these instructions are also relevant for remote debugging on another computer.

## Steps
### 1. Get Microsoft Windows 10 ISO file
    We will download a copy of Microsoft Windows 10 directly from Microsoft. Apparently authorization key is not needed to run it, although it will bug you to enter authorization key every now and then.
    1. Go to https://www.microsoft.com/software-download/windows10
    2. Click Download now
    3. Run it and tell it to create an installation media. Select "Create DVD" as media type and save  it on the computer.
    4. Don't burn the iso file on the dvd.
### 2. Set up VMWare Player virtual machine
    1. Install vmware player
    2. Go to File > Create virtual machine
    3. Select ISO file created in the previous section
    4. Choose all default options and proceed with creating VM.
    5. Start VM
### 3. Quidck VMWare primer
    For anyone who hasn't played with virtual machines:
    1.Virtualization terms:
        * Host OS - your current Windows installation - that is operating system running on your hardware.
        * Guest OS - what you are about to install, that is operating system running inside VMWare player
    2. In order to switch to guest OS (or in other words, capture input), press `Control+Alt+Enter`. Sometimes you need to press it twice.
    3. In order to switch back to host OS, press `Control+Alt`.
    4. By default guest OS is not running a screenreader. SO a good way to check that you're in is by pressing e.g. `Alt+Tab` - if your input is captured, you won't hear any speech feedback.
### 4. Installing Windows
    1. Switch to guest OS
    2. Verify that you're in by pressing `Alt+Tab` - if no speech then you're in.
    2. Turn on narrator by pressing `Control+Windows+Enter`
    3. Proceed with setup using defrault options. 
    4. Specify that you don't have license key.
    5. Select "Windows 10 Pro" as the operating system to install.
    6. Select Custom as installation type (as opposed to upgrade)
    7. Select the only drive available in the table for installation.
    8. Proceed with installation and copying files step. This step takes less  than 10 minutes on a reasonably modern modest PC.
    9. While installation is running, you can try `NVDA+R` to OCR the contents of the entire window - sometimes it gives you an idea what it is working on when guest narrator is not running.
    10. Wait until OCR says something like:
        > Basics
        > Let's start with region. Is this right?
        > U.S. Minor Outlying Islands
        > ...
    11. Capture input and press `Control+Windows+Enter` to start narrator again. Now narrator speaks in a different voice.
    12. Proceed with specifying default options.
    13. When it prompts for your email address, I recommend to use an offline account, but I would think that online account would work too, so use your best judgement.
    14. Keep selecting default options until installation is complete.
    15. You can tell that the installation is complete when `Windows` key brings up start menu.
### 5. Installing VMWare tools
    VMWare tools provide better integration between guest and host systems. In particular shared clipboard and shared folders are two features that we definitely need.
    1. In VMWare player navigate to Menu > Install VMWare Tools
    3. In guest OS, press `Windows+R` and run `D:\setup64.exe`. 
    4. Proceed with installation. Select "Typical installation" if prompted.
    5. Restart guest OS as requested by VMWare Tools installer.
### 6. Setting up shared drive
    Important note! In order to make debugging easier, it is very convenient to have yourdevelopment NVDA repository accessible via the same path in both host and guest OS's. This can be easily done by mapping drives. For example, on your host OS, you can run:
    * `subst H: C:\Users\tony` which would map drive `H:` to my home directory - obviously replace `tony` with  your username.
    * Then Map host drive `H:` as guest drive `H:`.
    * Clone NVDA repository from github somewhere on drive `H:`, for example to `H:\nvda`, so that you can access it both from host and guest OS using exactly the same path.
    Now let's set up a shared folder:
    1. In VMWare player navigate to Menu > Manage > Virtual Machine Settings...
    2. Switch to options tab.
    3. In the list view select Shared folders.
    4. Select "Always enabled".
    5. Check "Map as a network drive in Windows guests"
    6. Click "Add".
    7. Select `H:\` as host path and select `H:` as guest drive name.
    8. Press OK.
    9. Capture input in your guest OS.
    10. Press `Windows+E` to open file explorer and type `\\vmware-host\Shared Folders\H` to verify that you can access shared drive.
    11. In command line in guest OS, type:
        ```
        subst H: "\\vmware-host\Shared Folders\H"
        ```
        Be sure to have the second argument in quotes, since share name contains a whitespace.
    12. Open command line in administrator mode in guest OS. E.g. Press `Windows+R`, then type cmd and press `Control+windows+Shift+Enter`
    13. Run the same command there to also make H: available in Administrator mode.
        ```
        subst H: "\\vmware-host\Shared Folders\H"
        ```
    14. Now in your guest OS drive `H:` should be available and should be identical to your host drive `H:`.
    15. Whenever you restart your guest OS, you will need to execute `subst` commands mentioned above again.
### 7. Install NVDA in guest OS
    Now use your shared `H:` drive to get a copy of NVDA and install it. I recommend to create a portable copy from your host NVDA on `H:` drive and then in guest OS run that portable copy and install it.
    If you get an error message complaining that file `NVDA_slave.exe` not found - try to copy your NVDA to local guest drive `C:` first. The thing is that because Windows is such an amazing operating system, the `subst` command that we ran earlier only creates a new drive for the user running in normal mode, not in administrator mode, and NVDA installer runs as administrator and so it's unable to see that substituted drive.
### 8. Create developer environment in guest OS
    Follow NVDA's [Create dev environment](https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/createDevEnvironment.md) document. 
    * If you already have an up-to-date git repository cloned in your `H:` drive, no need to clone it again.
    * However other dependencies, such as Python and Visual Studio need to be installed again in guest OS.
### 9. Install some other software you might need
    This step is optional, but you might want to install some software inside guest OS. An easy way to do that is using `choco`:
    1. Install `choco` by following [Choco installation guide](https://chocolatey.org/install) - really it's just a single command to be executed in administrator PowerShell.
    2. Run:
        ```
        choco install /y notepadplusplus  googlechrome
        ```
        or any other software that you need.
### 10. Disable firewall on guest OS
    1. In guest OS go to start menu > firewall. This opens settings window.
    2. In the list view select "Firewall & network protection".
    3. Select Domain network
    4. Under Microsoft Defender Firewall, switch the setting to Off.
    5. Also turn off firewall for Private networks and public networks.
### 11. Assign a static IP address to your guest OS (optional)
    VMWare likes to change IP address of guest OS every day, which is very annoying. If you don't want to be checking your IP daily and updating it in VSCode json file, let's assign a static one.
    1. On your host OS, go to VMWare player > Menu > Manage > Virtual Machine Settings...
    2. Select network adapter and click "Advanced".
    3. Find Mac address of your network adapter. It looks something like:
        ```
        00:0C:29:9E:88:D8
        ```
    4. Open `C:\ProgramData\VMware\vmnetdhcp.conf` in your favorite text editor like notepad. You need to open this as administrator to be able to edit this file. For examplel, you can press `Windows+r`, then type notepad, then press `control+shift+windows+enter` to open an instance of notepad with elevated privileges.
    5. Insert the following block in the end before the last line `# End` and replacing mac address as appropriate:
        ```
        host VMnet8 {
            hardware ethernet  00:0C:29:9E:88:D8;
            fixed-address 192.168.52.10;
        }
        ```
    6. Also make sure that IP address you select lies within subnet mask configured in your file. Subnet mask is defined by this line in the same file:
        ```
        subnet 192.168.52.0 netmask 255.255.255.0 {
        ```

    7. Restart VMware DHCP service. Run the following commands in administrator command prompt or PowerShell:
        ```
        net stop vmnetdhcp
        net start vmnetdhcp
        ```
### 12. Disable guest OS sleep mode
    I find it pretty annoying when guest OS enters standby mode after an hour or so. So to avoid that:
    1. In start menu go to "Power and sleep settings".
    2. In "Put my device to sleep after" select Never.
### 13. Set up debugger config.
    Steps in this section are slightly modified from  [VSCode debugging link](https://code.visualstudio.com/docs/python/debugging), specifically from "Debugging by attaching over a network connection" section.
    2. In guest oS, in `cmd` run the following command:
        ```
        ipconfig
        ```
    3. In its output find IPv4 address of your guest OS. Look for the line that looks something like:
        ```
        IPv4 Address. . . . . . . . . . . : 192.168.52.10
        ```
        In this case my IP address is 192.168.52.10. If you set up static IP address in the previous steps, you should see it here.
    4. Switch back to host OS.
    5. In `cmd` in your host OS run:
        ```
        ping 192.168.52.10
        ```
        You should see ping responses, something like:
        ```
        Reply from 192.168.52.10: bytes=32 time<1ms TTL=128
        ```
        If you see `Request timed out.` instead - then most likely your firewall on the guest OS is still blocking some connections. Or alternatively, your virtual machine might have changed IP address.
    6. Now open your VSCode still on the host OS.
    7. Open command palette (`Control+Shift+P`) and type "open launch.json". Paste the following content there replacing your IP address and local and remote paths as needed:
        ```
        {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python Debugger: Remote Attach",
                    "type": "debugpy",
                    "request": "attach",
                    "connect": {
                        "host": "192.168.52.10",
                        "port": 5678
                    },
                    "pathMappings": [
                        {
                            "localRoot": "H:\\nvda\\",
                            "remoteRoot": "H:\\nvda\\"
                        }
                    ]
                }
            ]
        }
        ```
    8. Open `H:\nvda\requirements.txt` and add the following line in the very end:
        ```
        debugpy
        ```
    8. Open `H:\nvda\source\nvda.pyw`. Find the lines where it calls `core.main()` that look something like this:
        ```
        try:
            import core
            core.main()
        ```
        And insert the following clause right before that `try` statement:
        ```
        if os.path.exists(r'\\vmware-host\Shared Folders'):
            import debugpy
            # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
            debugpy.listen(('0.0.0.0', 5678))
            print("Waiting for debugger attach")
            debugpy.wait_for_client()
            debugpy.breakpoint()
        ```
### 14. Finally, let's debug something!
    1. In guest OS run `runnvda.bat`. Screenreader will try to start up but will wait for the debugger to attach.
    2. Now switch back to host OS and in VSCode press F5. You should hear "debugging started". Then the cursor will be taken to the line immediately after breakpoint in `nvda.pyw`.
    3. Now once you're sure you are connected you can press F5 again to let guest NVDA to start up. You'll hear NVDA startup sound from guest OS.
    4. Have fun! For example, try setting a breakpoint in `def speak` function in `speech\speak.py` and see who's calling it.
### 15. VSCode debugging primer
    If you are not familiar with debugging in VSCode, read some tutorials, for example [this one](https://code.visualstudio.com/docs/editor/debugging).
    As for accessibility, the only thing to be aware of is that current execution line are not being indicated to the screenreader users in any way. So here are some tips for blind debugging from me:
    * For current execution line I haven't found a good way to figure out where it is. You may press `F10` to step over, then you'll figure out what's the next line, but that changes execution state. Other than that I guess you just need to remember at what line your program is currently paused.
    * When your cursor enters a line with a breakpoint, VSCode will play an earcon. Same thing happens when breakpoint is hit during execution.
    * To check value of a variable, press `Control+K control+i`. This only works for local variables.
    * For object fields and for any other arbitrary expressions, you can add them to watch list:
        1. Select desired variable or expression.
        2. In command palette (`control+shift+p`) type "Add to watch"
        3. To view your watch variables, in command palette type "Focus on watch view".
        4. To go back to your editor press  `control+shift+d` since watch view is on debug tab.
        * To avoid typing command names, you can assign keyboard shortcuts - see below.
    * Let's add some useful keyboard shortcuts for ease of debugging:
        1. Go to Menu > File > Preferences > Keyboard shortcuts.
        2. Press `Shift+tab` and press "Open KeyboardShortcuts.JSON"
        3. Paste the following lines:
            ```
            // Place your key bindings in this file to override the defaults
            [
                {
                    "key": "f4",
                    "command": "editor.debug.action.goToNextBreakpoint"
                },
                {
                    "key": "shift+f4",
                    "command": "editor.debug.action.goToPreviousBreakpoint"
                },
                {
                    "key": "ctrl+shift+q",
                    "command": "workbench.debug.action.focusWatchView"
                },
                {
                    "key": "ctrl+shift+a",
                    "command": "workbench.debug.action.focusCallStackView"
                },
                {
                    "key": "ctrl+shift+1",
                    "command": "editor.debug.action.selectionToWatch"
                },
            ]
            ```

## Conclusion
Setting up debugging environment is tedious - I'd expect it'd take 2-3 hours to follow this tutorial. But in the end it is worth it: the ability to step through your code and observe its internal state is priceless. An alternative would be to use `print` or `log` statements and then analyze log files - personally I find this more tedious than one-time setup of a virtual machine.

Hope you find this tutorial useful!