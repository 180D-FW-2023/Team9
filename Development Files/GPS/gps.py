from geopy.geocoders import Nominatim
import serial
import time

gps_serial = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)

geolocator = Nominatim(user_agent = "gps_example")

try:
	while True:
		gps_data = gps_serial.readline().decode('utf-8', errors='ignore').strip()
		
		if 'GPGGA' in gps_data or 'GNGGA' in gps_data:
			
			fields = gps_data.split(',')
			
			if fields[2][:2] == '':
				print("No connection")
				break
				
			latitude = float(fields[2][:2]) + float(fields[2][2:]) / 60.0
			longitude = float(fields[4][:3]) + float(fields[4][3:]) / 60.0
			longitude = -longitude
			
			if -90 <= latitude <= 90 and -180 <= longitude <= 180:
				
				location = geolocator.reverse((latitude, longitude), language = 'en')
				
				address = location.address
				city = location.raw.get('address', {}).get('city', 'N/A')
				
				print(f"Latitude: {latitude}, Longitude: {longitude}")
				print(f"Address: {address}")
				print(f"City: {city}")
				
				time.sleep(5)
			print(f"GPS Data: {gps_data}")
			
except KeyboardInterrupt:
	print("Program terminated by Jarbisss")
	
finally:
	gps_serial.close()
