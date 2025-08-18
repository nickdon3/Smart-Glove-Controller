# 🧤 Smart-Glove RC Car Controller

This project is a **glove-based control system** I built for an RC car, combining embedded hardware, sensors, and custom Python code. Instead of using the car’s original remote, I reverse-engineered the wiring and integrated a custom control interface powered by an **Adafruit Feather M4 microcontroller**.  

By blending gesture recognition, motion sensing, and light-based speed adjustment, the glove turns natural hand movements into driving commands — making RC car driving feel more futuristic and intuitive.  

---

## ⚙️ How It Works
- **Hand Gestures**  
  - Making a **fist** → Forward motion  
  - Wrist **rotations** → Steer left or right  

- **Sensors Used**  
  - **LSM6DSOX accelerometer**: Measures X/Y motion for steering.  
  - **Two APDS-9960 proximity/gesture sensors**: Detect hand movements and adjust speed dynamically.  
  - **Optical sensor for headlights**: Automatically turns headlights on in low-light conditions.  

- **Motor Control**  
  - Implemented with **voltage-based commands**:  
    - `3.3V` → Forward motion
    - `1.65V` → Stationary
    - `0V` → Reverse  
    - Proportional voltages → Left/Right steering  

---

## Development Process
1. Reverse-engineered the original RC car controller by stripping and analyzing wiring.  
2. Prototyped the circuit on a breadboard before embedding sensors into the glove.  
3. Wrote custom Python code to control multiple sensors and the Feather M4.  
4. Tested and calibrated sensor responses for smooth steering and speed control.  
5. Installed permanent wiring into the car for a fully integrated Smart-Glove system.  

---

## Hardware
- **Adafruit Feather M4 microcontroller**  
- **LSM6DSOX accelerometer**  
- **APDS-9960 gesture/proximity sensors (x2)**  
- **Custom wiring harness** (reverse-engineered from stock controller)  
- **RC Car with headlights**

---

##  Software
- Written in **Python**, running on the Feather M4.  
- Sensor libraries sourced from [Adafruit’s examples](https://learn.adafruit.com/).  
- Modified and combined to create a unified Smart-Glove control interface.  


