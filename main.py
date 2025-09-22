# Smart Home Automation
from abc import ABC, abstractmethod
import copy

print("\n===== SMART HOME AUTOMATION SYSTEM =====\n")

# ---------------------------
# OBSERVER (notify user app)
# ---------------------------
class Observer(ABC):
    @abstractmethod
    def update(self, msg): pass

class UserApp(Observer):
    def update(self, msg): print(f"[Notification] {msg}")

class Device:
    def __init__(self, name):
        self.name = name
        self.state = "OFF"
        self.observers = []
    
    def add_observer(self, obs):
        if obs not in self.observers:
            self.observers.append(obs)
    
    def remove_observer(self, obs):
        if obs in self.observers:
            self.observers.remove(obs)
    
    def set_state(self, state):
        old_state = self.state
        self.state = state
        if old_state != state:
            for o in self.observers: 
                o.update(f"{self.name} -> {self.state}")

# Create device and observer
light = Device("Living Room Light")
user_app = UserApp()
light.add_observer(user_app)
print("Observer Pattern:")
light.set_state("ON")
print()

# ---------------------------
# COMMAND (undo/redo)
# ---------------------------
class Command(ABC):
    def __init__(self, device):
        self.device = device
        self.previous_state = None
    
    @abstractmethod
    def execute(self): pass
    
    @abstractmethod
    def undo(self): pass

class TurnOnCommand(Command):
    def execute(self):
        self.previous_state = self.device.state
        self.device.set_state("ON")
    
    def undo(self):
        if self.previous_state:
            self.device.set_state(self.previous_state)

class TurnOffCommand(Command):
    def execute(self):
        self.previous_state = self.device.state
        self.device.set_state("OFF")
    
    def undo(self):
        if self.previous_state:
            self.device.set_state(self.previous_state)

class CommandHistory:
    def __init__(self):
        self.history = []
        self.redo_stack = []
    
    def execute_command(self, command):
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()
    
    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)
    
    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)

print("Command Pattern:")
history = CommandHistory()
turn_off = TurnOffCommand(light)
history.execute_command(turn_off)
history.undo()  # Should turn light back ON
print()

# ---------------------------
# STATE (Fan Speeds)
# ---------------------------
class FanState(ABC):
    @abstractmethod
    def press(self, fan): pass

class OffState(FanState):
    def press(self, fan):
        fan.set_state(LowState())
        return "LOW"

class LowState(FanState):
    def press(self, fan):
        fan.set_state(MediumState())
        return "MEDIUM"

class MediumState(FanState):
    def press(self, fan):
        fan.set_state(HighState())
        return "HIGH"

class HighState(FanState):
    def press(self, fan):
        fan.set_state(OffState())
        return "OFF"

class Fan:
    def __init__(self):
        self.state = OffState()
    
    def set_state(self, state):
        self.state = state
    
    def press_button(self):
        result = self.state.press(self)
        print(f"Fan -> {result}")

print("State Pattern:")
fan = Fan()
for _ in range(5):
    fan.press_button()
print()

# ---------------------------
# STRATEGY (Scheduling)
# ---------------------------
class SchedulingStrategy(ABC):
    @abstractmethod
    def run(self, device): pass

class TimedStrategy(SchedulingStrategy):
    def run(self, device):
        print(f"{device.name} turns ON at 7 PM")

class SensorStrategy(SchedulingStrategy):
    def run(self, device):
        print(f"{device.name} turns ON if motion detected")

class Scheduler:
    def __init__(self, strategy: SchedulingStrategy = None):
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def apply(self, device):
        if self.strategy:
            self.strategy.run(device)

print("Strategy Pattern:")
scheduler = Scheduler(TimedStrategy())
scheduler.apply(light)
scheduler.set_strategy(SensorStrategy())
scheduler.apply(light)
print()

# ---------------------------
# MEDIATOR (Hub connects devices)
# ---------------------------
class SmartHomeHub:
    def __init__(self):
        self.devices = {}
    
    def register_device(self, name, device):
        self.devices[name] = device
        print(f"Registered {name}")
    
    def send_command(self, device_name, command, *args):
        if device_name in self.devices:
            device = self.devices[device_name]
            if command == "turn_on":
                device.set_state("ON")
            elif command == "turn_off":
                device.set_state("OFF")
            else:
                print(f"Unknown command: {command}")
        else:
            print(f"Device {device_name} not found")

print("Mediator Pattern:")
hub = SmartHomeHub()
hub.register_device("living_room_light", light)
hub.send_command("living_room_light", "turn_on")
print()

# ---------------------------
# MEMENTO (Save/Restore config)
# ---------------------------
class DeviceMemento:
    def __init__(self, state):
        self.state = state
class DeviceCaretaker:
    def __init__(self, device):
        self.device = device
        self.saved_states = []
    def save_state(self):
        memento = DeviceMemento(self.device.state)
        self.saved_states.append(memento)
        print(f"Config saved: {memento.state}")
        return memento
    
    def restore_state(self, index=-1):
        if self.saved_states:
            memento = self.saved_states[index]
            self.device.state = memento.state
            print(f"Config restored -> {memento.state}")
        else:
            print("No saved states to restore")

print("Memento Pattern:")
caretaker = DeviceCaretaker(light)
caretaker.save_state()
light.set_state("OFF")
caretaker.restore_state()
print()

# ---------------------------
# INTERPRETER (parse command)
# ---------------------------
class CommandInterpreter:
    def interpret(self, command_text, device):
        command_text = command_text.lower().strip()
        
        if "turn on" in command_text or "switch on" in command_text:
            device.set_state("ON")
            return f"Turning {device.name} ON"
        elif "turn off" in command_text or "switch off" in command_text:
            device.set_state("OFF")
            return f"Turning {device.name} OFF"
        elif "toggle" in command_text:
            new_state = "OFF" if device.state == "ON" else "ON"
            device.set_state(new_state)
            return f"Toggling {device.name} to {new_state}"
        else:
            return "Command not recognized"

print("Interpreter Pattern:")
interpreter = CommandInterpreter()
commands = ["turn on light", "turn off light", "toggle light"]
for cmd in commands:
    result = interpreter.interpret(cmd, light)
    print(f"'{cmd}' -> {result}")
print()

# ---------------------------
# CHAIN OF RESPONSIBILITY (Alerts)
# ---------------------------
class AlertHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler   
    @abstractmethod
    def handle_alert(self, alert_level, message): pass
class MotionHandler(AlertHandler):
    def handle_alert(self, alert_level, message):
        if alert_level == "motion":
            print(f"Motion detected! {message}")
        elif self.next_handler:
            self.next_handler.handle_alert(alert_level, message)
class AlarmHandler(AlertHandler):
    def handle_alert(self, alert_level, message):
        if alert_level == "alarm":
            print(f"Alarm triggered! {message}")
        elif self.next_handler:
            self.next_handler.handle_alert(alert_level, message)
class PoliceHandler(AlertHandler):
    def handle_alert(self, alert_level, message):
        if alert_level == "police":
            print(f"Police notified! {message}")
        elif self.next_handler:
            self.next_handler.handle_alert(alert_level, message)
print("Chain of Responsibility Pattern:")
# Build the chain
police_handler = PoliceHandler()
alarm_handler = AlarmHandler(police_handler)
motion_handler = MotionHandler(alarm_handler)
# Test different alert levels
alerts = [
    ("motion", "Movement in living room"),
    ("alarm", "Intrusion detected"),
    ("police", "Emergency situation"),
    ("unknown", "Test message")
]
for level, message in alerts:
    print(f"Alert level: {level}")
    motion_handler.handle_alert(level, message)
    print()






