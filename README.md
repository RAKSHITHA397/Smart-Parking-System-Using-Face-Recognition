# Smart Parking System Using Face Recognition

A Python-based smart parking system that uses **face recognition** to automate vehicle entry and exit, calculate parking duration, and generate charges — all using a **webcam**.

---

# Features

- 🎥 Captures face image using webcam
- 🧠 Detects faces using OpenCV Haar cascades
- 🕐 Records entry and exit times
- 🧾 Automatically calculates parking charges
- 🔒 Verifies face on exit to avoid misuse

---

# How It Works

1. **Vehicle Entry**:
   - Captures face using webcam
   - Stores name, vehicle number, face data & entry time

2. **Vehicle Exit**:
   - Captures face again
   - Verifies it's the same person using Euclidean distance
   - Calculates time spent and charges:
     - ₹50 for first hour
     - ₹30 per additional hour
   - Prints a parking bill

---

# Technologies Used

- Python
- OpenCV
- NumPy
- datetime module

---

# How to Run

### 1. Install dependencies:

```bash
pip install opencv-python numpy
