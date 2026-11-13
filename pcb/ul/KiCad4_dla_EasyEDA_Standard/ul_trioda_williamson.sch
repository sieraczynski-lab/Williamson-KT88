EESchema Schematic File Version 2
LIBS:williamson
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Williamson KT88 - przelacznik UL/trioda, 4x KT88 na jednej plytce"
Date ""
Rev "0.4"
Comp ""
Comment1 "Soloist 88 Stereo"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONNR_3 J1
U 1 1 5A91B54A
P 1200 2100
F 0 "J1" H 1100 1810 50  0000 L CNN
F 1 "LAMPA_V5" H 1100 1890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x03_P7.62_V" H 1200 2100 50  0001 C CNN
F 3 "" H 1200 2100 50  0001 C CNN
	1    1200 2100
	1    0    0    -1  
$EndComp
$Comp
L RELAY_G2RL K1
U 1 1 538A840B
P 3800 2200
F 0 "K1" H 3550 1690 50  0000 L CNN
F 1 "G2RL-2-DC12" H 3550 1770 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 3800 2200 50  0001 C CNN
F 3 "" H 3800 2200 50  0001 C CNN
F 4 "LCSC" H 3800 2200 50  0001 C CNN "Supplier"
F 5 "C61458" H 3800 2200 50  0001 C CNN "Supplier Part"
	1    3800 2200
	1    0    0    -1  
$EndComp
$Comp
L CONNR_3 J2
U 1 1 5398E4F0
P 1200 3900
F 0 "J2" H 1100 3610 50  0000 L CNN
F 1 "LAMPA_V6" H 1100 3690 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x03_P7.62_V" H 1200 3900 50  0001 C CNN
F 3 "" H 1200 3900 50  0001 C CNN
	1    1200 3900
	1    0    0    -1  
$EndComp
$Comp
L RELAY_G2RL K2
U 1 1 5A83D5B1
P 3800 4000
F 0 "K2" H 3550 3490 50  0000 L CNN
F 1 "G2RL-2-DC12" H 3550 3570 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 3800 4000 50  0001 C CNN
F 3 "" H 3800 4000 50  0001 C CNN
F 4 "LCSC" H 3800 4000 50  0001 C CNN "Supplier"
F 5 "C61458" H 3800 4000 50  0001 C CNN "Supplier Part"
	1    3800 4000
	1    0    0    -1  
$EndComp
$Comp
L CONNR_3 J3
U 1 1 549FD466
P 6200 2100
F 0 "J3" H 6100 1810 50  0000 L CNN
F 1 "LAMPA_V7" H 6100 1890 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x03_P7.62_V" H 6200 2100 50  0001 C CNN
F 3 "" H 6200 2100 50  0001 C CNN
	1    6200 2100
	1    0    0    -1  
$EndComp
$Comp
L RELAY_G2RL K3
U 1 1 5D84E527
P 8800 2200
F 0 "K3" H 8550 1690 50  0000 L CNN
F 1 "G2RL-2-DC12" H 8550 1770 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 8800 2200 50  0001 C CNN
F 3 "" H 8800 2200 50  0001 C CNN
F 4 "LCSC" H 8800 2200 50  0001 C CNN "Supplier"
F 5 "C61458" H 8800 2200 50  0001 C CNN "Supplier Part"
	1    8800 2200
	1    0    0    -1  
$EndComp
$Comp
L CONNR_3 J4
U 1 1 5AFB41C5
P 6200 3900
F 0 "J4" H 6100 3610 50  0000 L CNN
F 1 "LAMPA_V8" H 6100 3690 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x03_P7.62_V" H 6200 3900 50  0001 C CNN
F 3 "" H 6200 3900 50  0001 C CNN
	1    6200 3900
	1    0    0    -1  
$EndComp
$Comp
L RELAY_G2RL K4
U 1 1 53E07084
P 8800 4000
F 0 "K4" H 8550 3490 50  0000 L CNN
F 1 "G2RL-2-DC12" H 8550 3570 50  0000 L CNN
F 2 "williamson:Relay_DPDT_Omron_G2RL" H 8800 4000 50  0001 C CNN
F 3 "" H 8800 4000 50  0001 C CNN
F 4 "LCSC" H 8800 4000 50  0001 C CNN "Supplier"
F 5 "C61458" H 8800 4000 50  0001 C CNN "Supplier Part"
	1    8800 4000
	1    0    0    -1  
$EndComp
$Comp
L CONNR_2 J5
U 1 1 5DFC7153
P 1200 6200
F 0 "J5" H 1100 5960 50  0000 L CNN
F 1 "CEWKI" H 1100 6040 50  0000 L CNN
F 2 "williamson:TerminalBlock_1x02_P5.08" H 1200 6200 50  0001 C CNN
F 3 "" H 1200 6200 50  0001 C CNN
	1    1200 6200
	1    0    0    -1  
$EndComp
$Comp
L D_V D1
U 1 1 541298C4
P 3000 6200
F 0 "D1" H 3070 6180 50  0000 L CNN
F 1 "1N4148" H 3070 6260 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62" H 3000 6200 50  0001 C CNN
F 3 "" H 3000 6200 50  0001 C CNN
	1    3000 6200
	1    0    0    -1  
$EndComp
$Comp
L D_V D2
U 1 1 5D1BC97E
P 3600 6200
F 0 "D2" H 3670 6180 50  0000 L CNN
F 1 "1N4148" H 3670 6260 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62" H 3600 6200 50  0001 C CNN
F 3 "" H 3600 6200 50  0001 C CNN
	1    3600 6200
	1    0    0    -1  
$EndComp
$Comp
L D_V D3
U 1 1 5A1CF9E8
P 4200 6200
F 0 "D3" H 4270 6180 50  0000 L CNN
F 1 "1N4148" H 4270 6260 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62" H 4200 6200 50  0001 C CNN
F 3 "" H 4200 6200 50  0001 C CNN
	1    4200 6200
	1    0    0    -1  
$EndComp
$Comp
L D_V D4
U 1 1 54786C4B
P 4800 6200
F 0 "D4" H 4870 6180 50  0000 L CNN
F 1 "1N4148" H 4870 6260 50  0000 L CNN
F 2 "williamson:D_DO-35_P7.62" H 4800 6200 50  0001 C CNN
F 3 "" H 4800 6200 50  0001 C CNN
	1    4800 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 5900 3000 6050
Wire Wire Line
	3000 5900 3600 5900
Wire Wire Line
	3600 5900 3900 5900
Wire Wire Line
	3900 5900 4200 5900
Wire Wire Line
	4200 5900 4800 5900
Wire Wire Line
	4800 5900 4800 6050
Wire Wire Line
	3000 6350 3000 6500
Wire Wire Line
	3000 6500 3600 6500
Wire Wire Line
	3600 6500 3900 6500
Wire Wire Line
	3900 6500 4200 6500
Wire Wire Line
	4200 6500 4800 6500
Wire Wire Line
	4800 6350 4800 6500
Wire Wire Line
	3600 5900 3600 6050
Wire Wire Line
	3600 6350 3600 6500
Wire Wire Line
	4200 5900 4200 6050
Wire Wire Line
	4200 6350 4200 6500
Wire Wire Line
	3900 5800 3900 5900
Wire Wire Line
	3900 6500 3900 6600
Wire Wire Line
	1500 2000 1600 2000
Wire Wire Line
	1500 2100 1600 2100
Wire Wire Line
	1500 2200 1600 2200
Wire Wire Line
	3300 2000 3400 2000
Wire Wire Line
	3300 2100 3400 2100
Wire Wire Line
	4200 1900 4300 1900
Wire Wire Line
	4200 2000 4300 2000
Wire Wire Line
	4200 2100 4300 2100
Wire Wire Line
	4200 2300 4300 2300
Wire Wire Line
	4200 2400 4300 2400
Wire Wire Line
	4200 2500 4300 2500
Wire Wire Line
	1500 3800 1600 3800
Wire Wire Line
	1500 3900 1600 3900
Wire Wire Line
	1500 4000 1600 4000
Wire Wire Line
	3300 3800 3400 3800
Wire Wire Line
	3300 3900 3400 3900
Wire Wire Line
	4200 3700 4300 3700
Wire Wire Line
	4200 3800 4300 3800
Wire Wire Line
	4200 3900 4300 3900
Wire Wire Line
	4200 4100 4300 4100
Wire Wire Line
	4200 4200 4300 4200
Wire Wire Line
	4200 4300 4300 4300
Wire Wire Line
	6500 2000 6600 2000
Wire Wire Line
	6500 2100 6600 2100
Wire Wire Line
	6500 2200 6600 2200
Wire Wire Line
	8300 2000 8400 2000
Wire Wire Line
	8300 2100 8400 2100
Wire Wire Line
	9200 1900 9300 1900
Wire Wire Line
	9200 2000 9300 2000
Wire Wire Line
	9200 2100 9300 2100
Wire Wire Line
	9200 2300 9300 2300
Wire Wire Line
	9200 2400 9300 2400
Wire Wire Line
	9200 2500 9300 2500
Wire Wire Line
	6500 3800 6600 3800
Wire Wire Line
	6500 3900 6600 3900
Wire Wire Line
	6500 4000 6600 4000
Wire Wire Line
	8300 3800 8400 3800
Wire Wire Line
	8300 3900 8400 3900
Wire Wire Line
	9200 3700 9300 3700
Wire Wire Line
	9200 3800 9300 3800
Wire Wire Line
	9200 3900 9300 3900
Wire Wire Line
	9200 4100 9300 4100
Wire Wire Line
	9200 4200 9300 4200
Wire Wire Line
	9200 4300 9300 4300
Wire Wire Line
	1500 6150 1600 6150
Wire Wire Line
	1500 6250 1600 6250
Connection ~ 3600 5900
Connection ~ 3900 5900
Connection ~ 4200 5900
Connection ~ 3600 6500
Connection ~ 3900 6500
Connection ~ 4200 6500
Text Label 3900 5800 1    50   ~ 0
+12V
Text Label 3900 6600 3    50   ~ 0
RLY_UL
Text Label 1600 2000 0    50   ~ 0
AN_V5
Text Label 1600 2100 0    50   ~ 0
UL_V5
Text Label 1600 2200 0    50   ~ 0
G2_V5
Text Label 3300 2000 2    50   ~ 0
+12V
Text Label 3300 2100 2    50   ~ 0
RLY_UL
Text Label 4300 1900 0    50   ~ 0
G2_V5
Text Label 4300 2000 0    50   ~ 0
UL_V5
Text Label 4300 2100 0    50   ~ 0
AN_V5
Text Label 4300 2300 0    50   ~ 0
G2_V5
Text Label 4300 2400 0    50   ~ 0
UL_V5
Text Label 4300 2500 0    50   ~ 0
AN_V5
Text Label 1600 3800 0    50   ~ 0
AN_V6
Text Label 1600 3900 0    50   ~ 0
UL_V6
Text Label 1600 4000 0    50   ~ 0
G2_V6
Text Label 3300 3800 2    50   ~ 0
+12V
Text Label 3300 3900 2    50   ~ 0
RLY_UL
Text Label 4300 3700 0    50   ~ 0
G2_V6
Text Label 4300 3800 0    50   ~ 0
UL_V6
Text Label 4300 3900 0    50   ~ 0
AN_V6
Text Label 4300 4100 0    50   ~ 0
G2_V6
Text Label 4300 4200 0    50   ~ 0
UL_V6
Text Label 4300 4300 0    50   ~ 0
AN_V6
Text Label 6600 2000 0    50   ~ 0
AN_V7
Text Label 6600 2100 0    50   ~ 0
UL_V7
Text Label 6600 2200 0    50   ~ 0
G2_V7
Text Label 8300 2000 2    50   ~ 0
+12V
Text Label 8300 2100 2    50   ~ 0
RLY_UL
Text Label 9300 1900 0    50   ~ 0
G2_V7
Text Label 9300 2000 0    50   ~ 0
UL_V7
Text Label 9300 2100 0    50   ~ 0
AN_V7
Text Label 9300 2300 0    50   ~ 0
G2_V7
Text Label 9300 2400 0    50   ~ 0
UL_V7
Text Label 9300 2500 0    50   ~ 0
AN_V7
Text Label 6600 3800 0    50   ~ 0
AN_V8
Text Label 6600 3900 0    50   ~ 0
UL_V8
Text Label 6600 4000 0    50   ~ 0
G2_V8
Text Label 8300 3800 2    50   ~ 0
+12V
Text Label 8300 3900 2    50   ~ 0
RLY_UL
Text Label 9300 3700 0    50   ~ 0
G2_V8
Text Label 9300 3800 0    50   ~ 0
UL_V8
Text Label 9300 3900 0    50   ~ 0
AN_V8
Text Label 9300 4100 0    50   ~ 0
G2_V8
Text Label 9300 4200 0    50   ~ 0
UL_V8
Text Label 9300 4300 0    50   ~ 0
AN_V8
Text Label 1600 6150 0    50   ~ 0
+12V
Text Label 1600 6250 0    50   ~ 0
RLY_UL
Text Notes 800 1000 0    60   ~ 16
Przelacznik UL / trioda Williamson KT88 - jedna plytka, 4 x KT88 (V5, V6 kanal L; V7, V8 kanal P)
Text Notes 800 1120 0    60   ~ 16
Cewka bez zasilania: G2 <- odczep UL (NC, tryb UL). Cewka 12 V: G2 <- anoda (NO, trioda).
Text Notes 800 1240 0    60   ~ 16
PRZELACZAC TYLKO PRZY WYLACZONYCH ANODACH (ESP32: K3/K4 off, czekaj na Ua < 30 V, przelacz, start).
Text Notes 800 1360 0    60   ~ 16
J1..J4: 1 anoda toroidu (i J101-1/-5 Onyxa), 2 odczep UL toroidu, 3 do J101-2/-4 Onyxa (G2 przez R125/R126).
Text Notes 800 1700 0    60   ~ 16
KANAL L
Text Notes 5800 1700 0    60   ~ 16
KANAL P
Text Notes 800 7000 0    60   ~ 16
J5: ze sterowania J11 piny 1-2 (+12 V, RLY_UL); piny 3-4 J11 wolne
$EndSCHEMATC
