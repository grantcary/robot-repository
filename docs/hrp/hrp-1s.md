---
title: "HRP-1S"
series: hrp
robot:
  name: "HRP-1S"
  thumbnail: https://i.imgur.com/YHk22cT.jpeg
---

## HRP-1S

![](https://i.imgur.com/nkCTh8n.jpeg)

In 2000, HRP-1S was unveild with a focus on the application of what was learned on [HRP-1](hrp-1.md). HRP-1S could operate machinery such as a forklift or an excavator.

### Hardware

For the most part, the robot body remained the same between versions. The one area which has been upgraded is the controller. With HRP-1, the controller used was the one that came in a standard Honda P3. It caused a lot of problems being sort of a black-box, unable to be modified because of Honda's proprietary design. The controller was also limited in functionality, only allowing either the arms to move, or the legs to move, but not at the same time. Posture control was also locked down.

The controller is a VMIC single-board computer located ([VMIVME-7740-877](https://www.artisantg.com/info/VMIC_VMIVME_7740_870_Datasheet_202011614034.pdf)) in the backpack. The board runs a [Pentium III 800 MHz](https://www.techpowerup.com/cpu-specs/pentium-iii-800.c1289) processor, 512 MB of RAM, and a 128 MB ComplactFlash. Onboard is a 2 Mbps wireless link, as well as an optional fiber link which allows reflective-memory link functionality. The reflective-memory link allows the onboard computer to share memory with another computer offboard the robot for monitoring. This was mostly used in the lab. Lateron, both the processor and the wireless link were upgraded to 850 MHz and 11 Mbps.[^3]

### Software

HRP-1S uses [ART-Linux](https://art-linux.sourceforge.net/) as its real-time operating system. The control cycle is 5 ms.

HRP-1S uses a plug-in architecture for managing operational modes. Plug-ins are the team's answer to having to build everything first, which is very complex and time consuming. This way the system can be built in pieces, allowing a more flexible development approach. It is also possible to hot reload plug-ins. If a bug needs fixing or something needs to change while the robot is running: edit and rebuild the source, unload the old plug-in, then load in the new one.

The list of available plug-ins are:
- HUMANOID: Servo on/off and gain control
- SEQPLAY: Motion file playback
- KWALK: Real time walking generation
- STABILIZER: Joint trajectory correction from SEQPLAY/KWALK
- LOG: Records everything

A manager loads and unloads plug-ins when needed. The non-real-time thread handles user input from the many options of control devices. The real-time thread reads the sensor data, processes that data through each loaded plug-in sequentially, then outputs motor commands. Both the real-time and non-real-time threads share the loaded plug-ins, ART-Linux allows them to communicate.

Everything is written in C++, except the ModelParser and OnlineViewer

### Remote Operation

![](https://i.imgur.com/1PMq0w9.jpeg)

There are two new control devices. The arms of the robot are controlled by a pair of 6 DOF master arms with force feed and moment back. The head direction can be changed using a joystick on the master arms.

![](https://i.imgur.com/YxtdqpC.jpeg)

Walking is controlled by the "master foot", which uses "tape type sensors" attached at the ankles, allowing for movement of the feet, directing the walking direction.

![](https://i.imgur.com/FR50zJE.jpeg)

A 3D monitor is used to view the robot's POV.

The second mode of operation is by joystick control. With the joystick, an operator can select whether they want to control the head, hands, wrists, torso, or feet. Once selected, the target can be controlled while the body moves with it.

### Heavy Machinery

![](https://i.imgur.com/yNllRrM.jpeg)

Some of the projected uses for a robot such as HRP-1S would be a construction site or a warehouse. So the team worked hard on making sure that it would be compatible in such environments, along with being able to use their tools.

![](https://i.imgur.com/3qG8dAB.jpeg)

A special nylon suit was designed specifically for outdoor use, using hooded areas to allow for ventilation and blocking water from getting inside.

![](https://i.imgur.com/KjCruUq.jpeg) ![](https://i.imgur.com/XCiD0lp.jpeg)

The suit was made in five separate parts: hood, vest, sleeves, pants and boots. The suit does not limit the operational range of motion of the robot.

![](https://i.imgur.com/XAlxZpu.jpeg) ![](https://i.imgur.com/xCO6eZy.jpeg)

HRP-1S could also use a forklift. All that was needed is a special seat which was built to isolate vibrations coming from whichever machine the robot needs to operate.

https://www.youtube.com/watch?v=2yofYo5L5T8

Here is a video showing HRP-1S sitting in a backhoe and operating it without its potective suit.

### Health Care

![](https://i.imgur.com/16d5jjl.jpeg)

![](https://i.imgur.com/GvxWZRx.jpeg) ![](https://i.imgur.com/KgwBAfg.jpeg)

### Variations

![](https://i.imgur.com/HSLvqGN.jpeg)

A version of HRP-1S in a white protective suit was seen at ROBODEX2003.

### References

3. [A tele-operated humanoid robot drives a backhoe in the open air - IEEE Xplore](https://ieeexplore.ieee.org/document/1248794)