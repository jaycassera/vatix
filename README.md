# 🚨 Vatix Backend Assignment - "Where Are My People?"

A Django-based backend system to manage users, SOS tracking devices, and real-time location pings.

---

## 📦 Features

- Track **users** and their **SOS devices**
- Devices can only be assigned to one user at a time
- Users can only have one active device
- Devices send location pings when assigned
- Query for latest known locations
- See full device list and assignment status
- Filter map data by user or device

---

## 🛠 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/where-are-my-people.git
cd where-are-my-people
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create test data

```bash
python manage.py shell
```

```python
from tracker.models import User, SOSDevice

u1 = User.objects.create(name="Alice")
u2 = User.objects.create(name="Bob")

d1 = SOSDevice.objects.create(device_id="DEV001")
d2 = SOSDevice.objects.create(device_id="DEV002")
exit()
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### `GET /devices/`

List all devices and their current assignment status.

**Response:**

```json
[
  {
    "device_id": "DEV001",
    "assigned_user": {
      "id": 1,
      "name": "Alice"
    }
  },
  ...
]
```

---

### `POST /devices/<id>/assign/`

Assign a device to a user. Automatically unassigns other conflicting links.

**Payload:**

```json
{ "user_id": 1 }
```

---

### `POST /devices/<id>/unassign/`

Unassigns the device from the user.

**Response:**

```json
{ "message": "Device unassigned" }
```

---

### `POST /devices/<id>/location/`

Send a location ping (only allowed if device is assigned).

**Payload:**

```json
{
  "latitude": 51.509865,
  "longitude": -0.118092,
  "ping_time": "2025-05-12T12:30:00Z"
}
```

---

### `GET /users/<id>/location/`

Get last known location of the user based on their assigned device.

**Response:**

```json
{
  "latitude": 51.509865,
  "longitude": -0.118092,
  "timestamp": "2025-05-12T12:30:00Z"
}
```

---

### `GET /map/`

Get the latest known locations of all **currently assigned** devices.

**Optional Query Parameters:**

- `user_id` — filter by user
- `device_id` — filter by device

**Response:**

```json
[
  {
    "user": { "id": 1, "name": "Alice" },
    "device_id": "DEV001",
    "latitude": 51.509865,
    "longitude": -0.118092,
    "timestamp": "2025-05-12T12:30:00Z"
  }
]
```

---

## 🧠 Business Logic Rules

- Each **user** can only have **one device**.
- Each **device** can only be assigned to **one user**.
- Devices only send locations if **assigned**.
- Location pings are stored and ordered by timestamp.

---

## ✅ Requirements

- Python 3.8+
- Django 4.x

---

## 🚀 Ready for Deployment

You can adapt this to use PostgreSQL and host on services like Heroku, Railway, or Render with ease.

---

## 📩 Questions?

Feel free to reach out or open an issue.

---

## ⏰ If I had more time I would...

1. Create an endpoint for getting a user's historical location points for the day, which could be plotted as a visual map
2. Authentication and permissions for who can assign and unassign devices and view sensitive data
3. Detect and provide a list of inactive devices
