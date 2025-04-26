# Mental Health Monitoring System

> A dual-interface web application for tracking mental health: patients can log moods and triggers, while psychiatrists can monitor patient progress.

## 🛠️ Tech Stack
- **Frontend:** React/Next.js, CSS Modules
- **Backend:** Python/Flask
- **Database:** TinyDB (JSON-based document store)
- **API:** RESTful endpoints with Fetch API

## 🚀 Getting Started

### Prerequisites
Make sure you have the following installed:
- Python (v3.8 or higher)
- Node.js (v14 or higher)
- npm (comes with Node.js)

### Installation
1. Clone this repo
   ```bash
   git clone https://github.com/NitishPradhan26/Mood-Trigger-Tracker.git
   cd mental-health-monitor
   ```

2. Set up Backend
   ```bash
   cd BackEnd
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install flask flask-cors tinydb
   ```

3. Set up Frontend
   ```bash
   cd FrontEnd
   npm install
   ```

### Running the Application
1. Start Backend server
   ```bash
   cd BackEnd
   python app.py
   ```

2. Start Frontend development server
   ```bash
   cd FrontEnd
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## 📱 Features

### Patient Interface
- Mood tracking with emoji interface (😢 😐 😊)
- Trigger logging with intensity scale (1-10)
- Associated feelings tracking
- Historical view of entries

### Psychiatrist Dashboard
- Patient list management
- Individual patient history viewing
- Mood and trigger pattern monitoring
- Comprehensive emotional response tracking

## �� Project Structure
