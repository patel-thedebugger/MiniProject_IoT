import pytest
import serial
import time

# Serial port configuration — change to match your ESP32's port
ESP32_PORT = "COM6"       # On Linux/Mac, e.g., "/dev/ttyUSB0"
BAUD_RATE = 115200
TIMEOUT = 5  # seconds

@pytest.fixture(scope="module")
def esp32_serial():
    """Fixture to open and close serial connection to ESP32."""
    try:
        ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Wait for ESP32 reset after connection
        yield ser
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def test_esp32_output(esp32_serial):
    """Test that ESP32 sends expected output."""
    output_lines = []
    start_found = False

    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        line = esp32_serial.readline().decode(errors="ignore").strip()
        if not line:
            continue

        if line == "TEST_START":
            start_found = True
            output_lines.clear()
            continue
        elif line == "TEST_END":
            break
        elif start_found:
            output_lines.append(line)

    # Assertions
    assert start_found, "ESP32 did not send TEST_START"
    assert "ESP32 is working" in output_lines, "LED status not ON"
