# sreboard 2.1 (showcase)
> *This project is a stripped version of the original project for showcasing in compliance with the ServiceNow NDA.*
```
  ____  ____  _____     _                         _ 
 / ___||  _ \| ____|   | |__   ___   __ _ _ __ __| |
 \___ \| |_) |  _|     | '_ \ / _ \ / _` | '__/ _` |
  ___) |  _ <| |___   _| |_) | (_) | (_| | | | (_| |
 |____/|_| \_\_____| (_)_.__/ \___/ \__,_|_|  \__,_|
                                                    
```

sreboard: An automation for monitoring applications setup at ServiceNow SRE team


## Index

* [What does this do?](#what-does-this-do)
* [How to install?](#how-to-install)
* [How it works?](#how-it-works)
* [What are the options?](#what-are-the-options)




## What does this do?

* Decrypts VPN tokens for the respective hosts and authenticates to any of the active domains. Retries and reconnects or 
auto-switches between the most active domains if the current one becomes unresponsive. 
* Operating system level management for the applications that it controls.
* Opens specified browsers in kiosk modes and manages application window locations by host screen resolutions. 
* Command-line argument inputs to specify the optional functions.



## How to install?
* Clone the repository into the monitor Mac of your choice.
* To run it with the host default configuration run the <b>app.py</b> script as below:

```python
python sreboard.py
```
 Note: Your Mac may not be in the default configuration Mac list. See [available options](#what-are-the-options)



## How it works?
* The project structure has the following files:

```python
sreboard.py
factors.py
data.py
cord_attr.json
```

The automation leaverages the use of OSA Scripting, Mac OSX's internal system scripting to perform the actions like 
coordinating and window resizing.


The following files decribe the project's core structure:
* <b>app.py</b> contains the main function to the project and can be compared to the VIEW component.
* <b>factors.py</b> contains the control structure of the project and is compared to the CONTROLLER component.
* <b>data.py</b> contains all the related variables in the module which is obviously the MODEL component.
* <b>app.conf</b> file is updated everytime the script is triggered, it stores a volatile variable.
* <b>cord_attr.json</b> stores variables of the opened window sizes and coordinates in JSON format for the ease of setup.



## What are the options?

* optional arguments:

<pre>
  -h, --help     Shows this help message and exit
  -d, --default  Activates default host application configurations
  -s, --switch   Switchs to alternate monitor configurations
  -q, --quit     Quits ALL running Chrome AND/OR Adium processes only
</pre>


<pre>
<b>Email for issues/enhancements to:</b>
Salman:  salmansre21@gmail.com
         salman.rahman@servicenow.com
         
Ciprian: ciprian.iftode@servicenow.com
</pre>