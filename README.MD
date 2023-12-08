# Project Setup

In the following section, we will describe how the project can be set
up. We will explain each step in detail, so it can be followed manually.
An even easier way is to use the provided shell scripts that automate
the installation process.

## Overview

This is a high-level overview of the steps to set up the project.

1.  Set up Mininet VM.

2.  Prepare Mininet VM: Install required tools such as JDK, Maven, and
    Docker.

3.  Set up ONOS controller.

## Mininet-VM

This guide uses VirtualBox (`https://www.virtualbox.org/`) to run the
Mininet VM. Any other virtualizer is also suitable such as QEMU
(`https://www.qemu.org/`) or KVM
(`https://linux-kvm.org/page/Main_Page`). Please chose any of these and
install it onto your machine.\
Download the Mininet VM from GitHub at
`https://github.com/mininet/mininet/releases/`. This documentation uses
the Ubuntu 20.04.1 VM image (approximately 1 GB in size).\
Extract the downloaded ZIP file, open VirtualBox (or any other
virtualizer), and import the OVF (Open Virtualization Format) file.\
Enable bridged adapter in VM settings for network connectivity as shown
in the picture.

<figure>
<img src="Project setup/Bridged Adapter.png" style="width:50.0%" />
<figcaption>Bridged Adapter Configuration</figcaption>
</figure>

<figure>
<img src="Project setup/Mininet-VM.png" style="width:50.0%" />
<figcaption>Mininet VM Running</figcaption>
</figure>

## ONOS Installation

Once the VM is set up, we can install Docker which is used to run the
ONOS controller.

    # Install Docker package
    sudo apt-get -y install docker.io

    # Create a symbolic link for Docker CLI
    sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker

    # Download ONOS Docker image
    sudo docker pull onosproject/onos

    # Run ONOS instance
    sudo docker run -t -d -p 8181:8181 -p 8101:8101 -p 5005:5005 -p 830:830
    --name onos onosproject/onos

    # Check if the container is running
    sudo docker ps

<figure>
<img src="Project setup/onos running.png" style="width:50.0%" />
<figcaption>ONOS Running in Docker Container</figcaption>
</figure>

In order to access the ONOS GUI, we need to find out the IPv4 address of
our Mininet VM which is in our case 10.221.84.210.

    # Check Mininet VM IP
    ip addr | grep eth0

<figure>
<img src="Project setup/Mininet-VM IP.png" style="width:50.0%" />
<figcaption>Mininet-VM IP Address</figcaption>
</figure>

To access the ONOS GUI at `http://10.221.84.210:8181/onos/ui` we can use
the username `karaf` and password `karaf`.

<figure>
<img src="Project setup/GUI login.png" style="width:50.0%" />
<figcaption>ONOS GUI Login</figcaption>
</figure>

To access the ONOS CLI via SSH from your host, we first need to know the
docker container IP in which ONOS is running. First, we SSH into the
Mininet VM using username `mininet` and password `mininet`. Then we
inspect the docker container. Do not forget to change the values to
yours.

    # SSH into Mininet VM
    ssh mininet@10.221.84.210

    # Find the IP address of the Docker container
    sudo docker ps
    sudo docker inspect e453e6bf42a7 | grep "IPAddress"

<figure>
<img src="Project setup/ssh to mininet.png" style="width:50.0%" />
<figcaption>SSH to Mininet-VM</figcaption>
</figure>

<figure>
<img src="Project setup/get docker ip.png" style="width:50.0%" />
<figcaption>Get Docker Container IP</figcaption>
</figure>

Then we can SSH into the ONOS CLI using again the username `karaf` and
password `karaf`.

    # SSH to ONOS instance within the Docker container
    ssh -p 8101 karaf@172.17.0.2

Now we need to activate some applications, so ONOS can communicate with
Mininet via Openflow and the hosts can communicate with each other.

    # Activate forwarding and OpenFlow application
    app activate org.onosproject.openflow
    app activate org.onosproject.fwd

<figure>
<p><img src="Project setup/Activate openflow.png" style="width:50.0%"
alt="image" /> <img src="Project setup/Active forward.png"
style="width:50.0%" alt="image" /></p>
<figcaption>Activate OpenFlow and Forwarding</figcaption>
</figure>

In a new terminal, run the following commands to spin up a topology:

    # Create Mininet topology with ONOS controller
    sudo mn --topo tree,2,2 --mac --switch ovs,protocols=OpenFlow14 
    --controller remote,ip=172.17.0.2

    # Test if hosts can reach each other
    pingall

<figure>
<img src="Project setup/MininetTopo.png" style="width:50.0%" />
<figcaption>Mininet Topology</figcaption>
</figure>

Check the ONOS GUI to see the topology.

<figure>
<img src="Project setup/Onos GUI topo.png" style="width:50.0%" />
<figcaption>ONOS GUI Topology</figcaption>
</figure>

# Performance

In this section we want to do a brief performance analysis of the ONOS
controller. We want to measure the throughput and delay based on the
number of hosts.

# Building ONOS Application

Now we want to explain how to build ONOS applications like the ones we
already saw such as OpenFlow or active forwarding. The next section can
either be done in a new VM or your Host machine. We provide you with a
VM image (OVF) that already has everything installed which can be found
here: but you can also follow along by installing a new Ubuntu VM. The
high-level overview of the steps are as follows:

1.  Install Ubuntu as a VM in VirtualBox

2.  Install Maven and JDK on this new VM

3.  Install ONOS-admin tools

4.  Generate a new base ONOS application project

## Install Ubuntu VM to Virtualbox

You can skip the following section if you want to use the provided VM
image.

Take into account that you approxcamtily need 20 GB of free disk space.
Download the Ubuntu iso from the official website
`https://ubuntu.com/download/desktop`. We will use the newest version of
Ubuntu 22.04.3 LTS. LTS stands for long-term-support. The Ubunutu iso
has a size of around 4.7 GB.

Create a new VM in VirtualBox.

<figure>
<img src="Ubuntu VM install/Create VM.png" style="width:50.0%" />
<figcaption>Create a new VM in VirtualBox.</figcaption>
</figure>

Follow the installtion guide until you need to select the hard disk file
type, then click on expert mode.

<figure>
<img src="Ubuntu VM install/expert mode.png" style="width:50.0%" />
<figcaption>Select expert mode during VM creation.</figcaption>
</figure>

Change the size of the VDI to 20GB as Ubuntu requires at least 15 GB.

<figure>
<img src="Ubuntu VM install/vm disk size.png" style="width:50.0%" />
<figcaption>Change the size of the VDI to 20GB.</figcaption>
</figure>

Follow the steps of the VM creation process until the end. You can
safely allocate all CPU cores as they are shared in contrast to RAM. It
should look like this now.

<figure>
<img src="Ubuntu VM install/final overview.png" style="width:50.0%" />
<figcaption>Final overview of VM settings.</figcaption>
</figure>

Now we need to create a NAT network so that the two VMs (our Mininet VM
and this Ubuntu VM) can communicate with each other. Click on File,
Preferences, and then select Network.

<figure>
<img src="Ubuntu VM install/virtualbox create natnetwork.png"
style="width:50.0%" />
<figcaption>Create a new NAT network in VirtualBox.</figcaption>
</figure>

Add a new NAT network, give it a name and select the CIDR block scope as
follows.

<figure>
<img src="Ubuntu VM install/nat scope.png" style="width:50.0%" />
<figcaption>Select CIDR block scope for NAT network.</figcaption>
</figure>

Under settings for each of the VMs, select Network and add a new network
adapter. Select NAT network and choose the newly created NAT network. In
our case SDNNetwork.

<figure>
<img src="Ubuntu VM install/ubuntu natnetwork.png"
style="width:50.0%" />
<figcaption>Select NAT network for VMs.</figcaption>
</figure>

Add also a bridged network adapter to the Ubuntu VM, so it can
communicate with the host.

<figure>
<img src="Ubuntu VM install/network select bridged.png"
style="width:50.0%" />
<figcaption>Add a bridged network adapter.</figcaption>
</figure>

Now we are nearly ready to actually install Ubuntu; just select the ISO
as our storage controller, under Storage.

<figure>
<img src="Ubuntu VM install/select iso as storage .png"
style="width:50.0%" />
<figcaption>Select ISO as storage controller.</figcaption>
</figure>

Start the VM, Install Ubuntu and follow the installation guide. Select
minimal for faster setup as we do not need most of the software that
comes with Ubuntu.

<figure>
<img src="Ubuntu VM install/ubuntu installation.png"
style="width:50.0%" />
<figcaption>Start the VM and install Ubuntu.</figcaption>
</figure>

Due to the NAT network the IP address of the MininetVM changed and is
now reachable from within the Ubuntu VM. Get the new IP address of the
Mininet VM and Ubuntu VM.

    ifconfig

<figure>
<img src="App/new mininet ip.png" style="width:50.0%" />
<figcaption>New MininetVM IP</figcaption>
</figure>

We can try to ping from the Mininet VM to Ubuntu VM and vice versa. On
Ubuntu VM install net-tools to use ping.

    #install net-tools
    sudo apt-get install net-tools

<figure>
<img src="App/ping test 1.png" style="width:50.0%" />
<figcaption>Ping test 1</figcaption>
</figure>

<figure>
<img src="App/ping test 2.png" style="width:50.0%" />
<figcaption>Ping test 2</figcaption>
</figure>

We can also now check if we can still reach the GUI from within our new
Ubuntu VM, we just need to update the IP address to the new one.

<figure>
<img src="App/new ui test in ubunutu vm.png" style="width:50.0%" />
<figcaption>ONOS UI</figcaption>
</figure>

## Prepare VM

Now we need to install some requirements such as OpenJDK and Maven to
build ONOS applications. For easier use, we provide a bash script that
automates the installation process.

(Optional)

    sudo apt-get install git
    git clone https://github.com/selfoluap/ONOS-SDN
    sudo bash ONOS-SDN/install-requirements.sh

If you want to do the steps manually, follow along.

First we need to install OpenJDK 11 and Maven

    sudo apt-get install openjdk-11-jdk
    sudo apt install maven

<figure>
<img src="App/maven installed.png" style="width:50.0%" />
<figcaption>Maven and OpenJDK installed</figcaption>
</figure>

The we need to install curl to retrieve the onos-admin tools from the
maven repo.

    sudo apt-get install curl
    curl -sS --fail 
    https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.7.0/onos-admin-2.7.0.tar.gz \
      > tools.tar.gz
    tar xf tools.tar.gz
    mv onos-admin-2.7.0 tools

You sould see now be able to the tools like this.

<figure>
<img src="App/onos-admin tools installed.png" style="width:50.0%" />
<figcaption>ONOS tools</figcaption>
</figure>

## Create ONOS application

Now, we are finally ready to bootstrap an ONOS application. First we
need to select the ONOS version that we want to use for our project.
Open up a terminal in the Ubuntu VM and follow along.

First we need to specify the ONOS version we want our application to
use.

    export ONOS\_POM\_VERSION=2.7.0

Then we can use the onos-admin tools to generate a skeletal ONOS
application project. Confirm by typing \"y\".

    tools/onos-create-app app org.skku skku-app 1.0-SNAPSHOT org.skku.app

<figure>
<img src="onos-app/say yes.png" style="width:50.0%" />
<figcaption>Confirm Create ONOS Project</figcaption>
</figure>

<figure>
<img src="onos-app/project created.png" style="width:50.0%" />
<figcaption>ONOS Project Created</figcaption>
</figure>

This has now generated a new project. However, the properties are not
correct yet. This is because the maven install command builds against
the pom.xml file. As we can see in the figure below, the properties are
not set correctly, which we will do.

<figure>
<img src="onos-app/pom.xml before.png" style="width:50.0%" />
<figcaption>pom.xml before</figcaption>
</figure>

<figure>
<img src="onos-app/pom.xml after.png" style="width:50.0%" />
<figcaption>pom.xml after</figcaption>
</figure>

To construct the ONOS app, navigate to the main directory of the created
project and utilize Maven by executing the following commands.

    cd skku-app
    mvn clean install

<figure>
<img src="onos-app/project built.png" style="width:50.0%" />
<figcaption>ONOS Project Built</figcaption>
</figure>

Once the build process concludes, both the OSGi bundle and the
application archive will be installed in your local Maven repository.
This will also create an OAR file, which can be installed onto our ONOS
controller. To do so, execute the following command. Replace the IP
address of your Mininet VM. The '!' automatically activates the
application.

    tools/onos-app 192.168.2.9 install! ~/skku-app/target/skku-app-1.0-SNAPSHOT.oar

<figure>
<img src="onos-app/project installed.png" style="width:50.0%" />
<figcaption>ONOS Project installed</figcaption>
</figure>

To update an application after a code change, just replace install! with
reinstall!.

    tools/onos-app 192.168.2.9 reinstall! ~/skku-app/target/skku-app-1.0-SNAPSHOT.oar

We can see that the application got installed and activated in the GUI.

<figure>
<img src="onos-app/gui reinstall.png" style="width:50.0%" />
<figcaption>ONOS Project in GUI</figcaption>
</figure>

And this is just the beginning, from here we can create ONOS
applications that are supported in the ONOS CLI, ONOS GUI and ONOS REST
API. To do so, when creating the ONOS application, add the following
flags.

    tools/onos-create-app cli org.foo foo-app 1.0-SNAPSHOT org.foo.app
    tools/onos-create-app rest org.foo foo-app 1.0-SNAPSHOT org.foo.app
    tools/onos-create-app ui org.foo foo-app 1.0-SNAPSHOT org.foo.app
    tools/onos-create-app uitab org.foo foo-app 1.0-SNAPSHOT org.foo.app
    tools/onos-create-app uitopo org.foo foo-app 1.0-SNAPSHOT org.foo.app
