---
title: "E2-DR"
header: "E2-DR"
robot:
  name: "Honda E2-DR"
  thumbnail: https://i.imgur.com/96vJGQn.png
  letter: E
---

## Honda E2-DR

https://www.youtube.com/watch?v=uat8laSf7gc

On October 2nd during IROS 2017, Honda published the paper "Development of Experimental Legged Robot for Inspection and Disaster Response in Plants", giving a glimpse into what Honda R&D had been working on as a redirection of the ASIMO project. E2-DR is a robot designed for disaster response (hence the "DR" in E2-DR), meaning that from the ground up, it needed to be durable, capable, and reliable.

This robot was born from aftermath of the Fukushima disaster. With not a single robot capable of entering the dangerous landscape, Honda started switching gears away from the ASIMO project as we knew it, and refocusing efforts into something that could be put to practical use.

### Prototypes

https://www.youtube.com/watch?v=Sta-1gPrRSQ

The first experimentation with this robot line was the E series-like robot with ASIMO legs and a laser range finder, along with better terrain navigation software, shown off in the same NHK documentary.

https://www.youtube.com/watch?v=794YNdvOgKI

Prototype mockup first seen in NHK documentary robot revolution airing in 2014, the design more akin to the Honda P series with a blend of ASIMO.

![](https://i.imgur.com/6r2i00p.jpeg)

The first official E2-DR prototype was built to accommodate the desired dynamic movements. It stood 1.675 m tall and weighed 85 kg. It had a total of 33 degrees of freedom (DOF): 6 per leg, 8 per arm, 1 per hand, 2 in the torso, and 1 for the neck.

![](https://i.imgur.com/89o09L1.png)

According to the paper "Dynamic Gait Transition between Bipedal and Quadrupedal Locomotion", the initial goal for the new hardware to achieve was a gait transition from walking to crawling. The planning and control alorithm is an extention of ASIMO's planning and control which allows it to transition from running, walking and jumping smoothly. The papter "Robust Vertical Ladder Climbing and Transitioning between Ladder and Catwalk for Humanoid Robots" outlines their approach for transitioning to a ladder and climbing.

### E2-DR Hardware

![](https://i.imgur.com/K76QRBn.png)

![](https://i.imgur.com/37b2s4N.png)

With the purpose of this robot being to work in disaster response scenarios, the head is packed full of sensors that allow it to see in many different ways. First, it has two rotating Hokuyo UTM30LX-EW laser range finders, gathering a point cloud of E2-DR's surroundings. Secondly, it has a stereo camera/infrared light projector package allowing it to see in the dark. The last two are a SwissRanger SR4000 TOF (time-of-flight) camera and a monocular camera that can sync to an LED flash, illuminating the scene.

https://www.youtube.com/watch?v=5lZ1bTGCZpQ
