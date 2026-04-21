
# 🌍 Web Traffic Globe Visualisation

![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A real-time 3D visualisation of web traffic flowing to a server from all over the world. Built as part of the *Data Wrangling and Visualisation* course assignment.

<img width="1889" height="910" alt="image" src="https://github.com/user-attachments/assets/df8cf6c4-0790-4484-bf18-470c253880b0" />


## 🎯 Assignment Objectives Checklist

This project fulfills **all core requirements** and includes **bonus interactive features**:

| Task | Description | Status |
|------|-------------|--------|
| 1️⃣ | Python script reads `.csv` and sends packages with original timestamps | ✅ Done |
| 2️⃣ | Flask server parses incoming packages and forwards them to the frontend | ✅ Done |
| 3️⃣ | Three.js visualisation on a World Globe with interactive elements | ✅ Done |
| 4️⃣ | Full Docker containerisation with `docker compose up` orchestration | ✅ Done |
| 🌟 | **Bonus:** List of Top-5 most frequent locations (updates in real-time) | ✅ Done |
| 🌟 | **Bonus:** Filter to show only suspicious traffic | ✅ Done |
| 🌟 | **Bonus:** Reverse geocoding (click on point shows City & Country) | ✅ Done |

---

## 📁 Project Structure

```
Web-Traffic-Globe-Visualisation/
├── data_generation.py      # 🐍 Sender: reads CSV and streams data with delays
├── server.py               # 🌐 Flask API: receives packages and serves the frontend
├── ip_addresses.csv        # 📊 Dataset (IP, Lat, Lon, Timestamp, Suspicious flag)
├── docker-compose.yml      # 🐳 Docker composition configuration
├── Dockerfile.server       # 🐳 Flask server container definition
├── Dockerfile.sender       # 🐳 Data sender container definition
├── templates/              # 🎨 Frontend templates folder (Flask default)
│   └── visual.html         # ✨ Main Three.js visualisation 
└── README.md               # 📖 You are reading it!
```

---

## 🚀 How It Works

### 1️⃣ Data Generation (`data_generation.py`)
- The script loads the provided `ip_addresses.csv` file.
- It sorts the records by the **Unix timestamp** column to preserve the original order.
- Using the `requests` library, it sends each package as a **GET request** to the Flask server.
- ⏳ **Crucial:** It respects the time intervals between packages (waits for `delta` seconds), simulating real user traffic rather than a flood.

### 2️⃣ Backend Server (`server.py`)
- A lightweight **Flask** application.
- **`/package` (GET):** Receives JSON data from the sender via query parameters and stores it in memory.
- **`/packages` (GET):** Returns the entire list of received packages to the frontend as JSON.
- **`/` (GET):** Renders the `visual.html` template.

### 3️⃣ Frontend Visualisation (`visual.html` + Three.js)
- Renders a high-resolution **Earth** with clouds, atmosphere, and a starfield.
- Fetches package data from `/packages` every **2 seconds**.
- Converts `Latitude` and `Longitude` into 3D coordinates.
- **Point Lifetime:** Each point stays on the globe for **30 seconds** (adjustable) before gracefully fading away (removed from the scene).
- **Colors:**
    - 🟢 Green: Normal traffic (`suspicious = 0`)
    - 🔴 Red: Suspicious traffic (`suspicious = 1`)

### 4️⃣ Dockerisation
- Everything is wrapped in **Docker** for easy setup.
- `docker-compose.yml` spins up two services:
    - `flask-server`: Exposes port `5000`.
    - `data-sender`: Runs the script once the server is ready.

---

## 🎮 User Guide: How to Use the Visualisation

Once the project is running, open `http://localhost:5000` in your browser.

| Action | How to do it | What happens |
|--------|--------------|--------------|
| **Rotate View** | 🖱️ Click & Drag | Move around the Earth freely |
| **Zoom** | 🖱️ Scroll Wheel | Get closer or further away |
| **Auto-Rotate** | ⌨️ Press **`R`** | Toggle smooth automatic rotation ON/OFF |
| **Quick Info** | 🖱️ **Hover** over a point | Shows a tooltip with IP and Status |
| **Full Info** | 🖱️ **Click** on a point | Opens modal with IP, Coordinates, and **City/Country** |
| **Focus on Top City** | 🖱️ Click on a city in the **Top 5 list** | Camera flies to that exact location |
| **Filter Traffic** | ✅ Check **"Show only suspicious"** | Hides normal (green) traffic, showing only threats |

---

## 🔧 Setup & Installation

### ✅ Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- (Optional) Python 3.10+ if you want to run without Docker.

### ▶️ Step-by-Step Launch (Recommended: Docker)

1.  **Clone / Download** this repository.
2.  Open a terminal in the root folder (`Web-Traffic-Globe-Visualisation`).
3.  Run the command:
    ```bash
    docker compose up --build
    ```
4.  Wait for the build to finish. 
5.  Open your browser and go to: **`http://localhost:5000`**

### 🛑 Stopping the Service
- Press `Ctrl + C` in the terminal.
- Run `docker compose down` to clean up containers and network.

---

## 💡 Development Journey & Design Decisions

Here is a brief log of how the project was built and the logic behind specific choices:

### 🧠 1. Handling Timestamps & Realism
*   **Problem:** Just sending 2940 lines instantly is unrealistic.
*   **Solution:** The script calculates the `delta` between `current_time` and `prev_time` and uses `time.sleep()`. This respects the original time intervals in the CSV.

### 🧠 2. Avoiding "Pop-up & Disappear" Chaos
*   **Problem:** Points blinking in and out instantly makes analysis impossible.
*   **Solution:** Implemented a **Point Lifetime Map**. Each point gets a `createdAt` timestamp. A garbage collector runs every 2 seconds and removes points older than `POINT_LIFETIME` (10 sec). This creates a smooth, trailing effect of traffic.

### 🧠 3. Preventing Map Overwhelm
*   **Problem:** Too many points (especially from Moscow/China in this dataset) overlap and look like a messy blob.
*   **Solution:**
    *   **Lifetime:** Limits total visible points.
    *   **Filtering:** The "Suspicious Only" checkbox hides the majority (normal traffic) on demand.
    *   **Size:** Points are small (0.08 radius) but grow slightly on hover/click.

### 🧠 4. Fixing the "Mirrored World" Bug 🌏➡️🌎
*   **Problem:** Initially, points appeared in the ocean instead of on land.
*   **Solution:** In `latLngToPosition`, the formula for `lngRad` had a stray minus sign (`-lng * PI / 180`). Removing it fixed the projection perfectly.

### 🧠 5. Adding Context with Reverse Geocoding
*   **Problem:** Raw coordinates (`55.7558`, `37.6173`) mean nothing to a human observer.
*   **Solution:** Integrated **BigDataCloud Reverse Geocode API**. On clicking a point, the frontend fetches the city and country name and cleans up grammar artifacts like `(the)`.

### 🧠 6. Docker Networking
*   **Problem:** The sender container couldn't resolve `localhost`.
*   **Solution:** Connected both containers via a custom `traffic-net` bridge network. The sender now points to `http://flask-server:5000`.


---

## 🛠️ Built With

*   **Backend:** Flask, Flask-CORS
*   **Data Sender:** Python 3, Requests
*   **Frontend:** Three.js (r128), HTML5, CSS3
*   **Infrastructure:** Docker, Docker Compose
*   **Geocoding:** BigDataCloud Client API

