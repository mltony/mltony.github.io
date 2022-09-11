# Working with Linux using NVDA
This post contains many tips and tricks that I found to be useful that boost my productivity when working with remote Linux servers.
This post is not a tutorial for beginners on how to use Linux; it requires some knowledge of Linux basics. If you are new to Linux, please find a Linux tutorial  for beginners.

## Scenarios

We will look at two possible scenarios of working with Linux environment:
* WSL or WSL2 are solutions developed by Microsoft that allow you to run virtual Linux environment on your Windows computer. They are really good if you want to learn Linux or when you need to use some Linux commands on Windows.
* Connecting to a remote Linux server via SSH. This would allow you to work with real Linux servers and typically this would be required in most industrial jobs these days.

## Prompt verbosity

Default Linux prompts tend to be overly verbose, they often include current path or host name. This can be easily dropped by editing `bash` configuration.

Go to your home directory and open either `~/.bash_profile` or `~/.bashrc` file (some systems tend to use one and not the other, but most configuration can be done on whichever file is present on your system). Go to the end of the file and add the following line:
```
export PS1="LINUX$ "
```

Or feel free to set the prompt to even shorter word; however please keep in mind, that NVDA doesn't react when too few characters update on the screen, so please make sure that your prompt contains at least 3 non-whitespace characters, otherwise NVDA might not always announce prompt.

If you work with multiple Linux servers, it is a good idea to set distinct prompts on each of them. 

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

This way you don't [need to press extra keystrokes - your output will automatically appear in Notepad++.

### Solution 1: for short output clear your window before each command

When you know that command you're going to execute will not produce much output and all output would fit on the screen, which is by default around 25 lines, you don't have to use any extra tricks. However, it would be really convenient to be able to jump to the beginning of output. One trick is to clear your terminal window right before executing command, for example, to list all files in current directory, you can type:
```
$ clear; ls
```

Then you can press `NumPad7` key to jump to the first line of output.

You can also configure your bash to clear the window automatically before each executed command; in order to do so, add the following line to your bash config file:
```
bind '"\C-m": "\C-l\C-j"'
```

This line configures a custom binding for `Enter` keystroke: it first sends `Control+L` command to bash, which clears the window, and then it sends `Control+J`, which acts as the actual `Enter` keystroke. Here is an even more advanced version of this binding that you can consider using:
```
bind '"\C-m": "\C-l \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h \C-h\C-j"'
```
This advanced binding also sends 128 whitespace keystrokes and then deletes all of them by sending corresponding number of `Backspace` keystrokes. This will cause a slight delay after screen has been cleared, so that NVDA would notice that the screen became blank before output appears. This can be useful when you execute the same command twice in a row, and if you don't have this pause, the second time NVDA doesn't notice any change in screen content so it wouldn't speak anything.

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

https://github.com/mltony/mltony.github.io/blob/gh-pages/PATH_TO_FILE?raw=true


### Skipping timestamps

If you are working with Linux backend software, chances are you might have to read server logs, where each line starts with a timestamp. 
It is very inconvenient to listen to those timestamps, so it is probably a good idea to filter them out from NVDA speech.

You can do that via [Phonetic Punctuation](https://github.com/mltony/nvda-phonetic-punctuation/) NVDA add-on.
Just configure an audio-rule with regular expression capturing your timestamp and you can replace timestamps with a quick earcon sound.

## Accessing and editing remote files 

### Linux editors
### VSCode
### Notepad++ 
### sshfs-win and rclone
### sshfs under WSL2

## Other tricks
### Clipboard pasting
### Editing command line
### tmux