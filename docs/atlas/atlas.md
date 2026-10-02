---
title: "Atlas - PetProto"
series: atlas
robot:
  name: "Atlas"
  thumbnail: https://i.imgur.com/Dt3plip.jpeg
---

## AtlasProto

https://www.youtube.com/watch?v=FFGfq0pRczY

AtlasProto is the start of the Atlas lineage, which was originally developed to explore the use of an upper body with limbs to traverse challenging terrain. AtlasProto began development in 2012, and is the original PetProto robot, modified with stripped down PETMAN arms. It is 150 cm tall and weights 61 kg, and has 16 DoF. Each arm had a shoulder with 2 DoF, an elbow with 1 DoF, and a passive spring-loaded prismatic joint located in the forearm with a rubber hemispherical nub where the hand would be.

The software strategy for AtlasProto was much different than PETProto or PETMAN. For basic walking, those robots were only concerned about where to place their foot relative to their body. But the goal for AtlasProto was to have it do more complex dynamic actions, such as climbing stairs, or jumping down from a ledge. In order to do this, the robot had to take into account specific "holds" on the world around it, like a stair step for example. To give AtlasProto its "vision", Boston Dynamics used a Vicon motion-capture system and placed retro-reflective tracking markers all over the body of the robot. This made it possible for it to get real-time feedback on where it was in the world.

## Atlas
