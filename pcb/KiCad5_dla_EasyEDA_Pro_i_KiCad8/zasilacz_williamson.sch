EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title "Williamson KT88 - plytka zasilacza (siec, opoznienie anod, bias AC, pomiar Ua)"
Date ""
Rev "0.4"
Comp ""
Comment1 "Soloist 88 Stereo"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L williamson:CONNR_2 J1
U 1 1 5A91B54A
P 900 2050
F 0 "J1" H 800 1810 50  0000 L CNN
F 1 "SIEC" H 800 1890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08_V" H 900 2050 50  0001 C CNN
F 3 "~" H 900 2050 50  0001 C CNN
	1    900 2050
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONNR_2 J3
U 1 1 549FD466
P 900 3050
F 0 "J3" H 800 2810 50  0000 L CNN
F 1 "PS1" H 800 2890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08_V" H 900 3050 50  0001 C CNN
F 3 "~" H 900 3050 50  0001 C CNN
	1    900 3050
	1    0    0    -1  
$EndComp
$Comp
L williamson:FUSE_H F2
U 1 1 5F2DABFC
P 1600 3000
F 0 "F2" H 1520 2940 50  0000 L CNN
F 1 "T500mA 250V" H 1520 3090 50  0000 L CNN
F 2 "williamson:Fuseholder_5x20_Closed_P22.5" H 1600 3000 50  0001 C CNN
F 3 "~" H 1600 3000 50  0001 C CNN
	1    1600 3000
	1    0    0    -1  
$EndComp
$Comp
L williamson:RELAY_G2RL K1
U 1 1 538A840B
P 2900 2300
F 0 "K1" H 2650 1790 50  0000 L CNN
F 1 "G2RL-2-DC12" H 2650 1870 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 2900 2300 50  0001 C CNN
F 3 "~" H 2900 2300 50  0001 C CNN
F 4 "LCSC" H 2900 2300 50  0001 C CNN "Supplier"
F 5 "C61458" H 2900 2300 50  0001 C CNN "Supplier Part"
	1    2900 2300
	1    0    0    -1  
$EndComp
$Comp
L williamson:RH R1
U 1 1 588A2D13
P 3900 2200
F 0 "R1" H 3840 2140 50  0000 L CNN
F 1 "47R 10W" H 3840 2270 50  0000 L CNN
F 2 "williamson:R_Cement_10W_P55.88_V" H 3900 2200 50  0001 C CNN
F 3 "~" H 3900 2200 50  0001 C CNN
	1    3900 2200
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_2 J5
U 1 1 5DFC7153
P 5400 2250
F 0 "J5" H 5250 2010 50  0000 L CNN
F 1 "TR1_PRI" H 5250 2090 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08_V" H 5400 2250 50  0001 C CNN
F 3 "~" H 5400 2250 50  0001 C CNN
	1    5400 2250
	1    0    0    -1  
$EndComp
$Comp
L williamson:RELAY_G2RL K2
U 1 1 5A83D5B1
P 4300 3000
F 0 "K2" H 4050 2490 50  0000 L CNN
F 1 "G2RL-2-DC12" H 4050 2570 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 4300 3000 50  0001 C CNN
F 3 "~" H 4300 3000 50  0001 C CNN
F 4 "LCSC" H 4300 3000 50  0001 C CNN "Supplier"
F 5 "C61458" H 4300 3000 50  0001 C CNN "Supplier Part"
	1    4300 3000
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONNR_2 J7
U 1 1 53F2107F
P 900 4550
F 0 "J7" H 800 4310 50  0000 L CNN
F 1 "S1_IN" H 800 4390 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P7.62_V" H 900 4550 50  0001 C CNN
F 3 "~" H 900 4550 50  0001 C CNN
	1    900 4550
	1    0    0    -1  
$EndComp
$Comp
L williamson:FUSE_H F3
U 1 1 582A9B6A
P 1600 4500
F 0 "F3" H 1520 4440 50  0000 L CNN
F 1 "T1A 500V" H 1520 4590 50  0000 L CNN
F 2 "williamson:Fuseholder_5x20_Closed_P22.5_V" H 1600 4500 50  0001 C CNN
F 3 "~" H 1600 4500 50  0001 C CNN
	1    1600 4500
	1    0    0    -1  
$EndComp
$Comp
L williamson:RELAY_G2RL K3
U 1 1 5D84E527
P 2700 4800
F 0 "K3" H 2450 4290 50  0000 L CNN
F 1 "G2RL-2-DC12" H 2450 4370 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 2700 4800 50  0001 C CNN
F 3 "~" H 2700 4800 50  0001 C CNN
F 4 "LCSC" H 2700 4800 50  0001 C CNN "Supplier"
F 5 "C61458" H 2700 4800 50  0001 C CNN "Supplier Part"
	1    2700 4800
	1    0    0    -1  
$EndComp
$Comp
L williamson:RH R2
U 1 1 51837CA9
P 3900 5100
F 0 "R2" H 3840 5040 50  0000 L CNN
F 1 "100R 10W" H 3840 5170 50  0000 L CNN
F 2 "williamson:R_Cement_10W_P55.88_V" H 3900 5100 50  0001 C CNN
F 3 "~" H 3900 5100 50  0001 C CNN
	1    3900 5100
	1    0    0    -1  
$EndComp
$Comp
L williamson:RELAY_G2RL K4
U 1 1 53E07084
P 4300 5900
F 0 "K4" H 4050 5390 50  0000 L CNN
F 1 "G2RL-2-DC12" H 4050 5470 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 4300 5900 50  0001 C CNN
F 3 "~" H 4300 5900 50  0001 C CNN
F 4 "LCSC" H 4300 5900 50  0001 C CNN "Supplier"
F 5 "C61458" H 4300 5900 50  0001 C CNN "Supplier Part"
	1    4300 5900
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_2 J8
U 1 1 534D0DEE
P 5700 5150
F 0 "J8" H 5550 4910 50  0000 L CNN
F 1 "HT_L" H 5550 4990 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P7.62_V" H 5700 5150 50  0001 C CNN
F 3 "~" H 5700 5150 50  0001 C CNN
	1    5700 5150
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_2 J9
U 1 1 544A3D78
P 5700 5550
F 0 "J9" H 5550 5310 50  0000 L CNN
F 1 "HT_R" H 5550 5390 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P7.62_V" H 5700 5550 50  0001 C CNN
F 3 "~" H 5700 5550 50  0001 C CNN
	1    5700 5550
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONNR_2 J10
U 1 1 52C8E61A
P 900 7050
F 0 "J10" H 800 6810 50  0000 L CNN
F 1 "S4_IN" H 800 6890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08_V" H 900 7050 50  0001 C CNN
F 3 "~" H 900 7050 50  0001 C CNN
	1    900 7050
	1    0    0    -1  
$EndComp
$Comp
L williamson:FUSE_H F4
U 1 1 564E0EC9
P 1600 7000
F 0 "F4" H 1520 6940 50  0000 L CNN
F 1 "T100mA 250V" H 1520 7090 50  0000 L CNN
F 2 "williamson:Fuseholder_5x20_Closed_P22.5" H 1600 7000 50  0001 C CNN
F 3 "~" H 1600 7000 50  0001 C CNN
	1    1600 7000
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_2 J11
U 1 1 55CFD68C
P 2600 7050
F 0 "J11" H 2450 6810 50  0000 L CNN
F 1 "BIAS_L" H 2450 6890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 2600 7050 50  0001 C CNN
F 3 "~" H 2600 7050 50  0001 C CNN
	1    2600 7050
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_2 J12
U 1 1 5CC68736
P 2600 7450
F 0 "J12" H 2450 7210 50  0000 L CNN
F 1 "BIAS_R" H 2450 7290 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 2600 7450 50  0001 C CNN
F 3 "~" H 2600 7450 50  0001 C CNN
	1    2600 7450
	1    0    0    -1  
$EndComp
$Comp
L williamson:PAD_L J13
U 1 1 5BC1B7A0
P 7500 2000
F 0 "J13" H 7250 1980 50  0000 L CNN
F 1 "UA_IN" H 7250 2060 50  0000 L CNN
F 2 "williamson:WirePad_4.5" H 7500 2000 50  0001 C CNN
F 3 "~" H 7500 2000 50  0001 C CNN
	1    7500 2000
	1    0    0    -1  
$EndComp
$Comp
L williamson:R R3
U 1 1 56844C3F
P 8200 2250
F 0 "R3" H 8260 2230 50  0000 L CNN
F 1 "1M 1600V" H 8260 2310 50  0000 L CNN
F 2 "williamson:R_Axial_1W_P15.24_V" H 8200 2250 50  0001 C CNN
F 3 "~" H 8200 2250 50  0001 C CNN
	1    8200 2250
	1    0    0    -1  
$EndComp
$Comp
L williamson:R R4
U 1 1 58E0D99C
P 8200 2550
F 0 "R4" H 8260 2530 50  0000 L CNN
F 1 "1M 1600V" H 8260 2610 50  0000 L CNN
F 2 "williamson:R_Axial_1W_P15.24_V" H 8200 2550 50  0001 C CNN
F 3 "~" H 8200 2550 50  0001 C CNN
	1    8200 2550
	1    0    0    -1  
$EndComp
$Comp
L williamson:R R5
U 1 1 5FE7E90A
P 8200 2850
F 0 "R5" H 8260 2830 50  0000 L CNN
F 1 "1M 1600V" H 8260 2910 50  0000 L CNN
F 2 "williamson:R_Axial_1W_P15.24_V" H 8200 2850 50  0001 C CNN
F 3 "~" H 8200 2850 50  0001 C CNN
	1    8200 2850
	1    0    0    -1  
$EndComp
$Comp
L williamson:R R6
U 1 1 56EEB8B0
P 8200 3150
F 0 "R6" H 8260 3130 50  0000 L CNN
F 1 "15k" H 8260 3210 50  0000 L CNN
F 2 "williamson:R_Axial_0.5W_P12.7_V" H 8200 3150 50  0001 C CNN
F 3 "~" H 8200 3150 50  0001 C CNN
	1    8200 3150
	1    0    0    -1  
$EndComp
$Comp
L williamson:PAD J14
U 1 1 55A52203
P 8800 3000
F 0 "J14" H 8880 2980 50  0000 L CNN
F 1 "HV_SENSE" H 8880 3060 50  0000 L CNN
F 2 "williamson:WirePad_3.5" H 8800 3000 50  0001 C CNN
F 3 "~" H 8800 3000 50  0001 C CNN
	1    8800 3000
	1    0    0    -1  
$EndComp
$Comp
L williamson:R R7
U 1 1 51E98826
P 9200 2250
F 0 "R7" H 9260 2230 50  0000 L CNN
F 1 "220k 1W" H 9260 2310 50  0000 L CNN
F 2 "williamson:R_Axial_1W_P15.24_V" H 9200 2250 50  0001 C CNN
F 3 "~" H 9200 2250 50  0001 C CNN
	1    9200 2250
	1    0    0    -1  
$EndComp
$Comp
L williamson:R R8
U 1 1 515695B7
P 9200 2550
F 0 "R8" H 9260 2530 50  0000 L CNN
F 1 "220k 1W" H 9260 2610 50  0000 L CNN
F 2 "williamson:R_Axial_1W_P15.24_V" H 9200 2550 50  0001 C CNN
F 3 "~" H 9200 2550 50  0001 C CNN
	1    9200 2550
	1    0    0    -1  
$EndComp
$Comp
L williamson:D D1
U 1 1 541298C4
P 9200 2850
F 0 "D1" H 9280 2830 50  0000 L CNN
F 1 "LED HV czerwona" H 9280 2910 50  0000 L CNN
F 2 "williamson:LED_D3.0_P2.54" H 9200 2850 50  0001 C CNN
F 3 "~" H 9200 2850 50  0001 C CNN
	1    9200 2850
	1    0    0    -1  
$EndComp
$Comp
L williamson:PAD J15
U 1 1 52A21295
P 8800 3800
F 0 "J15" H 8880 3780 50  0000 L CNN
F 1 "GND_ONYX" H 8880 3860 50  0000 L CNN
F 2 "williamson:WirePad_4.5" H 8800 3800 50  0001 C CNN
F 3 "~" H 8800 3800 50  0001 C CNN
	1    8800 3800
	1    0    0    -1  
$EndComp
$Comp
L williamson:PAD J18
U 1 1 5C136E28
P 8800 4100
F 0 "J18" H 8880 4080 50  0000 L CNN
F 1 "GND_STER" H 8880 4160 50  0000 L CNN
F 2 "williamson:WirePad_3.5" H 8800 4100 50  0001 C CNN
F 3 "~" H 8800 4100 50  0001 C CNN
	1    8800 4100
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_3 J16
U 1 1 5BAB432F
P 2600 9050
F 0 "J16" H 2450 8760 50  0000 L CNN
F 1 "RELAY_A" H 2450 8840 50  0000 L CNN
F 2 "williamson:PinHeader_1x03_P2.54" H 2600 9050 50  0001 C CNN
F 3 "~" H 2600 9050 50  0001 C CNN
	1    2600 9050
	1    0    0    -1  
$EndComp
$Comp
L williamson:CONN_3 J17
U 1 1 5CAC73B9
P 2600 9650
F 0 "J17" H 2450 9360 50  0000 L CNN
F 1 "RELAY_B" H 2450 9440 50  0000 L CNN
F 2 "williamson:PinHeader_1x03_P2.54" H 2600 9650 50  0001 C CNN
F 3 "~" H 2600 9650 50  0001 C CNN
	1    2600 9650
	1    0    0    -1  
$EndComp
$Comp
L williamson:D_V D2
U 1 1 5D1BC97E
P 3400 9300
F 0 "D2" H 3470 9280 50  0000 L CNN
F 1 "1N4148" H 3470 9360 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 3400 9300 50  0001 C CNN
F 3 "~" H 3400 9300 50  0001 C CNN
	1    3400 9300
	1    0    0    -1  
$EndComp
$Comp
L williamson:D_V D3
U 1 1 5A1CF9E8
P 3800 9300
F 0 "D3" H 3870 9280 50  0000 L CNN
F 1 "1N4148" H 3870 9360 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 3800 9300 50  0001 C CNN
F 3 "~" H 3800 9300 50  0001 C CNN
	1    3800 9300
	1    0    0    -1  
$EndComp
$Comp
L williamson:D_V D4
U 1 1 54786C4B
P 4200 9300
F 0 "D4" H 4270 9280 50  0000 L CNN
F 1 "1N4148" H 4270 9360 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 4200 9300 50  0001 C CNN
F 3 "~" H 4200 9300 50  0001 C CNN
	1    4200 9300
	1    0    0    -1  
$EndComp
$Comp
L williamson:D_V D5
U 1 1 537F5CDD
P 4600 9300
F 0 "D5" H 4670 9280 50  0000 L CNN
F 1 "1N4148" H 4670 9360 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62_V" H 4600 9300 50  0001 C CNN
F 3 "~" H 4600 9300 50  0001 C CNN
	1    4600 9300
	1    0    0    -1  
$EndComp
Wire Wire Line
	1200 3000 1450 3000
Wire Wire Line
	1750 3000 2000 3000
Wire Wire Line
	2000 2000 2000 3000
Wire Wire Line
	1200 2000 2000 2000
Wire Wire Line
	2000 1800 2000 2000
Wire Wire Line
	2000 1800 3500 1800
Wire Wire Line
	3500 1800 3500 2000
Wire Wire Line
	3300 2000 3500 2000
Wire Wire Line
	3300 2200 3600 2200
Wire Wire Line
	3600 2200 3750 2200
Wire Wire Line
	4050 2200 4950 2200
Wire Wire Line
	4950 2200 5100 2200
Wire Wire Line
	3600 2200 3600 2550
Wire Wire Line
	3600 2550 4900 2550
Wire Wire Line
	4900 2550 4900 2700
Wire Wire Line
	4700 2700 4900 2700
Wire Wire Line
	4700 2900 4950 2900
Wire Wire Line
	4950 2200 4950 2900
Wire Wire Line
	1200 4500 1450 4500
Wire Wire Line
	1750 4500 2000 4500
Wire Wire Line
	2000 4300 2000 4500
Wire Wire Line
	2000 4300 3300 4300
Wire Wire Line
	3300 4300 3300 4500
Wire Wire Line
	3100 4500 3300 4500
Wire Wire Line
	3100 4700 3300 4700
Wire Wire Line
	3300 4700 3300 4900
Wire Wire Line
	3100 4900 3300 4900
Wire Wire Line
	3100 5100 3500 5100
Wire Wire Line
	3500 5100 3750 5100
Wire Wire Line
	3500 5100 3500 5450
Wire Wire Line
	3500 5450 4900 5450
Wire Wire Line
	4900 5450 4900 5600
Wire Wire Line
	4700 5600 4900 5600
Wire Wire Line
	4700 5800 5000 5800
Wire Wire Line
	5000 5100 5000 5800
Wire Wire Line
	4050 5100 5000 5100
Wire Wire Line
	5000 5100 5200 5100
Wire Wire Line
	5200 5100 5400 5100
Wire Wire Line
	5200 5100 5200 5500
Wire Wire Line
	5200 5500 5400 5500
Wire Wire Line
	1200 7000 1450 7000
Wire Wire Line
	1750 7000 2050 7000
Wire Wire Line
	2050 7000 2300 7000
Wire Wire Line
	2050 7000 2050 7400
Wire Wire Line
	2050 7400 2300 7400
Wire Wire Line
	7650 2000 8200 2000
Wire Wire Line
	8200 2000 8200 2100
Wire Wire Line
	8200 3000 8650 3000
Wire Wire Line
	8200 2000 9200 2000
Wire Wire Line
	9200 2000 9200 2100
Wire Wire Line
	8200 3300 8200 3400
Wire Wire Line
	9200 3000 9200 3100
Wire Wire Line
	8500 3800 8650 3800
Wire Wire Line
	8500 3800 8500 4100
Wire Wire Line
	8500 4100 8650 4100
Wire Wire Line
	8500 4100 8500 4200
Wire Wire Line
	1200 2100 1300 2100
Wire Wire Line
	1200 3100 1300 3100
Wire Wire Line
	2400 2100 2500 2100
Wire Wire Line
	2400 2200 2500 2200
Wire Wire Line
	3300 2400 3400 2400
Wire Wire Line
	3300 2600 3400 2600
Wire Wire Line
	5000 2300 5100 2300
Wire Wire Line
	3800 2800 3900 2800
Wire Wire Line
	3800 2900 3900 2900
Wire Wire Line
	4700 3100 4800 3100
Wire Wire Line
	4700 3300 4800 3300
Wire Wire Line
	1200 4600 1300 4600
Wire Wire Line
	2200 4600 2300 4600
Wire Wire Line
	2200 4700 2300 4700
Wire Wire Line
	3800 5700 3900 5700
Wire Wire Line
	3800 5800 3900 5800
Wire Wire Line
	4700 6000 4800 6000
Wire Wire Line
	4700 6200 4800 6200
Wire Wire Line
	5300 5200 5400 5200
Wire Wire Line
	5300 5600 5400 5600
Wire Wire Line
	1200 7100 1300 7100
Wire Wire Line
	2200 7100 2300 7100
Wire Wire Line
	2200 7500 2300 7500
Wire Wire Line
	8200 2400 8200 2500
Wire Wire Line
	8200 2700 8200 2800
Wire Wire Line
	9200 2400 9200 2500
Wire Wire Line
	9200 2700 9200 2800
Wire Wire Line
	2200 8950 2300 8950
Wire Wire Line
	2200 9050 2300 9050
Wire Wire Line
	2200 9150 2300 9150
Wire Wire Line
	2200 9550 2300 9550
Wire Wire Line
	2200 9650 2300 9650
Wire Wire Line
	2200 9750 2300 9750
Wire Wire Line
	3400 9450 3400 9550
Wire Wire Line
	3400 9050 3400 9150
Wire Wire Line
	3800 9450 3800 9550
Wire Wire Line
	3800 9050 3800 9150
Wire Wire Line
	4200 9450 4200 9550
Wire Wire Line
	4200 9050 4200 9150
Wire Wire Line
	4600 9450 4600 9550
Wire Wire Line
	4600 9050 4600 9150
Connection ~ 2000 2000
Connection ~ 3600 2200
Connection ~ 4950 2200
Connection ~ 3500 5100
Connection ~ 5000 5100
Connection ~ 5200 5100
Connection ~ 2050 7000
Connection ~ 8200 2000
Connection ~ 8200 3000
Connection ~ 8500 4100
Connection ~ 8200 2400
Connection ~ 8200 2700
Connection ~ 9200 2400
Connection ~ 9200 2700
Text Label 3300 2000 0    50   ~ 0
L_SW
Text Label 3300 2200 0    50   ~ 0
L_K1
Text Label 4700 2700 0    50   ~ 0
L_K1
Text Label 4700 2900 0    50   ~ 0
L_TR
Text Label 4700 5600 0    50   ~ 0
HT_K3
Text Label 4700 5800 0    50   ~ 0
HT_IN
Text Label 8200 3400 3    50   ~ 0
GND
Text Label 9200 3100 3    50   ~ 0
GND
Text Label 8500 4200 3    50   ~ 0
GND
Text Label 1300 2100 0    50   ~ 0
N_SW
Text Label 1300 3100 0    50   ~ 0
N_SW
Text Label 2400 2100 2    50   ~ 0
+12V
Text Label 2400 2200 2    50   ~ 0
RLY1
Text Label 3400 2400 0    50   ~ 0
L_SW
Text Label 3400 2600 0    50   ~ 0
L_K1
Text Label 5000 2300 2    50   ~ 0
N_SW
Text Label 3800 2800 2    50   ~ 0
+12V
Text Label 3800 2900 2    50   ~ 0
RLY2
Text Label 4800 3100 0    50   ~ 0
L_K1
Text Label 4800 3300 0    50   ~ 0
L_TR
Text Label 1300 4600 0    50   ~ 0
HT_B
Text Label 2200 4600 2    50   ~ 0
+12V
Text Label 2200 4700 2    50   ~ 0
RLY3
Text Label 3800 5700 2    50   ~ 0
+12V
Text Label 3800 5800 2    50   ~ 0
RLY4
Text Label 4800 6000 0    50   ~ 0
HT_K3
Text Label 4800 6200 0    50   ~ 0
HT_IN
Text Label 5300 5200 2    50   ~ 0
HT_B
Text Label 5300 5600 2    50   ~ 0
HT_B
Text Label 1300 7100 0    50   ~ 0
B_AC2
Text Label 2200 7100 2    50   ~ 0
B_AC2
Text Label 2200 7500 2    50   ~ 0
B_AC2
Text Label 8200 2500 3    50   ~ 0
HVS1
Text Label 8200 2800 3    50   ~ 0
HVS2
Text Label 9200 2500 3    50   ~ 0
LED_M
Text Label 9200 2800 3    50   ~ 0
LED_A
Text Label 2200 8950 2    50   ~ 0
+12V
Text Label 2200 9050 2    50   ~ 0
RLY1
Text Label 2200 9150 2    50   ~ 0
RLY2
Text Label 2200 9550 2    50   ~ 0
+12V
Text Label 2200 9650 2    50   ~ 0
RLY3
Text Label 2200 9750 2    50   ~ 0
RLY4
Text Label 3400 9550 3    50   ~ 0
RLY1
Text Label 3400 9050 1    50   ~ 0
+12V
Text Label 3800 9550 3    50   ~ 0
RLY2
Text Label 3800 9050 1    50   ~ 0
+12V
Text Label 4200 9550 3    50   ~ 0
RLY3
Text Label 4200 9050 1    50   ~ 0
+12V
Text Label 4600 9550 3    50   ~ 0
RLY4
Text Label 4600 9050 1    50   ~ 0
+12V
Text Notes 800 1500 0    60   ~ 16
230 V: F1 T2,5A w gniezdzie IEC i wylacznik poza plytka -> J1
Text Notes 800 1620 0    60   ~ 16
K1 wlacza TR1 przez R_SS 47R, po 1,5 s K2 zwiera R_SS
Text Notes 5750 2300 0    60   ~ 16
J5: pierwotne TR1
Text Notes 300 3350 0    60   ~ 16
J3: PS1 IRM-15-12 (czuwanie)
Text Notes 800 4000 0    60   ~ 16
Anody: S1 360 V (odczepy 345/375 V) -> F3 -> K3 (2 styki szeregowo, +45 s) -> R_IN -> K4 (+1,5 s)
Text Notes 800 4120 0    60   ~ 16
-> AC na mostki Onyxa J103 / J203. Prostowniki, filtry i dlawiki 10 H sa na plytce Onyxa.
Text Notes 5900 5000 0    60   ~ 16
J8 -> Onyx J103
Text Notes 5900 5400 0    60   ~ 16
J9 -> Onyx J203
Text Notes 800 6600 0    60   ~ 16
Bias: S4 58 V -> F4 -> AC na mostki biasu Onyxa J106 / J206 (ok. -80 V)
Text Notes 2900 7000 0    60   ~ 16
J11 -> Onyx J106
Text Notes 2900 7400 0    60   ~ 16
J12 -> Onyx J206
Text Notes 7300 1600 0    60   ~ 16
Pomiar Ua i LED HV z Ua-L plytki Onyxa (plus C121)
Text Notes 9100 3300 0    60   ~ 16
J14 HV_SENSE -> sterowanie J5-2 (ok. 2,3 V przy 465 V)
Text Notes 8900 3700 0    60   ~ 16
J15 masa do plytki Onyxa, J18 masa do sterowania
Text Notes 9700 2950 0    60   ~ 16
LED HV: NIE ZASTEPUJE MIERNIKA
Text Notes 800 8600 0    60   ~ 16
Cewki K1-K4 ze sterowania J2: J16 = piny 1,2,3; J17 = piny 1,4,5
Text Notes 800 10400 0    60   ~ 16
Zarzenie (S2 6,3 V/8 A, S3 6,3 V/3 A) idzie z TR1 wprost na Onyx J105/J205 i J104/J204, poza ta plytka.
Text Notes 800 10520 0    60   ~ 16
Zarzenie KT88 ma odniesienie do masy na plytce Onyxa (UaFF-L2), R11/R12 niepotrzebne.
NoConn ~ 3300 2100
NoConn ~ 3300 2500
NoConn ~ 4700 2800
NoConn ~ 4700 3200
NoConn ~ 3100 4600
NoConn ~ 3100 5000
NoConn ~ 4700 5700
NoConn ~ 4700 6100
$EndSCHEMATC
