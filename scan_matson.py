#!/usr/bin/env python3
"""Scan for Matson Monitor BLE devices and display their services."""
import asyncio
import sys
from bleak import BleakScanner, BleakClient


async def scan_devices():
    """Scan for Matson devices and display their details."""
    print("Scanning for Matson devices (10 seconds)...")
    print("-" * 60)
    
    devices = await BleakScanner.discover(timeout=10.0)
    
    # Filter for Matson devices (or show all if none found)
    matson_devices = [d for d in devices if d.name and "Matson" in d.name]
    
    if not matson_devices:
        print("\nNo devices with 'Matson' in the name found.")
        print("\nAll discovered devices:")
        for device in devices:
            rssi = getattr(device, 'rssi', 'N/A')
            print(f"  {device.name or 'Unknown'} ({device.address}) - RSSI: {rssi} dBm")
        
        response = input("\nWould you like to inspect a specific device? Enter address or 'n': ")
        if response.lower() == 'n':
            return
        
        target_device = next((d for d in devices if d.address.lower() == response.lower()), None)
        if not target_device:
            print(f"Device {response} not found!")
            return
        matson_devices = [target_device]
    
    for device in matson_devices:
        print(f"\n{'='*60}")
        print(f"Device: {device.name or 'Unknown'}")
        print(f"Address: {device.address}")
        rssi = getattr(device, 'rssi', 'N/A')
        print(f"RSSI: {rssi} dBm")
        print(f"{'='*60}")
        
        try:
            print("\nConnecting...")
            async with BleakClient(device.address, timeout=15.0) as client:
                print(f"✓ Connected to {device.name or device.address}")
                print(f"\nServices and Characteristics:")
                print("-" * 60)
                
                for service in client.services:
                    print(f"\n[SERVICE] {service.uuid}")
                    if service.description != "Unknown":
                        print(f"  Description: {service.description}")
                    
                    for char in service.characteristics:
                        properties = ", ".join(char.properties)
                        print(f"\n  [CHAR] {char.uuid}")
                        if char.description != "Unknown":
                            print(f"    Description: {char.description}")
                        print(f"    Properties: {properties}")
                        
                        # Try to read if readable
                        if "read" in char.properties:
                            try:
                                value = await client.read_gatt_char(char.uuid)
                                print(f"    Value (hex): {value.hex()}")
                                print(f"    Value (bytes): {list(value)}")
                                
                                # Try to decode as string
                                try:
                                    decoded = value.decode('utf-8', errors='ignore').strip('\x00')
                                    if decoded:
                                        print(f"    Value (string): {decoded}")
                                except:
                                    pass
                                
                                # Try to interpret as integers
                                if len(value) == 1:
                                    print(f"    Value (uint8): {value[0]}")
                                elif len(value) == 2:
                                    print(f"    Value (uint16_le): {int.from_bytes(value, 'little')}")
                                    print(f"    Value (uint16_be): {int.from_bytes(value, 'big')}")
                                elif len(value) == 4:
                                    print(f"    Value (uint32_le): {int.from_bytes(value, 'little')}")
                                    print(f"    Value (float_le): {float(int.from_bytes(value, 'little'))}")
                                    
                            except Exception as e:
                                print(f"    ✗ Could not read: {e}")
                        
                        # Show descriptors
                        if char.descriptors:
                            for desc in char.descriptors:
                                print(f"      [DESC] {desc.uuid}")
                
                print("\n" + "="*60)
                print("Connection successful! Use these UUIDs in const.py")
                print("="*60)
                
        except Exception as e:
            print(f"\n✗ Error connecting to {device.name or device.address}: {e}")
            print(f"  Make sure the device is not connected to another app")


def main():
    """Main entry point."""
    try:
        asyncio.run(scan_devices())
    except KeyboardInterrupt:
        print("\n\nScan cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
