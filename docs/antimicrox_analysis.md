# AntiMicroX Architecture Analysis

**Purpose**: Analysis of AntiMicroX for macOS controller mapping patterns applicable to Karabiner-Elements

**Repository**: https://github.com/AntiMicroX/antimicrox

---

## Executive Summary

AntiMicroX is a mature C++/Qt application for mapping gamepad inputs to keyboard/mouse events on Linux and Windows. While macOS support is absent, the architecture provides valuable patterns for controller mapping systems. This analysis extracts learnable patterns for our Karabiner-based Xbox controller setup.

**Key Takeaway**: AntiMicroX's layered architecture (SDL input -> device abstraction -> event translation -> platform output) is a reference design, but Karabiner's approach of intercepting at the HID level is fundamentally different and likely more robust for macOS.

---

## 1. Overall Architecture

AntiMicroX follows a clean **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                         Qt GUI Layer                             │
│         (Profile management, button configuration UI)            │
├─────────────────────────────────────────────────────────────────┤
│                    InputDevice Abstraction                       │
│  (Unified device model: buttons, axes, sticks, sensors, dpads)  │
├─────────────────────────────────────────────────────────────────┤
│                     SDL Event Reader                             │
│      (Timer-based polling, event queue monitoring)               │
├─────────────────────────────────────────────────────────────────┤
│                   Platform Event Handlers                        │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│    │   uinput     │  │   XTest      │  │  SendInput   │         │
│    │   (Linux)    │  │   (X11)      │  │  (Windows)   │         │
│    └──────────────┘  └──────────────┘  └──────────────┘         │
├─────────────────────────────────────────────────────────────────┤
│                    Operating System                              │
│              (Kernel input subsystem / WinAPI)                   │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

1. **Factory Pattern for Platform Handlers**: `AntKeyMapper` acts as a facade, delegating to platform-specific backends based on compile-time configuration.

2. **Template Method Pattern**: `BaseEventHandler` provides abstract interface with no-op defaults; child classes implement platform-specific behavior.

3. **Singleton Pattern**: Key mapper instances are lazily initialized with compile-time validation of handler availability.

4. **Observer Pattern**: Qt signals propagate input events (`clicked`, `released`, `rawButtonClick`) through the system.

---

## 2. Controller Input Handling

### SDL2 Integration

AntiMicroX uses **SDL2 (Simple DirectMedia Layer)** for cross-platform controller input:

```cpp
// From sdleventreader.cpp - Event detection via polling
void SDLEventReader::performWork() {
    if (eventStatus()) {
        pollRateTimer.stop();
        emit eventRaised();  // Signal higher-level handlers
    }
}

// Non-destructive event queue inspection
bool SDLEventReader::eventStatus() {
    return SDL_PeepEvents(nullptr, 0, SDL_PEEKEVENT,
                          SDL_FIRSTEVENT, SDL_LASTEVENT) > 0;
}
```

**Key insight**: SDL handles controller detection, button enumeration, axis mapping, and hat switch support. AntiMicroX focuses on the mapping logic rather than raw HID parsing.

### Controller Identification

Controllers are identified via SDL's GUID system plus an additional unique identifier:

```cpp
// From inputdevice.cpp - Device identification
QString uniqueId = SDL_JoystickGetDeviceGUID(deviceIndex);
int vendorId = SDL_JoystickGetVendorID(joystick);
int productId = SDL_JoystickGetProductID(joystick);
```

The project also loads a `gamecontrollerdb.txt` file with mappings for hundreds of controllers:

```
# SDL2 Game Controller Database format:
GUID,name,mapping_string
030000005e040000e002000000000000,Xbox Wireless Controller,a:b0,b:b1,back:b6...
```

**Karabiner equivalent**: Karabiner uses vendor_id + product_id + device_id for controller identification, similar in concept.

---

## 3. Event Mapping Mechanism

### Device Abstraction Model

The `InputDevice` class provides a unified model for all controller types:

```cpp
// Abstraction handles multiple input types
class InputDevice {
    // Physical inputs
    QList<JoyButton*> buttons;
    QList<JoyAxis*> axes;
    QList<JoyDPad*> dpads;
    QList<JoyControlStick*> sticks;

    // Modern controller features
    JoyGyroscopeSensor* gyroscope;
    JoyAccelerometerSensor* accelerometer;
    HapticTriggerPS5* hapticTrigger;

    // Configuration
    QList<SetJoystick*> sets;  // Multiple switchable profiles
};
```

### Set-Based Configuration

A distinctive feature is **multiple configuration sets per controller** (up to 8):

```cpp
// Switch between input sets at runtime
void InputDevice::setActiveSetNumber(int index) {
    // Preserve button states during transition
    // Handle "set change" conditions
    // Transfer axis/dpad values to new set
}
```

**Karabiner equivalent**: Karabiner's "profiles" and "layers" provide similar functionality. Our current setup uses single-layer mappings.

### Event Translation Flow

```
Controller Input
      │
      ▼
┌─────────────────┐
│ SDL Event Queue │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  InputDevice    │ ← Axis dead zones, calibration
│  Processing     │   Button debouncing, turbo
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Slot System    │ ← Maps input to action type:
│                 │   keyboard, mouse, script, hold
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Platform Handler│ ← Generates OS-level events
└─────────────────┘
```

---

## 4. Platform-Specific Event Generation

### Linux: uinput Kernel Interface

The most sophisticated handler uses Linux's uinput for kernel-level event injection:

```cpp
// From uinputeventhandler.cpp
void UInputEventHandler::write_uinput_event(int type, int code, int value) {
    struct input_event event;
    gettimeofday(&event.time, nullptr);
    event.type = type;
    event.code = code;
    event.value = value;

    write(uinputFd, &event, sizeof(event));

    // Synchronization event required
    event.type = EV_SYN;
    event.code = SYN_REPORT;
    write(uinputFd, &event, sizeof(event));
}

// Keyboard key press
void UInputEventHandler::sendKeyboardEvent(int keycode, bool pressed) {
    write_uinput_event(EV_KEY, keycode, pressed ? 1 : 0);
}

// Relative mouse movement
void UInputEventHandler::sendMouseEvent(int deltaX, int deltaY) {
    write_uinput_event(EV_REL, REL_X, deltaX);
    write_uinput_event(EV_REL, REL_Y, deltaY);
}
```

**Key insight**: uinput creates virtual input devices at the kernel level, indistinguishable from real hardware. This is the gold standard for input injection on Linux.

### Windows: SendInput API

Windows uses the user-mode SendInput API:

```cpp
// Conceptual Windows implementation
void WinEventHandler::sendKeyboardEvent(int virtualKey, bool pressed) {
    INPUT input = {0};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = virtualKey;
    input.ki.dwFlags = pressed ? 0 : KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
}
```

### macOS: CGEvent (Theoretical)

Based on research, a macOS implementation would use CGEvent:

```swift
// What macOS support WOULD look like (not implemented in AntiMicroX)
func sendKeyboardEvent(keyCode: CGKeyCode, pressed: Bool) {
    guard let event = CGEvent(keyboardEventSource: nil,
                               virtualKey: keyCode,
                               keyDown: pressed) else { return }
    event.post(tap: .cghidEventTap)  // Requires Accessibility permission
}

func sendMouseEvent(deltaX: Int32, deltaY: Int32) {
    let currentPos = CGEvent(source: nil)?.location ?? .zero
    guard let event = CGEvent(mouseEventSource: nil,
                               mouseType: .mouseMoved,
                               mouseCursorPosition: CGPoint(x: currentPos.x + CGFloat(deltaX),
                                                           y: currentPos.y + CGFloat(deltaY)),
                               mouseButton: .left) else { return }
    event.post(tap: .cghidEventTap)
}
```

---

## 5. Why macOS Support Was Never Implemented

### Official Status

- **Issue #455** (June 2022): Open request for macOS support, marked "help from outside needed"
- **Issue #24** (original antimicro): "Currently, there are no plans to support AntiMicro on OSX. I don't have the hardware or the time."
- **CMakeLists.txt**: Explicitly excludes macOS: `if(UNIX AND NOT APPLE...`

### Technical Challenges

1. **No uinput equivalent**: macOS lacks a kernel-level virtual input device mechanism comparable to Linux's uinput.

2. **CGEvent Accessibility requirements**: Input injection requires explicit user permission, adding UX friction.

3. **Sandboxing restrictions**: Modern macOS apps face significant restrictions on system-level input manipulation.

4. **Different controller frameworks**: macOS uses GameController.framework, not SDL's native path (though SDL can use it under the hood).

5. **Developer resources**: The maintainers explicitly stated "it would require a macOS developer" - a resource they don't have.

### Abandoned Work

A `macos_attempt` branch exists but contains incomplete work. The antimicrox.net website claims macOS support with DMG downloads, but this appears to be unofficial/community-maintained and not reflected in the main repository.

---

## 6. Configuration File Format

AntiMicroX uses XML-based profile files with `.amgp` extension:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gamecontroller configversion="15" appversion="2.11">
  <!-- Device identification -->
  <sdlname>Xbox Controller</sdlname>
  <guid>030000005e040000e002000000000000</guid>
  <profilename>My Xbox Profile</profilename>

  <sets>
    <set index="1">
      <!-- Analog sticks with 8-way directional buttons -->
      <stick index="1">
        <stickbutton index="1">  <!-- Up -->
          <slots>
            <slot>
              <code>0x57</code>   <!-- 'W' key -->
              <mode>keyboard</mode>
            </slot>
          </slots>
        </stickbutton>
        <!-- indices 3,5,7 for Right, Down, Left -->
      </stick>

      <!-- D-pad with 4 or 8-way mode -->
      <dpad index="1" mode="eight-way">
        <dpadbutton index="1">   <!-- Up = 0x0001 -->
          <slots>
            <slot>
              <code>0x31</code>  <!-- '1' key -->
              <mode>keyboard</mode>
            </slot>
          </slots>
        </dpadbutton>
        <!-- indices 2,4,8 for Right, Down, Left -->
      </dpad>

      <!-- Triggers with half/full press detection -->
      <trigger index="1">
        <triggerbutton index="2">
          <slots>
            <slot>
              <code>1</code>     <!-- Left mouse button -->
              <mode>mousebutton</mode>
            </slot>
          </slots>
        </triggerbutton>
      </trigger>

      <!-- Face buttons -->
      <button index="1">        <!-- A button -->
        <slots>
          <slot>
            <code>0x20</code>   <!-- Space -->
            <mode>keyboard</mode>
          </slot>
        </slots>
      </button>
    </set>
  </sets>
</gamecontroller>
```

### Slot Mode Types

| Mode | Description | Code Format |
|------|-------------|-------------|
| `keyboard` | Keyboard key | Hex keycode (0x20 = Space) |
| `mousebutton` | Mouse button | 1=Left, 2=Middle, 3=Right |
| `mousemovement` | Mouse axis | Direction + speed |
| `cycle` | Cycle through actions | Sequence definition |
| `hold` | Hold until release | Key + duration |
| `delay` | Wait before action | Milliseconds |
| `execute` | Run script/command | Path string |

### Comparison to Karabiner JSON

| Feature | AntiMicroX (XML) | Karabiner (JSON) |
|---------|------------------|------------------|
| Format | XML with nested elements | JSON with flat manipulators |
| Sets/Layers | `<set index>` elements | Separate rules/profiles |
| Key codes | Hex keycodes | Named key_code strings |
| Conditions | Per-slot modifiers | conditions[] array |
| Scripts | `<execute>` with path | shell_command string |

---

## 7. Reusable Patterns for Karabiner

### Pattern 1: Layered Architecture

AntiMicroX's separation of input detection, device abstraction, mapping logic, and output generation is clean. Our Karabiner setup could benefit from similar conceptual layers:

```
┌───────────────────────────────────────────────┐
│ Documentation Layer (cheatsheet, references)  │
├───────────────────────────────────────────────┤
│ Mapping Configuration (JSON files)            │
├───────────────────────────────────────────────┤
│ Karabiner-Elements (HID interception)         │
├───────────────────────────────────────────────┤
│ macOS HID Driver                              │
└───────────────────────────────────────────────┘
```

### Pattern 2: Controller Identification

AntiMicroX uses GUID + vendor/product for robust identification. Our Karabiner config already does this:

```json
// From xbox_zed_claude.json
"conditions": [{
    "type": "device_if",
    "identifiers": [{
        "vendor_id": 1118,     // Microsoft
        "product_id": 2835,    // Xbox Controller
        "is_pointing_device": true
    }]
}]
```

### Pattern 3: Multi-Set Configuration

AntiMicroX's switchable sets could inspire app-specific profiles in Karabiner:

```json
// Potential pattern: Different mappings per app
{
    "conditions": [{
        "type": "frontmost_application_if",
        "bundle_identifiers": ["^dev\\.zed\\..*$"]
    }],
    "manipulators": [/* Zed-specific mappings */]
}
```

### Pattern 4: Dead Zone and Calibration

AntiMicroX handles stick dead zones and calibration. Currently, we rely on macOS defaults, but Karabiner does support thresholds:

```json
// D-pad/stick threshold handling (conceptual)
"from": {
    "pointing_button": "button4",
    "modifiers": { "optional": ["any"] }
}
```

### Pattern 5: Profile Organization

AntiMicroX organizes profiles by: `applications/APP_NAME/CONTROLLER_GUID/PROFILE.amgp`

Our equivalent structure:
```
mods/
├── keyboard_text_shortcuts.json    # Caps+key shortcuts
├── xbox_zed_claude.json           # Xbox controller (global)
└── dictation_toggle.json          # SuperWhisper integration
```

---

## 8. Key Differences: AntiMicroX vs Karabiner

| Aspect | AntiMicroX | Karabiner-Elements |
|--------|------------|-------------------|
| **Input Layer** | SDL (user-space) | HID (driver-level) |
| **Output Method** | Event injection (uinput/SendInput) | Virtual keyboard driver |
| **Controller Support** | SDL gamepad database | Direct HID device matching |
| **Mapping Types** | Keyboard, mouse, scripts | Any HID event |
| **Profile Storage** | XML files in app directory | JSON in ~/.config/karabiner |
| **GUI** | Qt application | Preferences app + JSON |
| **D-pad Handling** | SDL hat events | generic_desktop events |

**Critical difference**: Karabiner intercepts at the HID driver level, making it fundamentally more integrated with macOS. AntiMicroX's SDL+injection approach would require Accessibility permissions and feel "bolted on."

---

## 9. Recommendations for Our Setup

### Keep Using Karabiner

Karabiner's approach is architecturally superior for macOS:
- Native HID interception (no permission prompts)
- Virtual keyboard driver (events indistinguishable from hardware)
- Active macOS support and updates

### Adopt Documentation Patterns

Create structured documentation similar to AntiMicroX's wiki:
- Button mapping reference (done: `xbox_button_reference.md`)
- Per-application profiles (consider for complex setups)
- Troubleshooting guide (for D-pad issues, etc.)

### Consider Profile Switching

AntiMicroX's multi-set feature could be emulated with Karabiner profiles or conditional layers based on frontmost application.

### Monitor SDL's macOS Support

If we ever need features Karabiner doesn't support (analog stick curve adjustment, complex macros), SDL2 does work on macOS for input reading. We could build a hybrid: SDL for input detection, CGEvent for output.

---

## 10. References

- **AntiMicroX Repository**: https://github.com/AntiMicroX/antimicrox
- **SDL2 Game Controller Database**: https://github.com/gabomdq/SDL_GameControllerDB
- **macOS CGEvent Documentation**: https://developer.apple.com/documentation/coregraphics/cgevent
- **Karabiner-Elements**: https://karabiner-elements.pqrs.org/
- **Apple GameController Framework**: https://developer.apple.com/documentation/gamecontroller

---

*Analysis completed: January 2026*
