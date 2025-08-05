import cv2
import numpy as np
from datetime import datetime

class SmartParkingSystem:
    def __init__(self):
        self.current_sessions = {}  # Store active parking sessions
        self.parking_rates = {
            'first_hour': 50,
            'additional_hour': 30
        }

    def capture_image(self):
        """Capture image from webcam"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return None

        print("Capturing image... Look at the camera.")
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()

        return frame if ret else None

    def process_face(self, frame):
        """Basic face detection using Haar Cascade"""
        if frame is None:
            return None

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            print("No face detected.")
            return None

        # Return coordinates of the first detected face
        return faces[0]

    def login(self):
        """Handle parking entry"""
        print("\n=== VEHICLE ENTRY ===")

        frame = self.capture_image()
        face = self.process_face(frame)

        if face is None:
            print("Face detection failed. Try again.")
            return

        name = input("Enter your name: ")
        vehicle_number = input("Enter vehicle number: ").upper()

        entry_time = datetime.now()
        session_id = f"{vehicle_number}_{entry_time.strftime('%Y%m%d%H%M%S')}"

        self.current_sessions[session_id] = {
            'name': name,
            'vehicle_number': vehicle_number,
            'entry_time': entry_time,
            'face_coordinates': face.tolist()
        }

        print("\n✅ Entry recorded!")
        print(f"Session ID: {session_id}")
        print(f"Entry Time: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return session_id

    def logout(self):
        """Handle parking exit"""
        print("\n=== VEHICLE EXIT ===")

        frame = self.capture_image()
        current_face = self.process_face(frame)

        if current_face is None:
            print("Face detection failed. Try again.")
            return

        vehicle_number = input("Enter vehicle number: ").upper()

        matching_session = None
        session_id = None

        for sid, session in self.current_sessions.items():
            if session['vehicle_number'] == vehicle_number:
                matching_session = session
                session_id = sid
                break

        if matching_session is None:
            print("❌ No matching session found.")
            return

        stored_face = np.array(matching_session['face_coordinates'])
        if np.linalg.norm(stored_face - current_face) > 100:  # Face mismatch
            print("❌ Face verification failed. Contact parking attendant.")
            return

        exit_time = datetime.now()
        duration = exit_time - matching_session['entry_time']
        hours = duration.total_seconds() / 3600

        if hours <= 1:
            charges = self.parking_rates['first_hour']
        else:
            charges = self.parking_rates['first_hour'] + \
                      self.parking_rates['additional_hour'] * int(hours - 1)

        print("\n=== PARKING BILL ===")
        print(f"Name: {matching_session['name']}")
        print(f"Vehicle Number: {matching_session['vehicle_number']}")
        print(f"Entry Time: {matching_session['entry_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Exit Time: {exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {int(hours)} hours {int((hours % 1) * 60)} minutes")
        print(f"Charges: ₹{charges}")

        # Remove session
        del self.current_sessions[session_id]

        return charges

def main():
    parking_system = SmartParkingSystem()

    while True:
        print("\n=== SMART PARKING SYSTEM ===")
        print("1. Vehicle Entry")
        print("2. Vehicle Exit")
        print("3. Exit Program")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            parking_system.login()
        elif choice == '2':
            parking_system.logout()
        elif choice == '3':
            print("Thank you for using Smart Parking System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

