---
title: "HRP-1"
series: hrp
robot:
  name: "HRP-1"
  thumbnail: https://i.imgur.com/FBupDfm.jpeg
---

## HRP-1

![](https://i.imgur.com/myVz9Za.jpeg)

In the fiscal year of 1998, The Ministry of Economy Trade and Insdustry (METI) of Japan announced a 5 year long project called the Humanoid Robot Project (HRP). The project had an approximate budget of 5 billion yen. The humanoid robot project is a colaboration with many companies and research labs across Japan.

The goal for this project was to build a tele-existence robotic platform that would be capable of working in construction sites, disaster zones, and care for elderly/handicap people.

The project was broken up into two phases. The first phase had a focus on building out the hardware technology, developing three main components; the humanoid platform, the virtual platform, and the remote operation cockpit. The second phase was focused on the application of such hardware (covered in HRP-1S page).

### Humanoid Platform

![](https://i.imgur.com/KKcvPYD.jpeg) ![](https://i.imgur.com/8E613s0.jpeg)

Honda R&D supplied the HRP with four of their [P3](../p-series/p3.md) humanoid robots. Besides having the color changed to yellow, they were also modified with a custom communication interface where it could use either ethernet or fiber optics. HRP-1 could be used either wirelessly or tethered.

### Virtual Platform

The virtual platform was developed by Fujitsu, Hitachi, the Mechanical Engineering Research Laboratory, the Central Research Institute of Electric Power Industry, Waseda University, and the University of Tokyo

### Remote Operation Cockpit

![](https://i.imgur.com/aSNCjA0.jpeg)

The remote operation cockpits were developed by Matsushita Electric, Kawasaki Heavy Industries, FANUC, and Toshiba. Two different cockpits were conceived, the super cockpit, and the minimum cockpit.

https://www.youtube.com/watch?v=JYQDPR9op2E

The super cockpit was a highly emersive telepresence control system where a user could pilot the robot using haptic master control arms. It was completed in March of 2000.[^1]

The super cockpit was made up of three subsystems:

- 3D Audio/Visual Display subsystem
- Telepresence Master subsystem
- Cockpit and Robot Communication subsystem

![](https://i.imgur.com/87TsRD1.png)

Starting with the 3D audio/visual display subsystem, the robot is externally fitted with a stereo multi-camera system. Each multi-camera system has four cameras, one facing forwards, another facing down, and the others facing left and right. The combined horizontal field of view (FOV) is 150 degrees, upper vertical is 19 degrees, and lower vertical is 58 degrees. The stereo multi-cameras are separated by 65mm, which is about the average adult human's pupillary distance (PD).

![](https://i.imgur.com/SKG6ULf.png) ![](https://i.imgur.com/YnEgmCR.png)

Nine screens surround the cockpit (later reduced to six screens), giving a wide field of view of the robot's surroundings, however, only four of the screens are dedicated to displaying the point of view (POV) fo the robot. Each screen is 60 inches, and has two projectors projecting polarized right eye and left eye images. The operator wears polarizing glasses to utilize the stereo image.

![](https://i.imgur.com/46grIMQ.png) ![](https://i.imgur.com/AGS9v6v.png)

To help the operator from getting disoriented, they can see a virtual reconstruction of the robot's current surroundings on one of the cockpit's screens. The scene is created before piloting using VRML (Virtual Reality Modeling Language).

![](https://i.imgur.com/kqnDPlq.jpeg)

When manipulating objects, operator uses a head mounted display (HMD), which takes the feed from the stereo cameras built into the head of the P3. The HMD then tracks the movement of the operator's head at 300 Hz, and subsequently moves the robot's head with latency lower than 2 ms. The HMD FOV is 48 degrees horizontally, and 36 vertically.

![](https://i.imgur.com/9lSC0LK.png) ![](https://i.imgur.com/26UWdK9.png)

Next, the telepresence master subsystem consists of two master arms, left and right, each with a gripping actuation device, a motion base, and 3D mouse.

Using these master arms, the operator can directly manipulate the arms of the robot. They are designed to act like an exoskeleton, each having 7 degrees of freedom (DOF). The operator's only point of contact with the master arm are the hand grips. So in order to move the position of the elbows, they have optical sensors to measure the distance between itself and the elbow of the operator, moving them appropriately. The joint motors on the master arms providing force feedback can represent forces up to 10 Newtons.

An operator leans back onto the seat of the motion base, which can simulate the feeling of walking, displacement, and upper body inclination of the robot. To reduce the distortion of perspective, the seat can only move in three directions, back and forth (surge), left and right (sway), and up and down (heave).

The 3D mouse is used to input commands to the main control program, such as to change the control mode.

Lastly, the cockpit and robot communication subsystem. Audio/visual data is transmitted via an analog communication module, while control data is exchanged through a shared memory module called Reflective Memory Module, which syncs up all of the subsystems.

### References

1. [Telexistence and Retro-reflective Projection Technology (RPT)](https://tachilab.org/content/files/publication/ic/tachi200305VRIC.pdf)
