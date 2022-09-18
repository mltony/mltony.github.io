# Working with Linux using NVDA
This post contains many tips and tricks that I found to be useful that boost my productivity when working with remote Linux servers.
This post is not a tutorial for beginners on how to use Linux; it requires some knowledge of Linux basics. If you are new to Linux, please find a Linux tutorial  for beginners.

## Scenarios

We will look at two possible scenarios of working with Linux environment:
* WSL or WSL2 are solutions developed by Microsoft that allow you to run virtual Linux environment on your Windows computer. They are really good if you want to learn Linux or when you need to use some Linux commands on Windows.
* Connecting to a remote Linux server via SSH. This would allow you to work with real Linux servers and typically this would be required in most industrial jobs these days.

## Terminal/Console programs

There are a few options

* Command prompt (cmd.exe) - well-known and bulletproof program that tends to work best. If you are having troubles using any other programs, try good old command prompt.
* PuTTY - only for SSH connections; accessibility is good.
* Windows Terminal - recently Microsoft added this revamped terminal that supports tabs. As of the date of writing this post NVDA mostly supports it.
* SecureCRT is a paid SSH and terminal program. Screenreader users have reported using it successfully, so mentioning it in this list for what it's worth.

## Linux text editors

Linux comes with a wide variety of terminal-based editors; however their accessibility is not always good enough. Typical problems that seem to plague all of them are:
* Cursor lag - that is when screenreader announces one line while your cursor is on the next line. This problem gets only more egregious on slower network connections.
* Inconsistent word navigation: `Control+LeftArrow` and `Control+RIghtArrow` commands use different definition of word in different programs, so that confuses NVDA and either you might hear NVDA repeating the same word twice, or skipping a word.
* No indentation information - add-ons like [IndentNav]()(https://github.com/mltony/nvda-indent-nav/) don't work there.
* Screenreaders don't automatically announce editor notifications and this might be confusing for screenreader users.

Therefore I strongly suggest to figure out a way to edit files using any editor running natively on Windows instead of trying to fix Linux editors. However, for quick one-line edits on Linux server it is still beneficial to be familiar with one of Linux editors. Here are some of your options:

* nano - it is good for beginners as it is very simple. Only a few keyboard shortcuts to learn.
* emacs is a more advanced editor. It is  known for a very weird set of keyboard shortcuts - that is you would need to learn all shortcuts from scratch. But if you decide to learn it, it offers  a good jump start into [EmacsSpeak](https://github.com/tvraman/emacspeak/) - a very interesting emacs-based screenreader solution, that doesn't depend on NVDA.
* vim - another popular text editor.

## Prompt verbosity

Default Linux prompts tend to be overly verbose, they often include current path or host name. This can be easily dropped by editing `bash` configuration.

Go to your home directory and open either `~/.bash_profile` or `~/.bashrc` file (some systems tend to use one and not the other, but most configuration can be done on whichever file is present on your system). Go to the end of the file and add the following line:
```
export PS1="LINUX$ "
```

Or feel free to set the prompt to even shorter word; however please keep in mind, that NVDA doesn't react when too few characters update on the screen, so please make sure that your prompt contains at least 3 non-whitespace characters, otherwise NVDA might not always announce prompt.

If you work with multiple Linux servers, it is a good idea to set distinct prompts on each of them.

Whenever you need to figure out current directory or hostname, you can always type commands `pwd` and `hostname` to do so.

## Capturing and reviewing command output

This is one of the major painpoints for screenreader users as SSH terminal was not designed with accessibility in mind. However the good news is that there are many solutions that can simplify your experience reading commands output.

### WSL solutions

When using WSL or WSL2 you can typically just redirect command output to `clip.exe` to capture it in Windows clipboard. You can run:
```
$ my_command | clip.exe
```
and then paste to your favorite text editor, such as Notepad++.

If you would like to capture both `StdOut` and `StdErr`, then run:
```
$ my_command |& clip.exe
```

Alternatively, if you know some of Bash scripting, you can write a short script that you would redirect your output to; and the script would:
* save all the output to a temporary file on Windows disk.
* Open that file in your favorite editor. Hint: in WSL you can call Windows programs directly from Bash scripts as long as you specify full path to their executables.

This way you don't need to press extra keystrokes - your output will automatically appear in Notepad++.

### Solution 1: for short output clear your window before each command

When you know that command you're going to execute will not produce much output and all output would fit on the screen, which is by default around 25 lines, you don't have to use any extra tricks. However, it would be really convenient to be able to jump to the beginning of output. One trick is to clear your terminal window right before executing command, for example, to list all files in current directory, you can type:
```
$ clear; ls
```

Then you can press `Shift+NumPad7` key to jump to the first line of output. From there you can use NVDA review cursor to read output either by line, by word or by character.

Note that in Windows Terminal `Shift+NumPad7` command would take you all the way to the beginning of text buffer instead of the first visible line; as of this post writing date I am not aware of any workaround, but check with NVDA community.

If you wish to copy output to clipboard, you can use NVDA built-in keystrokes `NVDA+F9` and `NVDA+F10`. Another  convenient way of copying files is provided by [Review Cursor Copier](https://addons.nvda-project.org/addons/reviewCursorCopier.en.html) NVDA add-on.

You can also configure your bash to clear the window automatically before each executed command; in order to do so, add the following line to your bash config file:
```
bind '"\C-m": "\C-l\C-j"'
```

This line configures a custom binding for `Enter` keystroke: it first sends `Control+L` command to bash, which clears the window, and then it sends `Control+J`, which acts as the actual `Enter` keystroke. Here is an even more advanced version of this binding that you can consider using:
```
bind '"\C-m": "\C-l \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h\C-j"'
```
This advanced binding also sends 128 whitespace keystrokes and then deletes all of them by sending corresponding number of `Backspace` keystrokes. This will cause a slight delay after screen has been cleared, so that NVDA would notice that the screen became blank before output appears. This can be useful when you execute the same command twice in a row, and if you don't have this pause, the second time NVDA doesn't notice any change in screen content so it wouldn't speak anything.

Also, remember to always maximize your window to increase the number of visible lines on the screen.

### Solution 2: for medium-size output

If you know that your command produces output that is only several pages long, you can consider using screen capture feature of my [Console toolkit](https://github.com/mltony/nvda-console-toolkit) NVDA add-on.
After downloading and installing Console Toolkit, try executing your command by pressing `Control+Enter`; this will make the add-on to capture screen output by piping it into `less` command; it will then display a fully accessible window that contains all captured output.
This add-on requires `less` command to be installed on your Linux computer - which is typically the case unless you are not using mainstream Linux distribution.
Since it is using less command, the process of capturing output is somewhat slow, that's why it can realistically capture a few pages of output.

Please read add-on documentation for troubleshooting.

### Solution 3: for long output

If you need to read very long outputs, this would be the best solution, but it requires the most configuration. If you are not afraid of scripting, keep reading! :)

Basically, we will write two scripts:
1. On Linux server we will write `l`-script. It would capture all output that is piped into it and then it would save this output to a file in a predefined directory that we'll call transfer directory.
2.Watchdog script running on Windows would connect to Linux server via SFTP protocol and it would check transfer directory. Once any file appears there, it would automatically download it, delete it from the server and open locally downloaded copy in Notepad++.

#### l-script

Download this [sample l-script](https://raw.githubusercontent.com/mltony/mltony.github.io/main/files/l)
and save it to any directory where `$PATH` can find it. For example, I like to create `scripts` in my home directory and I adjust `$PATH` environment variable in my bash config files like this:
```
export PATH=$PATH:$HOME/scripts
```

Edit your l-script in any text editor and make sure that on line 5 `mv` command moves into transfer directory that exists on your computer.

Now, let's make sure that `l`-script can indeed be found in your path by executing:
```
$ l
```
If it says `command not found` - then it's not in your path - please check `$PATH` environment variable again, or maybe restart bash if you haven't done soe already. If everything works, the script would echo every line you type, and after you're all done (press `Control+D`) it would save the file with random name in transfer directory ready to be picked up by the watchdog.

#### Watchdog

Download [watchdog](https://raw.githubusercontent.com/mltony/mltony.github.io/main/files/watchdog.py) and save it on your Windows computer.

Open `watchdog.py` in any editor and update the following variables in the beginning of the file to point to your server:
* `SFTP_HOSTNAME`
* `SFTP_USER`
* `SFTP_PASSWORD_FILE` or `SFTP_PASSWORD`. Please note that it is not safe to store plain text password, so do it at your own risk. If security is important, please look into SSH public key authentication - it is not covered in this post.
* `SFTP_DIR` - please make sure this points to exactly the same transfer directory you specified in your l-script in previous section.

Now it is time to run the watchdog! On your Windows computer, execute:
```
$ python watchdog.py
```

If you see the following exception:
```
paramiko.ssh_exception.SSHException: No hostkey for host {hostname} found.
```
This would mean that you have never connected to given SSH host before and SSH doesn't know whether to trust it or not. In this case, connect to the same SSH host using Windows SSH by typing:
```
$ ssh username@hostname
```
You would see  a warning message similar to this one:
```
The authenticity of host '{hostname} ({IP address})' can't be established.
ECDSA key fingerprint is SHA256:......
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
Type `y` and from now on your SSH client has memorized fingerprint of your Linux server, so try running watchdog again, the error must disappear by now.

#### bash shortcut

You can assign a keyboard shortcut in your bash configuration to execute current command with input redirection to l-script. Add this line to your bash config file:
```
bind '"\e[24~": "\e[4~ |&l \n"'
```

This defines binding for F12 key, and once you press it, bash will seimulate the following keystrokes:
* Press `End` key,
* Press spacebar,
* Type `|&l`
* and finally, press `Enter` to actually execute command.

With this configuration you can type a command and then run it with `F12` instead of `Enter` to send its output to your local Notepad++.

### Ignoring timestamps

If you are working with Linux backend software, chances are you might have to read server logs, where each line starts with a timestamp.
It is very inconvenient to listen to those timestamps, so it is probably a good idea to filter them out from NVDA speech.

You can do that via [Phonetic Punctuation](https://github.com/mltony/nvda-phonetic-punctuation/) NVDA add-on.
Just configure an audio-rule with regular expression capturing your timestamp and you can replace timestamps with a quick earcon sound.

## Accessing and editing remote files

When working with a large project, chances are you would want your source code to reside on Linux server so that you can build and run it. This poses a question: how to edit files that are located on a Linux server? There are many options to choose from, each of them having their own pros and cons.

### Linux text editors

A few popular Linux editors are mentioned above in this note. Any of them can run inside your SSH session. However, using them with a screenreader seems to be inconvenient at best, so I wouldn't recommend to use them except for quick 1 line edits.

### VSCode

Microsoft Visual Studio Code (VSCode) has already become de facto standard of IDE for all kinds of software development. And the good news is that it works great with all major screenreaders. It also supports remote development over SSH, which makes it the best option for developing on Linux servers.

You can read more about VSCode [accessibility](https://code.visualstudio.com/docs/editor/accessibility) and [remote development over SSH](https://code.visualstudio.com/docs/remote/ssh).

As of the date of writing this post, all the steps required to set up VSCode to work with a remote Linux server are fully accessible with NVDA. If you are stuck in any step, feel free to ask at [program-l mailing list](program-l@freelists.org).

### WinSCP and other SFTP clients

There are a bunch of SFTP clients for Windows, such as:
* [WinSCP](https://winscp.net/),
* (FileZilla)[https://filezilla-project.org/],
* [CyberDuck](https://cyberduck.io/).

As of the date of writing this post, WinSCP is fully accessible; I cannot comment on accessibility of other clients.

In general the advantage of SFTP clients is that they tend to work very reliably and they are easy to set up. The downside is that you would be stuck in a cycle of download file, edit file, upload it back, which gets very tedious and confusing if you have more than just a single file to edit.

### Mounting SSHFS on Windows: SSHFS-win , rClone, SFTP Drive

[SSHFS](https://github.com/libfuse/sshfs) is a popular Linux tool that allows you to mount file system of a remote machine locally. It doesn't work on Windows, however, there are a few good alternatives for Windows:

* [SSHFS-win](https://github.com/winfsp/sshfs-win) is a Windows port of SSHFS and it is fully accessible -since it can be fully configured from command line. I recommend to start with it since it tends to work well for me. Excellent documentation on its github page. Its main downside is limited options for SSH authentication: it only supports password authentication and key-based authentication without passphrase.

* [RClone](https://rclone.org/) positions itself as file synchronization tool, however among other features it can also mount remote SFTP drives. For more information, check out its [mount command](https://rclone.org/commands/rclone_mount/). It is also fully accessible and can be configured straight from command line. It appears that it can integrate with Windows SSH agent for passpharse key authentication, however, I can't speak about accessibility of that solution. Downside: RClone appears to be pretty slow compared to other SSHFS solutions.

* [SFTP Drive](https://www.nsoftware.com/sftp/drive/) is a commercial tool for mounting remote SSH file systems; but it is free for personal use. User interface is mostly accessible, never mind a few minor glitches.

### Proper sshfs under WSL2

Now if none of SSHFS solutions mentioned in the previous section work for you and you are not afraid configuring Linux services, you can try to set up proper SSHFS that is running inside WSL2 container. Please note that this will only work in WSL2 and not in WSL1, since WSL1 is not emulating the entire Linux kernel. Alternatively, you can run virtual Linux in any other virtualization software, such as VMWare Player or VirtualBox, however WSL2 offers a straightforward bash command line and therefore is the most convenient option.

Please follow [these instructions](https://tanat44.github.io/post/2021-09-13-wsl2-sshfs.html) to enable SSHFS and access it from Windows.

### Configuring Samba/SMB server

This option is again only for those who are not afraid of configuring Linux servers.
SMB is a network file protocol used for Windows file sharing - that is when you type address like `\\host_name\share_name\file.txt` - under the hood you are requesting a file over SMB.
Samba is an open-source implementation of SMB server and client.

Here is a good [samba tutorial for Debian/Ubuntu](https://ubuntu.com/tutorials/install-and-configure-samba) - or you can find another tutorial for your favorite  flavor of Linux.

Please note that SMB typically runs over port 445 and you would need to make sure that access to this port is not blocked in whatever datacenter your Linux server is located. Often times it is blocked due to security reasons. If this is the case, please check out a section below on how to work around this by setting up SSH tonnels.

### Notepad++

Notepad++ has [NppFTP plugin](https://ashkulz.github.io/NppFTP/) that supports many protocols, including SFTP. So in theory it should allow editing files directly on remote Linux server. However, I found its configuration window to be not accessible with NVDA, so sighted help will be required to configure it.

### File synchronization tools: rsync, syncthing, Dropbox and others

I don't recommend this approach, since any changes to local copy will propagate to the server with some delay.
In practice this often creates confusion, e.g. when you build a binary but the most recent changes have not yet propagated to the server by the time build was started.
But if all other fails, this might still be the best option available.

The main idea is that we will keep two copies of your source code repository: one on Linux server and the other one locally on your Windows computer. Then we make sure that both copies are identical using one of these tools:

* rsync - is a well-known Unix file synchronization tool. You would need to install rsync client on your Windows computer (either from cygwin or from WSL) and have it synchronize with Linux server using either SFTP protocol, or preferrably via rsync protocol; the latter option would require you to set up rsync server on Linux server, but then it would run much faster. You can also consider writing a script that would kcik off synchronization on rsync client side in an infinite loop.

* Dropbox, Google Drive, an many other competitors offer file synchronization services. You would need to install their clients on both Windows and Linux sides and they would automatically sync contents of their folders with the cloud and with each other.

* [Syncthing](https://syncthing.net/) is another open-source file sync solution that uses peer-to-peer protocol to synchronized files.

## Other useful tricks

### Clipboard pasting

It happens that the standard `Control+V` command doesn't work with SSH. Command prompt offers "Paste" command in its context menu, but it is hard to navigate to.

As a workaround I implemented `Control+V` feature in my Console toolkit add-on for NVDA. Simply install the add-on, and `Control+V` would work for pasting in both Command Prompt and PuTTY.

### Editing command line

Editing commands right inside bash prompt in SSH can be tedious, because navigation by word does not work the way NVDA expects and as a result NVDA would often announce the same word multiple times when pressing `Control+LeftArrow/RightArrow`.

In order to work around this, I came up with an accessible command editor feature in my Console Toolkit add-on.
Just press `NVDA+E` to open current command in a fully accessible window.
After editing you can either press `Escape` to update it in SSH window, or alternatively, press `Enter` to execute it right away.

### tmux

In addition to all tricks mentioned above, it would probably be a good idea to learn using tmux within SSH session. Tmux stands for terminal multiplexer, and its two key features are:
* Persistence: your bash session or sessions will survive even after you disconnect.
* Multiplexing: you can have 10 or even more sessions within a single SSH connection and you can switch between them using `Control+B`, followed by 0-9 digit.

If you are new to tmux, you can read any tutorial, like for example [this one](https://leimao.github.io/blog/Tmux-Tutorial/).

Let me describe my tmux configuration that makes tmux more screenreader-friendly.

on the very bottom of tmux screen there is status line, that displays things like window name and clock. 
I find status line useless and given the fact that NVDA often catches seconds ticking in the status line - even annoying.
So it's a good idea to turn it off completely, by running:
```
$ tmux status off
```
Or, alternatively, you can add the following line to your `~/.tmux.conf` file:
```
set -g status off
```

But without status it would be hard to figure out the index of current window.
To address this we can change bash prompt to include window number.
Add these lines to your bash configuration:
```
export TMUX_WINDOW=$(tmux display-message -p '#I')
export PS1="tmux${TMUX_WINDOW}) "
```

Another useful key binding is clearing screen. 
In bash you can clear screen by presssing `Control+L`, however it won't work when you are inside an interactive program, such as Python interpreter.
So you can set key binding in tmux to still clear screen on `Control+L`; add the following line to your `.tmux.conf` file:
```
bind -n C-l send-keys -R \; send-keys C-l \; clear-history
```


Note: There is one downside of using tmux compared to simple SSH session. 
When your command produces more than one screen of output, the first lines of output disappear from console completely, and even if you can access off-screen lines via your review cursor you won't find them there.
This is just the way tmux works.
You can still access first lines in tmux buffer by pressing `Control+B PageUp`, which is less convenient than review cursor.
However, given all possible ways to capture command output that I listed in this note above, the advantages of tmux sure enough outweigh this downside.

### Appendix: SSH for dummies