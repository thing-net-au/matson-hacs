#!/usr/bin/env python3
"""Direct connection test for MATSON Monitor."""
import asyncio
from bleak import BleakClient, BleakScanner

MATSON_ADDRESS = "52375622-4547-E20B-B992-FD703C98FE5E"

async def connect_to_matson():
    """Connect to MATSON Monitor and read services."""
    print(f"Attempting to connect to MATSON Monitor at {MATSON_ADDRESS}...")
    
    try:
        # Try to find the device first
        print("Scanning for device...")
        device = await BleakScanner.find_device_by_address(MATSON_ADDRESS, timeout=10.0)
        
        if not device:
            print("Device not found during scan!")
            return
        
        print(f"Found device: {device.name or 'Unknown'}")
        print(f"Attempting connection with longer timeout...")
        
        async with BleakClient(device, timeout=30.0) as client:
            print(f"✓ Connected successfully!")
            print(f"Is connected: {client.is_connected}")
            
            # Get services
            print("\nDiscovering services...")
            services = client.services
            
            print(f"\n{'='*70}")
            print(f"MATSON Monitor - Services and Characteristics")
            print(f"{'='*70}")
            
            for service in services:
                print(f"\n[SERVICE] {service.uuid}")
                print(f"  Handle: {service.handle}")
                if service.description != "Unknown":
                    print(f"  Description: {service.description}")
                
                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"\n  [CHARACTERISTIC] {char.uuid}")
                    print(f"    Handle: {char.handle}")
                    if char.description != "Unknown":
                        print(f"    Description: {char.description}")
                    print(f"    Properties: {props}")
                    
                    # Try to read
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(f"    ✓ Read successful!")
                            print(f"      Hex: {value.hex()}")
                            print(f"      Bytes: {list(value)}")
                            print(f"      Length: {len(value)} bytes")
                            
                            # Try string decode
                            try:
                                decoded = value.decode('utf-8', errors='ignore').strip('\x00')
                                if decoded and decoded.isprintable():
                                    print(f"      String: '{decoded}'")
                            except:
                                pass
                            
                            # Try numeric interpretations
                            if len(value) == 1:
                                print(f"      uint8: {value[0]}")
                                print(f"      int8: {int.from_bytes(value, 'little', signed=True)}")
                            elif len(value) == 2:
                                print(f"      uint16 (LE): {int.from_bytes(value, 'little')}")
                                print(f"      int16 (LE): {int.from_bytes(value, 'little', signed=True)}")
                            elif len(value) == 4:
                                print(f"      uint32 (LE): {int.from_bytes(value, 'little')}")
                                print(f"      int32 (LE): {int.from_bytes(value, 'little', signed=True)}")
                                import struct
                                print(f"      float (LE): {struct.unpack('<f', value)[0]:.2f}")
                                
                        except Exception as e:
                            print(f"    ✗ Read failed: {e}")
                    
                    # Check if notify/indicate available
                    if "notify" in char.properties or "indicate" in char.properties:
                        print(f"    ℹ Supports notifications/indications")
                    
                    # Show descriptors
                    if char.descriptors:
                        for desc in char.descriptors:
                            print(f"      [DESCRIPTOR] {desc.uuid}")
                            try:
                                desc_value = await client.read_gatt_descriptor(desc.handle)
                                print(f"        Value: {desc_value.hex()}")
                            except:
                                pass
            
            print(f"\n{'='*70}")
            print("Connection successful! Use these UUIDs in const.py")
            print(f"{'='*70}\n")
            
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(connect_to_matson())
