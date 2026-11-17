EESchema Schematic File Version 2
LIBS:williamson
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Williamson KT88 - przelacznik kolumn Marantz/Lampa + pomiar VU"
Date ""
Rev "0.4"
Comp ""
Comment1 "Soloist 88 Stereo"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L RELAY_G2RL K1
U 1 1 538A840B
P 4000 2600
F 0 "K1" H 3750 2090 50  0000 L CNN
F 1 "G2RL-2-DC12" H 3750 2170 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 4000 2600 50  0001 C CNN
F 3 "" H 4000 2600 50  0001 C CNN
F 4 "LCSC" H 4000 2600 50  0001 C CNN "Supplier"
F 5 "C61458" H 4000 2600 50  0001 C CNN "Supplier Part"
	1    4000 2600
	1    0    0    -1  
$EndComp
$Comp
L CONNR_2 J1
U 1 1 5A91B54A
P 1300 2150
F 0 "J1" H 1200 1910 50  0000 L CNN
F 1 "MARANTZ_L" H 1200 1990 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 1300 2150 50  0001 C CNN
F 3 "" H 1300 2150 50  0001 C CNN
	1    1300 2150
	1    0    0    -1  
$EndComp
$Comp
L CONNR_2 J2
U 1 1 5398E4F0
P 1300 3050
F 0 "J2" H 1200 2810 50  0000 L CNN
F 1 "LAMPA_L" H 1200 2890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 1300 3050 50  0001 C CNN
F 3 "" H 1300 3050 50  0001 C CNN
	1    1300 3050
	1    0    0    -1  
$EndComp
$Comp
L CONN_2 J3
U 1 1 549FD466
P 6300 2550
F 0 "J3" H 6150 2310 50  0000 L CNN
F 1 "KOLUMNA_L" H 6150 2390 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 6300 2550 50  0001 C CNN
F 3 "" H 6300 2550 50  0001 C CNN
	1    6300 2550
	1    0    0    -1  
$EndComp
$Comp
L RELAY_G2RL K2
U 1 1 5A83D5B1
P 4000 5300
F 0 "K2" H 3750 4790 50  0000 L CNN
F 1 "G2RL-2-DC12" H 3750 4870 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 4000 5300 50  0001 C CNN
F 3 "" H 4000 5300 50  0001 C CNN
F 4 "LCSC" H 4000 5300 50  0001 C CNN "Supplier"
F 5 "C61458" H 4000 5300 50  0001 C CNN "Supplier Part"
	1    4000 5300
	1    0    0    -1  
$EndComp
$Comp
L CONNR_2 J4
U 1 1 5AFB41C5
P 1300 4850
F 0 "J4" H 1200 4610 50  0000 L CNN
F 1 "MARANTZ_R" H 1200 4690 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 1300 4850 50  0001 C CNN
F 3 "" H 1300 4850 50  0001 C CNN
	1    1300 4850
	1    0    0    -1  
$EndComp
$Comp
L CONNR_2 J5
U 1 1 5DFC7153
P 1300 5750
F 0 "J5" H 1200 5510 50  0000 L CNN
F 1 "LAMPA_R" H 1200 5590 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 1300 5750 50  0001 C CNN
F 3 "" H 1300 5750 50  0001 C CNN
	1    1300 5750
	1    0    0    -1  
$EndComp
$Comp
L CONN_2 J6
U 1 1 54F520E9
P 6300 5250
F 0 "J6" H 6150 5010 50  0000 L CNN
F 1 "KOLUMNA_R" H 6150 5090 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 6300 5250 50  0001 C CNN
F 3 "" H 6300 5250 50  0001 C CNN
	1    6300 5250
	1    0    0    -1  
$EndComp
$Comp
L CONNR_2 J7
U 1 1 53F2107F
P 1300 7200
F 0 "J7" H 1200 6960 50  0000 L CNN
F 1 "CEWKI" H 1200 7040 50  0000 L CNN
F 2 "williamson:PinHeader_1x02_P2.54" H 1300 7200 50  0001 C CNN
F 3 "" H 1300 7200 50  0001 C CNN
	1    1300 7200
	1    0    0    -1  
$EndComp
$Comp
L D_V D1
U 1 1 541298C4
P 2800 7200
F 0 "D1" H 2870 7180 50  0000 L CNN
F 1 "1N4148" H 2870 7260 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62" H 2800 7200 50  0001 C CNN
F 3 "" H 2800 7200 50  0001 C CNN
	1    2800 7200
	1    0    0    -1  
$EndComp
$Comp
L D_V D2
U 1 1 5D1BC97E
P 3400 7200
F 0 "D2" H 3470 7180 50  0000 L CNN
F 1 "1N4148" H 3470 7260 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62" H 3400 7200 50  0001 C CNN
F 3 "" H 3400 7200 50  0001 C CNN
	1    3400 7200
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 588A2D13
P 8000 2400
F 0 "R1" H 8060 2380 50  0000 L CNN
F 1 "100k 1%" H 8060 2460 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7" H 8000 2400 50  0001 C CNN
F 3 "" H 8000 2400 50  0001 C CNN
	1    8000 2400
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 56844C3F
P 8600 3000
F 0 "R3" H 8660 2980 50  0000 L CNN
F 1 "5k1 1%" H 8660 3060 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7" H 8600 3000 50  0001 C CNN
F 3 "" H 8600 3000 50  0001 C CNN
	1    8600 3000
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 5B530E03
P 9100 3000
F 0 "C1" H 9200 2980 50  0000 L CNN
F 1 "1n C0G" H 9200 3060 50  0000 L CNN
F 2 "williamson:C_Box_P5_7x4" H 9100 3000 50  0001 C CNN
F 3 "" H 9100 3000 50  0001 C CNN
	1    9100 3000
	1    0    0    -1  
$EndComp
$Comp
L D_V D3
U 1 1 5A1CF9E8
P 9700 2400
F 0 "D3" H 9770 2380 50  0000 L CNN
F 1 "BAT85" H 9770 2460 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 9700 2400 50  0001 C CNN
F 3 "" H 9700 2400 50  0001 C CNN
	1    9700 2400
	1    0    0    -1  
$EndComp
$Comp
L D_V D4
U 1 1 54786C4B
P 10300 3000
F 0 "D4" H 10370 2980 50  0000 L CNN
F 1 "BAT85" H 10370 3060 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 10300 3000 50  0001 C CNN
F 3 "" H 10300 3000 50  0001 C CNN
	1    10300 3000
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 51837CA9
P 8000 4700
F 0 "R2" H 8060 4680 50  0000 L CNN
F 1 "100k 1%" H 8060 4760 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7" H 8000 4700 50  0001 C CNN
F 3 "" H 8000 4700 50  0001 C CNN
	1    8000 4700
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 58E0D99C
P 8600 5300
F 0 "R4" H 8660 5280 50  0000 L CNN
F 1 "5k1 1%" H 8660 5360 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7" H 8600 5300 50  0001 C CNN
F 3 "" H 8600 5300 50  0001 C CNN
	1    8600 5300
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 525A5FB9
P 9100 5300
F 0 "C2" H 9200 5280 50  0000 L CNN
F 1 "1n C0G" H 9200 5360 50  0000 L CNN
F 2 "williamson:C_Box_P5_7x4" H 9100 5300 50  0001 C CNN
F 3 "" H 9100 5300 50  0001 C CNN
	1    9100 5300
	1    0    0    -1  
$EndComp
$Comp
L D_V D5
U 1 1 537F5CDD
P 9700 4700
F 0 "D5" H 9770 4680 50  0000 L CNN
F 1 "BAT85" H 9770 4760 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 9700 4700 50  0001 C CNN
F 3 "" H 9700 4700 50  0001 C CNN
	1    9700 4700
	1    0    0    -1  
$EndComp
$Comp
L D_V D6
U 1 1 5A760D67
P 10300 5300
F 0 "D6" H 10370 5280 50  0000 L CNN
F 1 "BAT85" H 10370 5360 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 10300 5300 50  0001 C CNN
F 3 "" H 10300 5300 50  0001 C CNN
	1    10300 5300
	1    0    0    -1  
$EndComp
$Comp
L R R5
U 1 1 5FE7E90A
P 8000 6700
F 0 "R5" H 8060 6680 50  0000 L CNN
F 1 "1k" H 8060 6760 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7_V" H 8000 6700 50  0001 C CNN
F 3 "" H 8000 6700 50  0001 C CNN
	1    8000 6700
	1    0    0    -1  
$EndComp
$Comp
L R R6
U 1 1 56EEB8B0
P 8000 7300
F 0 "R6" H 8060 7280 50  0000 L CNN
F 1 "1k" H 8060 7360 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7_V" H 8000 7300 50  0001 C CNN
F 3 "" H 8000 7300 50  0001 C CNN
	1    8000 7300
	1    0    0    -1  
$EndComp
$Comp
L CP C3
U 1 1 555D6F2F
P 8600 7300
F 0 "C3" H 8700 7280 50  0000 L CNN
F 1 "10u 16V" H 8700 7360 50  0000 L CNN
F 2 "williamson:CP_Radial_D6.3_P2.5" H 8600 7300 50  0001 C CNN
F 3 "" H 8600 7300 50  0001 C CNN
	1    8600 7300
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 J8
U 1 1 534D0DEE
P 10200 7000
F 0 "J8" H 10050 6660 50  0000 L CNN
F 1 "VU" H 10050 6740 50  0000 L CNN
F 2 "williamson:PinHeader_1x04_P2.54_H" H 10200 7000 50  0001 C CNN
F 3 "" H 10200 7000 50  0001 C CNN
	1    10200 7000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 6900 2800 7050
Wire Wire Line
	2800 6900 3100 6900
Wire Wire Line
	3100 6900 3400 6900
Wire Wire Line
	3400 6900 3400 7050
Wire Wire Line
	2800 7350 2800 7500
Wire Wire Line
	2800 7500 3100 7500
Wire Wire Line
	3100 7500 3400 7500
Wire Wire Line
	3400 7350 3400 7500
Wire Wire Line
	3100 6800 3100 6900
Wire Wire Line
	3100 7500 3100 7600
Wire Wire Line
	8000 2550 8000 2700
Wire Wire Line
	8000 2700 8600 2700
Wire Wire Line
	8600 2700 9100 2700
Wire Wire Line
	9100 2700 9700 2700
Wire Wire Line
	9700 2700 10300 2700
Wire Wire Line
	8600 2700 8600 2850
Wire Wire Line
	9100 2700 9100 2850
Wire Wire Line
	9700 2550 9700 2700
Wire Wire Line
	10300 2700 10300 2850
Wire Wire Line
	8600 3150 8600 3300
Wire Wire Line
	8600 3300 8850 3300
Wire Wire Line
	8850 3300 9100 3300
Wire Wire Line
	9100 3150 9100 3300
Wire Wire Line
	10300 2700 10800 2700
Wire Wire Line
	8850 3300 8850 3400
Wire Wire Line
	8000 4850 8000 5000
Wire Wire Line
	8000 5000 8600 5000
Wire Wire Line
	8600 5000 9100 5000
Wire Wire Line
	9100 5000 9700 5000
Wire Wire Line
	9700 5000 10300 5000
Wire Wire Line
	8600 5000 8600 5150
Wire Wire Line
	9100 5000 9100 5150
Wire Wire Line
	9700 4850 9700 5000
Wire Wire Line
	10300 5000 10300 5150
Wire Wire Line
	8600 5450 8600 5600
Wire Wire Line
	8600 5600 8850 5600
Wire Wire Line
	8850 5600 9100 5600
Wire Wire Line
	9100 5450 9100 5600
Wire Wire Line
	10300 5000 10800 5000
Wire Wire Line
	8850 5600 8850 5700
Wire Wire Line
	8000 6850 8000 7000
Wire Wire Line
	8000 7000 8000 7150
Wire Wire Line
	8000 7000 8600 7000
Wire Wire Line
	8600 7000 8600 7150
Wire Wire Line
	8000 7450 8000 7600
Wire Wire Line
	8000 7600 8300 7600
Wire Wire Line
	8300 7600 8600 7600
Wire Wire Line
	8600 7450 8600 7600
Wire Wire Line
	8300 7600 8300 7700
Wire Wire Line
	8600 7000 8900 7000
Wire Wire Line
	3500 2400 3600 2400
Wire Wire Line
	3500 2500 3600 2500
Wire Wire Line
	4400 2300 4500 2300
Wire Wire Line
	4400 2400 4500 2400
Wire Wire Line
	4400 2500 4500 2500
Wire Wire Line
	4400 2700 4500 2700
Wire Wire Line
	4400 2800 4500 2800
Wire Wire Line
	4400 2900 4500 2900
Wire Wire Line
	1600 2100 1700 2100
Wire Wire Line
	1600 2200 1700 2200
Wire Wire Line
	1600 3000 1700 3000
Wire Wire Line
	1600 3100 1700 3100
Wire Wire Line
	5900 2500 6000 2500
Wire Wire Line
	5900 2600 6000 2600
Wire Wire Line
	3500 5100 3600 5100
Wire Wire Line
	3500 5200 3600 5200
Wire Wire Line
	4400 5000 4500 5000
Wire Wire Line
	4400 5100 4500 5100
Wire Wire Line
	4400 5200 4500 5200
Wire Wire Line
	4400 5400 4500 5400
Wire Wire Line
	4400 5500 4500 5500
Wire Wire Line
	4400 5600 4500 5600
Wire Wire Line
	1600 4800 1700 4800
Wire Wire Line
	1600 4900 1700 4900
Wire Wire Line
	1600 5700 1700 5700
Wire Wire Line
	1600 5800 1700 5800
Wire Wire Line
	5900 5200 6000 5200
Wire Wire Line
	5900 5300 6000 5300
Wire Wire Line
	1600 7150 1700 7150
Wire Wire Line
	1600 7250 1700 7250
Wire Wire Line
	8000 2150 8000 2250
Wire Wire Line
	9700 2150 9700 2250
Wire Wire Line
	10300 3150 10300 3250
Wire Wire Line
	8000 4450 8000 4550
Wire Wire Line
	9700 4450 9700 4550
Wire Wire Line
	10300 5450 10300 5550
Wire Wire Line
	8000 6450 8000 6550
Wire Wire Line
	9800 6850 9900 6850
Wire Wire Line
	9800 6950 9900 6950
Wire Wire Line
	9800 7050 9900 7050
Wire Wire Line
	9800 7150 9900 7150
Connection ~ 3100 6900
Connection ~ 3100 7500
Connection ~ 8600 2700
Connection ~ 9100 2700
Connection ~ 9700 2700
Connection ~ 10300 2700
Connection ~ 8850 3300
Connection ~ 8600 5000
Connection ~ 9100 5000
Connection ~ 9700 5000
Connection ~ 10300 5000
Connection ~ 8850 5600
Connection ~ 8000 7000
Connection ~ 8600 7000
Connection ~ 8300 7600
Text Label 3100 6800 1    50   ~ 0
+12V
Text Label 3100 7600 3    50   ~ 0
RLY_SPK
Text Label 10800 2700 0    50   ~ 0
VU_L
Text Label 8850 3400 3    50   ~ 0
VMID
Text Label 10800 5000 0    50   ~ 0
VU_R
Text Label 8850 5700 3    50   ~ 0
VMID
Text Label 8300 7700 3    50   ~ 0
GND
Text Label 8900 7000 0    50   ~ 0
VMID
Text Label 3500 2400 2    50   ~ 0
+12V
Text Label 3500 2500 2    50   ~ 0
RLY_SPK
Text Label 4500 2300 0    50   ~ 0
SPK_LP
Text Label 4500 2400 0    50   ~ 0
MAR_LP
Text Label 4500 2500 0    50   ~ 0
TUBE_LP
Text Label 4500 2700 0    50   ~ 0
SPK_LN
Text Label 4500 2800 0    50   ~ 0
MAR_LN
Text Label 4500 2900 0    50   ~ 0
TUBE_LN
Text Label 1700 2100 0    50   ~ 0
MAR_LP
Text Label 1700 2200 0    50   ~ 0
MAR_LN
Text Label 1700 3000 0    50   ~ 0
TUBE_LP
Text Label 1700 3100 0    50   ~ 0
TUBE_LN
Text Label 5900 2500 2    50   ~ 0
SPK_LP
Text Label 5900 2600 2    50   ~ 0
SPK_LN
Text Label 3500 5100 2    50   ~ 0
+12V
Text Label 3500 5200 2    50   ~ 0
RLY_SPK
Text Label 4500 5000 0    50   ~ 0
SPK_RP
Text Label 4500 5100 0    50   ~ 0
MAR_RP
Text Label 4500 5200 0    50   ~ 0
TUBE_RP
Text Label 4500 5400 0    50   ~ 0
SPK_RN
Text Label 4500 5500 0    50   ~ 0
MAR_RN
Text Label 4500 5600 0    50   ~ 0
TUBE_RN
Text Label 1700 4800 0    50   ~ 0
MAR_RP
Text Label 1700 4900 0    50   ~ 0
MAR_RN
Text Label 1700 5700 0    50   ~ 0
TUBE_RP
Text Label 1700 5800 0    50   ~ 0
TUBE_RN
Text Label 5900 5200 2    50   ~ 0
SPK_RP
Text Label 5900 5300 2    50   ~ 0
SPK_RN
Text Label 1700 7150 0    50   ~ 0
+12V
Text Label 1700 7250 0    50   ~ 0
RLY_SPK
Text Label 8000 2150 1    50   ~ 0
TUBE_LP
Text Label 9700 2150 1    50   ~ 0
3V3
Text Label 10300 3250 3    50   ~ 0
GND
Text Label 8000 4450 1    50   ~ 0
TUBE_RP
Text Label 9700 4450 1    50   ~ 0
3V3
Text Label 10300 5550 3    50   ~ 0
GND
Text Label 8000 6450 1    50   ~ 0
3V3
Text Label 9800 6850 2    50   ~ 0
3V3
Text Label 9800 6950 2    50   ~ 0
GND
Text Label 9800 7050 2    50   ~ 0
VU_L
Text Label 9800 7150 2    50   ~ 0
VU_R
Text Notes 800 1000 0    60   ~ 16
Przelacznik kolumn Marantz / Lampa + pomiar sygnalu do wskaznikow VU - Williamson KT88
Text Notes 800 1120 0    60   ~ 16
Cewki bez pradu: kolumny <- Marantz (NC). Lampa gotowa (ESP32): kolumny <- Lampa (NO). Oba bieguny przelaczane.
Text Notes 800 1240 0    60   ~ 16
ESP32 przelacza tylko przy MUTE. RL 100R 2W zostaje na wtornym kazdego toroidu (odczep 4 Ohm - COM).
Text Notes 7300 1600 0    60   ~ 16
POMIAR VU: odczep 4 Ohm PRZED przekaznikiem -> 100k / 5k1 do 1,65 V
Text Notes 7300 1720 0    60   ~ 16
45 W / 4 Ohm = 19 V szczyt -> +-0,92 V na ADC. GND toru VU = masa sterowania,
Text Notes 7300 1840 0    60   ~ 16
NIE laczyc z TUBE_xN na plytce (COM toroidu jest uziemiony na plytce Onyxa).
Text Notes 7300 7900 0    60   ~ 16
J8 -> sterowanie: 3V3, GND, GPIO2 (L), GPIO3 (P)
Text Notes 800 7900 0    60   ~ 16
J7: z plytki sterowania J13 (+12 V, RLY_SPK)
$EndSCHEMATC
