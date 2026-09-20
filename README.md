# 🚌 Goa Express - Bus Reservation System

An end-to-end Bus Reservation System built in Python with both a Terminal (CLI) interface and a modern Single-Page Web Application (SPA).

---

## 🌟 Features

- **Route Discovery**: Filter buses connecting Goa towns (Panaji, Margao, Vasco, Mapusa, etc.) with intra-state locations and outstation destinations (Mumbai, Pune, Bangalore, Hyderabad, etc.).
- **Interactive Seat Layout**: Realistic 4-column coach view (`Window | Aisle | Walking Aisle | Aisle | Window`) with live seat status indicators (Available, Selected, Reserved).
- **Seat Booking & Fare Calculation**: Dynamic fare computation supporting Seater and Sleeper coach multiplier rates.
- **Digital Boarding Pass**: Instant digital boarding pass generation with unique booking ID.
- **Booking Management**: Search existing reservations by **Booking ID**, **Phone Number**, or **Passenger Name**.
- **Partial & Full Cancellation**: Cancel individual or multiple seats with automatic total fare recalculation.
- **Bus Occupancy Analytics**: Real-time seat occupancy reporting and progress tracking for operators.
- **Data Persistence**: Automatic daily schedule rollover and JSON file-based database storage.

---

## 📁 Project Structure

```
BusReservationSystem/
├── data/                                 # JSON Data Files
│   ├── buses_YYYY-MM-DD.json
│   └── reservations_YYYY-MM-DD.json
├── models/                               # Domain Models
│   ├── bus.py                            # Bus class and seat layout logic
│   ├── reservation.py                    # Reservation data model
│   ├── seat.py                           # Seat status and booking methods
│   └── user.py                           # Passenger data model
├── services/                             # Core Business Services
│   ├── bus_generator.py                  # Procedural bus schedule generator
│   ├── file_manager.py                   # JSON persistence manager
│   └── reservation_system.py             # Business logic & CLI operations
├── utils/                                # Constants & Custom Exceptions
│   ├── constants.py                      # Routes, operators, fare tiers
│   └── exceptions.py                     # Custom domain exceptions
├── web/                                  # 🚀 Web Application
│   ├── static/
│   │   ├── css/style.css                 # Modern responsive CSS
│   │   └── js/app.js                     # Frontend interactive controller
│   ├── templates/
│   │   └── index.html                    # Single-Page App (SPA) template
│   └── app.py                            # Flask server and REST APIs
├── requirements.txt                      # Project dependencies
├── run_web.py                            # Web app launcher
├── main.py                               # Terminal CLI launcher
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites & Installation

```bash
# Clone the repository
git clone https://github.com/ArnavNKamat/Bus-Reservation-System.git
cd Bus-Reservation-System

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Launch the Web Application

```bash
python run_web.py
```

Then open your browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

### 3. Run the Terminal (CLI) Application

```bash
python main.py
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Flask-CORS
- **Frontend**: HTML5, Vanilla Modern CSS, Vanilla JavaScript (ES6+)
- **Storage**: JSON File Database (`data/`)

---

## 📄 License

Developed as a Python Capstone Project by Arnav Kamat.
