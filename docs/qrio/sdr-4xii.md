---
title: "Sony SDR-4X II"
series: qrio
robot:
  name: "Sony SDR-4 II"
  thumbnail: https://i.imgur.com/fvjD3EZ.png
---

## SDR-4X II

![](https://ascii.jp/img/2023/03/28/3514096/o/e6483dd25a3a1b93.jpg)

In Sony's continuing quest to commercialize QRIO, a new prototype was unveiled on March 24th, 2003, focusing on software elements that would translate to a more general consumer base.

In an interview with EE Times at ROBODEX2003, Tadatoshi Doi, president of Sony Corp.'s Intelligence Dynamics Laboratories, claimed that commercial release was projected for the following year and it would cost around $42,000. QRIO was never released commercially.

Though [SDR-4X](sdr-4x.md) and SDR-4X II have mostly the same exterior, here's how to differentiate them. On SDR-4X, the hands and knee joint are black. On SDR-4 II, the hands are grey and the knee joints are silver.

### QRIO Rebrand

![](https://sonny-dreams.github.io/images/QRIO-2.jpg)

On October 1st, 2003, Sony would drop the SDR (Sony Dream Robot) naming scheme and adopt a new one, QRIO.[^3] QRIO stands for "Quest for cuRIOsity" and sounds like the word "curiosity". QRIO would now be appointed as Sony group's corporate ambassador.

December 18th, 2003 is when QRIO made it's first appearance with it's new name.

![](https://i.imgur.com/OMAWp0a.jpeg) ![](https://i.imgur.com/b3lsvBZ.jpeg)

![](https://i.imgur.com/kPmJssr.jpeg) ![](https://i.imgur.com/Yka1EPz.jpeg)

During the promotion of the new QRIO brand, we were introduced to four individual QRIO robots: Charlie (Green), Marco (Yellow), Ken (Blue), and Audrey (Pink).

https://www.youtube.com/watch?v=bllJXLpNecg

### Hardware

![](https://i.imgur.com/2X68RjR.jpeg)

Pictured are the stereo cameras and main control board. QRIO is now equipped with three 64-bit RISC processors (mSDR, aSDR, and iSDR), each with 64 MB of memory. Each processor handles different tasks; mSDR is for motion control, aSDR is for speech recognition and synthesis, and iSDR is for vision and autonomous behavior control. The stereo image is processed by FPGAs to compute the disparity image which is then sent to the iSDR CPU.[^4]

![](https://i.imgur.com/26ONc5y.jpeg) ![](https://i.imgur.com/HiKhp1p.jpeg)

On the left image, you can see the five individually actuated fingers. On the right, interior shell made from magnesium alloy.

![](https://i.imgur.com/1DQge0G.jpeg)

Getting a view with it's chest plate flipped down, there are some points of interest.

![](https://i.pcmag.com/imagery/encyclopedia-terms/sony-memory-stick-_memstk.fit_lim.size_512x.gif)

The card slot on the left labled "Memory Stick" is a Sony Memory Stick slot with a 16 MB Memory Stick installed. Commonly used in Sony AIBO robot dogs, Memory Sticks were branded as AIBOware cards which carried unique personalities you could install into your AIBO.

![](https://pc.watch.impress.co.jp/docs/article/20001012/aibo11.jpg)

The card slot on the right is for a PC Card (type-II) and has an AIBO Wireless Lan Card installed. This, as the name implies, enables the wireless connectivity to QRIO.

Below the card slots is the power button in the center. You can toggle it when the shell is closed by pressing the glowing orb on it's chest. Below that are two recessed buttons with lables "mode" and "+". Above that is a mini LCD, most likely for battery level indication. We can also see that this QRIO's model number is 0157.

This hatch is also where the batteries can be replaced.

![](https://pc.watch.impress.co.jp/docs/2003/0405/p1040090.jpg)

A new charging port is added to the upper back, underneath the carrying handle. The port has exposed contacts for the pogo pins on it's charging station.

### Software

SDR-4X II's software upgrades have two themes, safety and localization. On the safety front, it can detect when something is being pinched between it's joints and stop it's motion from crushing it, also fall reaction and recovery. With localization, SDR-4X II can build an internal map using it's stereo cameras and infrared distance sensor, and can self-localize using this map.

https://www.youtube.com/watch?v=UWPx1bHDCWQ

When SDR-4X II was renamed to QRIO, Sony replaced the control theory allowing it to run and jump. This makes QRIO the world's first running humanoid robot.

September 2004, QRIO's walking gate was upgraded to be more natural. Using a heel-toe foot motion, it has a wider stride with a faster pace. It can also now climb and decend stairs autonomously by using it's new 2.5D map path planning.

### Ancillary Equipment

![](https://pc.watch.impress.co.jp/docs/2003/0405/p1040518.jpg)

![](https://pc.watch.impress.co.jp/docs/2003/0405/p1040028.jpg) ![](https://pc.watch.impress.co.jp/docs/2003/0405/p1040201.jpg)

SDR-4X II can sit in it's cradle to charge. This cradle is called it's "station".

![](https://pc.watch.impress.co.jp/docs/2004/1217/sony2543.jpg) ![](https://pc.watch.impress.co.jp/docs/2004/1217/sony2548.jpg)

A hard shelled travel case is used to transports QRIO.

### Variations

- #### QRIO Articulated Face

    ![](https://pc.watch.impress.co.jp/docs/2005/0422/kyokai0516.jpg)

    April 22th, 2005, during Sony's annual Intelligence Dynamics conference, a presentation of QRIO's speech imitation cababilities showcased a modified QRIO head with actuated eyelids and mouth.

    ![](https://image.itmedia.co.jp/lifestyle/articles/0504/10/ts_mabuta02.jpg) ![](https://image.itmedia.co.jp/lifestyle/articles/0504/10/ts_mabuta03.jpg)

    This QRIO variation can emulate expressions such as sadness, and act like it is sleeping. Also when it speaks, it will move its mouth up and down.

    Since it isn't officially documented very thoroughly, I'll make some assumptions on the mechanisms at play. For the eyelids, there seem to be top and bottom eyelids for each eye and they seem to open and close simultaneously, which probably means it uses a single actuator. The top eyelids can slant in opposite directions, also most likely driven by one actuator. Lastly the mouth can open and close, using one actuator. Altogether, 3 DOF were added.

- #### Possible QRIO II / SDR-4X III

    ![](https://pc.watch.impress.co.jp/docs/2005/1216/sony08.jpg)

    A new variation of QRIO was demonstrated at a press conference on January 23rd, 2006. Though this variation doesn't have a name, the upgrades would most likely be worthy of being its own version.

    ![](https://pc.watch.impress.co.jp/docs/2005/1216/sony10.jpg)

    Known hardware upgrades include two addtional degrees of freedom in each arm (wrist pitch/roll), a pressure sensor in each plam, and a new wide angle camera in the forhead bump replacing the infrared distance sensor. Also, QRIO can now lift and carry objects up to 120 grams.

    https://www.youtube.com/watch?v=SBKrC2-QvpE

    https://www.youtube.com/watch?v=Lvd5l_6KHD0

    This video demonsrates of the capabilities between the standard QRIO and this newly upgraded one.

### Research

### Appearances

- #### Beck - Hell Yes (Official Music Video)

    https://www.youtube.com/watch?v=z5U9QRiY46I

### Conclusion

On January 26th, 2006, just 3 days after showcasing their newest version, Sony discontinued all robot development going forward.

In an interview done by a project lead, if they had had approximately 2 more years to develop the project, it very well could have been released as a commercial product.

<!-- Kept exactly as on the original page: this list has no heading and shows as 1-2,
     while the in-text markers above are [3] and [4]. That is why it is raw HTML with
     explicit ids. To make the numbers match, replace it with a "### References"
     heading and a normal list starting at "3." (see README.md). -->
<ol class="references">
<li id="cite_note-03"><a href="https://www.sony.com/en/SonyInfo/News/Press/200310/03-1001E/">Small Biped Entertainment Robot "QRIO" Appointed as Sony Group's Corporate Ambassador</a></li>
<li id="cite_note-04"><a href="https://www.cs.columbia.edu/~allen/S19/SonyQRIO.pdf">Sony QRIO - Kenichiro Nagasaka</a></li>
</ol>
