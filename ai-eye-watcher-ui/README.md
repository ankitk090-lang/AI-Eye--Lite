# AI-Eye Watcher - Native Dev UI

A modern, dark-themed dashboard for the AI-Eye Watcher network security monitoring system built with React and Material-UI.

## Features

- 🎨 Modern dark theme with purple accent colors
- 📱 Responsive design that works on desktop and mobile
- 📊 Dashboard with statistics cards and chart placeholders
- 🧭 Navigation sidebar with routing
- 🎯 Built with React, Material-UI, and React Router

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
   ```bash
   cd ai-eye-watcher-ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
src/
├── components/
│   ├── Layout.jsx          # Main layout with sidebar and navigation
│   └── StatCard.jsx        # Reusable statistics card component
├── pages/
│   └── DashboardPage.jsx   # Main dashboard page
├── theme.js                # Material-UI dark theme configuration
├── App.jsx                 # Main app component with routing
└── main.jsx                # App entry point with providers
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Technologies Used

- **React 19** - UI library
- **Material-UI (MUI)** - Component library and theming
- **React Router** - Client-side routing
- **Vite** - Build tool and development server
- **Chart.js** - Charting library (ready for integration)

## Next Steps

- Replace chart placeholders with real Chart.js implementations
- Add real data integration
- Implement remaining pages (Network Activity, Threat Alerts, etc.)
- Add authentication and user management
- Connect to backend APIs