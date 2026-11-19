#pragma once
// Przydzial pinow plytki "sterowanie" (docs/10, rozdz. 2.1 i 2.2)

namespace pins {
constexpr int I2C_SDA = 8;
constexpr int I2C_SCL = 9;

// Wyjscia na ULN2803 (stan wysoki = cewka zalaczona)
constexpr int RLY_K1 = 10;     // K1: siec przez R_SS (zarzenie, bias)
constexpr int RLY_K2 = 11;     // K2: bypass R_SS
constexpr int RLY_K3 = 12;     // K3: anody przez R_IN
constexpr int RLY_K4 = 13;     // K4: bypass R_IN
constexpr int RLY_SOUND = 14;  // J3 -> K11 selektora (wariant 7.5b): aktywne = DZWIEK
constexpr int RLY_UL = 17;     // J11: 4 przekazniki UL/trioda, aktywne = trioda, bez pradu = UL
constexpr int RLY_SPK = 18;    // J13: kolumny, aktywne = lampa, bez pradu = Marantz

constexpr int TRIG_IN = 1;     // transoptor, 0 = 12 V triggera obecne
constexpr int ONEWIRE = 4;     // DS18B20 (etap 2)
constexpr int IR_RX = 5;       // TSOP38238 (etap 4)
constexpr int ENC_VOL_A = 6;   // enkoder glosnosci (etap 4)
constexpr int ENC_VOL_B = 7;
constexpr int ENC_VOL_SW = 15;
constexpr int BTN_POWER = 16;  // przycisk wlacz / czuwanie, zalozenie: zwiera do masy (sprawdzic na plytce)

// Nowe, prawa listwa DevKitC (etap 4 / 6)
constexpr int ENC_SEL_A = 21;
constexpr int ENC_SEL_B = 47;
constexpr int ENC_SEL_SW = 48;  // albo 38, zalezy od wersji DevKitC (dioda RGB)
constexpr int VU_L = 2;         // ADC1
constexpr int VU_R = 3;         // ADC1, strapping JTAG
}  // namespace pins
