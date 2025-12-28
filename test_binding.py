#!/usr/bin/env python3
"""Test binding procedure with MATSON Monitor."""
import asyncio
from bleak import BleakClient, BleakScanner

MATSON_ADDRESS = "52375622-4547-E20B-B992-FD703C98FE5E"

# Track notifications
notifications_received = []

def notification_handler(sender: int, data: bytearray):
    """Handle BLE notifications."""
    print(f"\n📩 Notification from handle {sender}:")
    print(f"   Hex: {data.hex()}")
    print(f"   Bytes: {list(data)}")
    try:
        decoded = data.decode('utf-8', errors='ignore')
        if decoded and decoded.isprintable():
            print(f"   String: '{decoded}'")
    except:
        pass
    notifications_received.append((sender, data))


async def test_binding():
    """Test binding with MATSON Monitor."""
    print(f"Attempting to connect to MATSON Monitor at {MATSON_ADDRESS}...")
    
    try:
        # Find device
        print("Scanning for device...")
        device = await BleakScanner.find_device_by_address(MATSON_ADDRESS, timeout=10.0)
        
        if not device:
            print("❌ Device not found during scan!")
            print("\nTroubleshooting:")
            print("1. Ensure device is powered on")
            print("2. Close any apps connected to the device")
            print("3. Try resetting the device")
            return
        
        print(f"✓ Found device: {device.name or 'Unknown'}")
        print(f"\nAttempting connection...")
        
        async with BleakClient(device, timeout=30.0) as client:
            print(f"✓ Connected successfully!")
            
            # Discover services
            print("\n" + "="*70)
            print("Discovering services and characteristics...")
            print("="*70)
            
            notify_chars = []
            write_chars = []
            
            for service in client.services:
                print(f"\n[SERVICE] {service.uuid}")
                
                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"  [CHAR] {char.uuid}")
                    print(f"    Properties: {props}")
                    
                    if "notify" in char.properties or "indicate" in char.properties:
                        notify_chars.append(char)
                    if "write" in char.properties or "write-without-response" in char.properties:
                        write_chars.append(char)
            
            # Enable notifications on all notify-capable characteristics
            print("\n" + "="*70)
            print("Attempting to enable notifications (binding)...")
            print("="*70)
            
            for char in notify_chars:
                try:
                    print(f"\n📡 Enabling notifications on {char.uuid}...")
                    await client.start_notify(char.uuid, notification_handler)
                    print(f"   ✓ Notifications enabled successfully")
                except Exception as e:
                    print(f"   ❌ Failed to enable: {e}")
            
            # Wait for any immediate notifications
            print("\n⏳ Waiting for notifications (5 seconds)...")
            await asyncio.sleep(5)
            
            # Try reading characteristics
            print("\n" + "="*70)
            print("Attempting to read characteristics...")
            print("="*70)
            
            for service in client.services:
                for char in service.characteristics:
                    if "read" in char.properties:
                        try:
                            print(f"\n📖 Reading {char.uuid}...")
                            value = await client.read_gatt_char(char.uuid)
                            print(f"   Hex: {value.hex()}")
                            print(f"   Bytes: {list(value)}")
                            if len(value) <= 20:
                                try:
                                    decoded = value.decode('utf-8', errors='ignore').strip('\x00')
                                    if decoded and decoded.isprintable():
                                        print(f"   String: '{decoded}'")
                                except:
                                    pass
                        except Exception as e:
                            print(f"   ❌ Read failed: {e}")
            
            # Show write characteristics for manual testing
            if write_chars:
                print("\n" + "="*70)
                print("Write-capable characteristics (for binding commands):")
                print("="*70)
                for char in write_chars:
                    print(f"  {char.uuid} - {char.properties}")
                    print(f"    To test binding, try writing to this characteristic")
            
            # Wait for more notifications
            print("\n⏳ Waiting for additional notifications (10 seconds)...")
            await asyncio.sleep(10)
            
            # Summary
            print("\n" + "="*70)
            print("BINDING TEST SUMMARY")
            print("="*70)
            print(f"✓ Connection successful")
            print(f"✓ Notifications enabled on {len(notify_chars)} characteristic(s)")
            print(f"✓ Total notifications received: {len(notifications_received)}")
            
            if notifications_received:
                print("\nNotifications received:")
                for i, (handle, data) in enumerate(notifications_received, 1):
                    print(f"  {i}. Handle {handle}: {data.hex()}")
            
            print("\n💡 Next steps:")
            print("1. Update MATSON_CHARACTERISTIC_NOTIFY_UUID in const.py with notify UUID")
            print("2. If binding command needed, update MATSON_BINDING_COMMAND")
            print("3. The coordinator will auto-enable notifications on connect")
            print("="*70)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Troubleshooting tips:")
        print("1. Ensure no other app is connected to the device")
        print("2. Try closing the official Matson app if running")
        print("3. Power cycle the MATSON Monitor")
        print("4. Check if device requires app-based authorization first")


if __name__ == "__main__":
    asyncio.run(test_binding())
