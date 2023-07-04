# README

Web used by our Radio Recommendation system.

## How to start the web

Given the huge variety of operating systems at our disposal in this day and age, trying to explain how to deploy this web to each and every one of them would be out of the scope of this work. Nevertheless, we can take advantage of tools to avoid that. In this particular case, we provide you with the means to automatically create a Linux box in your system via [Vagrant][vagrant], using [Ansible][ansible] for the deployment of both the prerequisites and the software. You can find Vagrant and Ansible scripts in the folder **vagrant** of this very repository.

Once you have cloned this repository in your system, open a terminal in the repository folder **vagrant** and run:

```bash
vagrant up
```

When the deployment process ends you will be able to access the web at [localhost:8080][web]. Please notice that if you have any other server listening in the same port, CompareML will not be able to start.

Use this command to log into the virtual machine:

```bash
vagrant ssh
```

In case you want to deploy the web to your own machine, just take a look at the file **playbook.yml**. Although it contains all the steps needed in order to do so, it boils down to something like this:

```bash
sudo apt update
sudo apt install python3-pip
pip install cherrypy
git clone https://github.com/i3uex/RadioRecsWeb.git
```

For your reference, a more accurate description of the process is the file **playbook.yml**, inside the folder **vagrant**.

One these steps are completed, use the scripts provided to control the server.

From the terminal, use the script `start.sh` to launch the server:

```bash
sh start.sh
```

The script will execute `python 3 main.py &`. Besides, it saves the PID of the launched process in the file **pid.txt**, so it's easier to stop the server when needed.

To stop the server, use the script `stop.sh` from the terminal:

```bash
sh stop.sh
```

It will read the PID stored in the file **pid.txt** and the kill said process.

You can also restart the server this way:

```bash
sh restart.sh
```

This script just calls `start.sh` and then `stop.sh`.

[vagrant]: https://www.vagrantup.com "Development Environments Made Easy"
[ansible]: https://www.ansible.com "Automation for everyone"
[web]: http://localhost:8080 "Web at localhost"
