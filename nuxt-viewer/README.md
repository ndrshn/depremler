# Earthquakes in Türkiye - Nuxt 4 + Nuxt UI

This application visualizes earthquake data in Türkiye from 2003 onwards.

## Features

- **Interactive Map**: Leaflet-based map showing earthquake locations with color-coded magnitude markers
- **Data Table**: Paginated table with earthquake details including date, location, magnitude, and depth
- **Statistics**: Comprehensive statistics including:
  - Average magnitude and depth
  - Daily earthquake average
  - Highest magnitude earthquake
  - Deepest earthquake
  - Magnitude distribution
  - Depth distribution
  - Monthly distribution
- **Year Filter**: Select earthquakes by year (2003-present)
- **Date Filter**: Filter earthquakes within a date range

## Tech Stack

- **Framework**: Nuxt 4 (with compatibility mode)
- **UI Library**: Nuxt UI 3
- **Styling**: Tailwind CSS 4
- **Maps**: Leaflet
- **TypeScript**: Full type support

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
nuxt-viewer/
├── app/
│   ├── components/
│   │   └── Statistics.vue    # Statistics display component
│   ├── pages/
│   │   └── index.vue         # Main page with map and table
│   ├── assets/
│   │   └── css/
│   │       └── main.css      # Global styles
│   └── app.vue               # Root component
├── public/
│   ├── data/                 # Earthquake data JSON files
│   └── logo.svg              # App logo
├── nuxt.config.ts            # Nuxt configuration
└── package.json
```

## Data Source

Earthquake data is sourced from historical records and includes:
- Date and time
- Location
- Latitude and longitude
- Magnitude
- Depth (km)
