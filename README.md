# $100 Optical Computer
Everything related to the CERN MicroClub webfest 2024 project to build an Optical Computer and use it to simulate a quantum computer. We haven't started yet...


#### Task 1: Wire everything together.

We're using the pinouts from here:
- http://www.lcdwiki.com/2.4inch_RPi_Display

- http://www.lcdwiki.com/3.5inch_RPi_Display

We need to wire up both screens to the Pi using some jumpers:
<br>
Here are the relevant pins:
#### 2.4" screen:


| PIN NO.            | SYMBOL           | DESCRIPTION                                                             |
| ------------------ | ---------------- | ----------------------------------------------------------------------- |
|                                                                                                                 |
| 1, 17              | 3.3V             | Power positive (3.3V power input)                                       |
| 2, 4               | 5V               | Power positive (5V power input)                                         |
| 3, 5, 7, 8, 10, 22 | NC               | Not connected                                                           |
| 6, 9, 14, 20, 25   | GND              | Ground                                                                  |
| 15                 | LCD_RS           | LCD instruction control, Instruction/Data Register selection            |
| 19                 | LCD_SI / TP_SI   | SPI data input of LCD/Touch Panel                                       |
| 21                 | TP_SO            | SPI data output of Touch Panel                                          |
| 23                 | LCD_SCK / TP_SCK | SPI clock of LCD/Touch Panel                                            |
| 24                 | LCD_CS           | LCD chip selection, low active                                          |


<!--  
1, 17 	3.3V 	Power supply (3.3V power input)
2, 4 	5V 	Power supply (5V power input)
3, 5, 7, 8, 10, 12， 16，18，22 	NC 	Not connected
6, 9, 14, 20, 25 	GND 	Power ground
15 	LCD_RS 	Instruction/data register selection, low level is instruction, high level is data
19 	LCD_SI / TP_SI 	LCD display / touch panel SPI data input
21 	TP_SO 	Touch panel SPI data output
13 	RST 	Reset signal, low reset
23 	LCD_SCK / TP_SCK 	LCD display / touch panel SPI clock signal
24 	LCD_CS 	LCD chip select signal, low level enable
-->
#### 3.5" screen


| PIN NO.                        | SYMBOL           | DESCRIPTION                                                             |
| ------------------------------ | ---------------- | ----------------------------------------------------------------------- |
|  |
| 18                             | LCD_RS           | Instruction/Data Register selection                                     |
| 19                             | LCD_SI / TP_SI   | SPI data input of LCD/Touch Panel                                       |
| 21                             | TP_SO            | SPI data output of Touch Panel                                          |
| 22                             | RST              | Reset                                                                   |
| 23                             | LCD_SCK / TP_SCK | SPI clock of LCD/Touch Panel                                            |
| 24                             | LCD_CS           | LCD chip selection, low active                                          |

<!--  
18 	LCD_RS 	Instruction/Data Register selection
19 	LCD_SI / TP_SI 	SPI data input of LCD/Touch Panel
21 	TP_SO 	SPI data output of Touch Panel
22 	RST 	Reset
23 	LCD_SCK / TP_SCK 	SPI clock of LCD/Touch Panel
24 	LCD_CS 	LCD chip selection, low active 
-->

The Raspberry Pi 4 Model B official GPIO pinouts are here:
https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-datasheet.pdf

And some advice on wiring up ouyr WS2812Bs from here:
https://core-electronics.com.au/guides/fully-addressable-rgb-raspberry-pi/

In summary:
<!--  
1,NC
2,SPI Screen 1
3,NC
4,SPI Screen 2 + LED power (unless we can find this elsewhere)
5,NC
6,SPI Screen 1 GND
7,NC
8,NC
9,SPI Screen 2 GND
10,NC
11,NC
12,LED Data
13,NC
14,LED GND
15,LCD_RS (common or one per screen?)
16,NC
17,NC
18,LCD_RS (if using 3.5" screens..)
19,LCD_SI (Screen 1)
20,NC
21,NC (we don't need the touch panels)
22,RST (Screen 1)
23,LCD_SCK (Screen 1 clock)
24,LCD_CS (Screen 1 chip select)
25,NC
26,NC
28,NC
29,NC
30,NC
31,NC
32,NC
33,NC
34,NC
35,NC
36,LCD_CS (Screen 2 chip select)
37,NC
38,LCD_SI (Screen 2)
39,NC
40,LCD_SCK (Screen 2 clock)
-->

| PIN RP | PERIPHERAL                                                   |
| ------ | ------------------------------------------------------------ |
| 1      | NC                                                           |
| 2      | SPI Screen 1                                                 |
| 3      | NC                                                           |
| 4      | SPI Screen 2 + LED power (unless we can find this elsewhere) |
| 5      | NC                                                           |
| 6      | SPI Screen 1 GND                                             |
| 7      | NC                                                           |
| 8      | NC                                                           |
| 9      | SPI Screen 2 GND                                             |
| 10     | NC                                                           |
| 11     | NC                                                           |
| 12     | LED Data                                                     |
| 13     | NC                                                           |
| 14     | LED GND                                                      |
| 15     | LCD_RS (common or one per screen?)                           |
| 16     | NC                                                           |
| 17     | NC                                                           |
| 18     | LCD_RS (if using 3.5" screens..)                             |
| 19     | LCD_SI (Screen 1)                                            |
| 20     | NC                                                           |
| 21     | NC (we don't need the touch panels)                          |
| 22     | RST (Screen 1)                                               |
| 23     | LCD_SCK (Screen 1 clock)                                     |
| 24     | LCD_CS (Screen 1 chip select)                                |
| 25     | NC                                                           |
| 26     | NC                                                           |
| 28     | NC                                                           |
| 29     | NC                                                           |
| 30     | NC                                                           |
| 31     | NC                                                           |
| 32     | NC                                                           |
| 33     | NC                                                           |
| 34     | NC                                                           |
| 35     | NC                                                           |
| 36     | LCD_CS (Screen 2 chip select)                                |
| 37     | NC                                                           |
| 38     | LCD_SI (Screen 2)                                            |
| 39     | NC                                                           |
| 40     | LCD_SCK (Screen 2 clock)                                     |

Here is someone doing something very similar to what we are doing:
https://forums.raspberrypi.com/viewtopic.php?t=325328
