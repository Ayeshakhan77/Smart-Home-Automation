# Smart-Home-Automation
# 🏠 Smart Home Automation System

A **console-based Python project** that simulates a **Smart Home Automation System** using multiple **Behavioral Design Patterns**.  
This project demonstrates the application of **Observer, Command, Strategy, and Composite Patterns** with **hardcoded values** for simplicity.

---

## 🎯 Overview

This project models a **smart home environment** where devices like **lights, fans, and thermostats** can be controlled.  
The system highlights how **design patterns** make software more modular, reusable, and easier to extend.

---
## 🛠️ Behavioral Patterns Implemented

1. **Observer Pattern** – Devices notify observers (e.g., User App) when their state changes.  
2. **Command Pattern** – Encapsulates requests and provides **Undo/Redo** functionality for device actions.  
3. **Chain of Responsibility Pattern** – Escalates requests (e.g., security alert passing from Sensor → Hub → User).  
4. **Mediator Pattern** – Devices communicate indirectly via a central **Smart Hub**.  
5. **Memento Pattern** – Saves and restores the state of devices (e.g., thermostat settings).  
6. **State Pattern** – Device behavior changes based on its state (e.g., Light: ON, OFF, DIM).  
7. **Strategy Pattern** – Multiple strategies for controlling devices (e.g., Manual, Scheduled, Eco Mode).  
8. **Interpreter Pattern** – Provides a skeleton for device operations, allowing customization of steps.  
 
---

## 📊 UML Diagrams

- **Class Diagram** – Defines relationships between system classes.  
- **Sequence Diagram** – Illustrates device operation flows.  

---

## 💻 Backend Logic

The system is written in **a single Python file** with hardcoded values.  
All actions and outputs are **console-based**.

### Example – Observer Pattern

[Notification] Living Room Light -> ON

### Example – Command Pattern (Undo/Redo)

[Notification] Living Room Light -> OFF
[Notification] Living Room Light -> ON (after undo)

## 🚀 How to Run

1. Install **Python 3.x**  
2. Clone this repository :  https://github.com/Ayeshakhan77/Smart-Home-Automation
3. Run the program:
   ```bash
   python smart_home.py
View the console outputs

