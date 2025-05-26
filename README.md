# MeteoApp

A modern cross-platform weather application built with Python, Flet, and Flutter.

## Features

- Display current weather conditions for any city
- Show hourly and daily forecasts
- Display temperature charts
- Use current location for weather data
- Responsive design for different screen sizes
- Cross-platform support (Desktop, Web, Mobile)
- Native mobile experience through Flutter integration

## Project Structure

The project follows a modular architecture with both Python backend and Flutter frontend:

```
.
├── src/                    # Python backend source code
│   ├── app.py             # Main application entry point
│   ├── config.py          # Configuration settings
│   ├── state_manager.py   # Application state management
│   ├── assets/            # Static assets (images, icons)
│   ├── layout/            # Layout components
│   │   ├── backend/       # Backend layout logic
│   │   └── frontend/      # Frontend layout components
│   ├── services/          # Service layer
│   │   ├── api_service.py     # Weather API service
│   │   └── geolocation_service.py  # Geolocation service
│   └── ui/                # User interface components
│       ├── components.py      # Reusable UI components
│       └── weather_view.py    # Weather display components
│
├── build/                  # Build artifacts and Flutter app
│   └── flutter/           # Flutter application
│       ├── lib/           # Flutter source code
│       ├── android/       # Android platform code
│       ├── ios/           # iOS platform code
│       ├── web/           # Web platform code
│       ├── windows/       # Windows platform code
│       ├── linux/         # Linux platform code
│       └── macos/         # macOS platform code
│
├── storage/               # Application data storage
│   ├── data/             # Persistent data
│   └── temp/             # Temporary files
│
└── requirements.txt       # Python dependencies
```

## Requirements

- Python 3.7+
- Flet
- Requests
- python-dotenv
- Babel

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MeteoApp.git
cd MeteoApp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenWeatherMap API key:
```
API_KEY=your_api_key_here
```

## Running the Application

Run the application using:

```bash
python src/app.py
```

For backward compatibility, you can also use:

```bash
python src/main.py
```

## Development

### Adding New Features

To add new features:

1. Update the appropriate service in `src/services/`
2. Add any new UI components in `src/ui/`
3. Update the state manager if needed
4. Connect everything in `src/app.py`

### Configuration

All configuration settings are centralized in `src/config.py`. Modify this file to change default settings.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
