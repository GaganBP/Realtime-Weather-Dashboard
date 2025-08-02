# 🌤️ Automated Multi-City Weather Dashboard

A fully automated, enterprise-grade weather monitoring dashboard built with Power BI and GitHub Actions, providing real-time weather data and forecasts for multiple Indian cities with advanced air quality monitoring and automated data refresh every 3 hours.

![Weather Dashboard Preview](https://via.placeholder.com/800x400/FF6B35/FFFFFF?text=Automated+Weather+Dashboard)

## 🚀 **NEW: Full Automation Features**
- ⚡ **GitHub Actions Integration**: Automated data fetching every 3 hours
- 🔄 **Power BI Auto-Refresh**: Dashboard updates 8 times daily
- 🛠️ **Zero Manual Intervention**: Fully automated pipeline
- 📊 **Real-time Data**: Always fresh weather information
- 🏗️ **Enterprise Architecture**: Production-ready automated system

## 📊 Features

### 🏙️ Multi-City Coverage
- **9 Indian Cities**: Bengaluru, Mumbai, Mysuru, New Delhi, Mandya, Madikeri, Hassan, Bhagamandala, Ghaziabad
- **Seamless Navigation**: Horizontal scrollable city selector for quick switching
- **Regional Diversity**: Coverage from coastal cities to hill stations to metropolitan areas
- **Automated Updates**: Fresh data every 3 hours for all cities

### 🌡️ Weather Metrics
- **Current Conditions**: Real-time temperature, humidity, wind speed, visibility
- **14-Day Forecast**: Extended temperature trends with interactive line charts
- **Precipitation**: Rain probability percentages and current precipitation levels
- **UV Index**: Sun exposure monitoring for outdoor planning
- **Sunrise/Sunset**: Daily solar schedule for each location

### 🌬️ Air Quality Monitoring
- **Comprehensive AQI**: Real-time Air Quality Index with health recommendations
- **Pollutant Breakdown**: PM10, PM2.5, O3, SO2, CO, NO2 levels
- **Health Alerts**: Color-coded warnings for sensitive individuals
- **Regional Comparison**: Air quality variations across different geographic regions

### 📈 Data Visualization
- **Temperature Trends**: Interactive forecast charts showing 14-day weather patterns
- **Rain Probability**: Visual percentage bars for precipitation chances
- **Air Quality Gauge**: Circular progress indicators with health status
- **Weather Icons**: Intuitive visual representation of weather conditions

## 🛠️ Technical Architecture

### Automated Data Pipeline
```
WeatherAPI.com → GitHub Actions → GitHub Repository → Power BI Service → Dashboard
     ↓              (Every 3h)         ↓              (8x daily)      ↓
 Fresh Data    →   Automated Fetch  →  JSON Storage  →  Auto Refresh → Live Dashboard
```

### Technology Stack
- **GitHub Actions**: Automated data fetching and repository updates
- **Python**: Weather data processing and JSON generation
- **WeatherAPI.com**: Real-time weather and air quality data source
- **Power BI Pro**: Dashboard visualization with scheduled refresh
- **Power Query**: Data transformation and GitHub integration
- **DAX**: Custom calculations and measures

### Automation Schedule
- **GitHub Actions**: Every 3 hours (8 times daily)
  - UTC: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00
  - IST: 5:30 AM, 8:30 AM, 11:30 AM, 2:30 PM, 5:30 PM, 8:30 PM, 11:30 PM, 2:30 AM
- **Power BI Refresh**: 8 times daily (synchronized with data updates)
  - IST: 6:00 AM, 9:00 AM, 12:00 PM, 3:00 PM, 6:00 PM, 9:00 PM, 12:00 AM, 3:00 AM

## 📋 Setup Instructions

### Prerequisites
- GitHub account with repository
- WeatherAPI.com account and API key
- Power BI Pro license (for scheduled refresh)
- Basic understanding of GitHub Actions

### 🔧 Complete Setup Guide

#### 1. Repository Setup
```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard
```

#### 2. API Key Configuration
- Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
- Get your free API key
- Update the API key in your `weather_fetcher.py` file

#### 3. GitHub Actions Setup
- Copy the workflow file to `.github/workflows/weather_update.yml`
- Ensure Python script `weather_fetcher.py` is in root directory
- Commit and push to trigger first run

#### 4. Power BI Configuration
- Open `Weather_Dashboard.pbix` in Power BI Desktop
- Update data source to point to your GitHub repository
- Publish to Power BI Service
- Configure scheduled refresh (8 times daily)

## 🏗️ Project Structure
```
weather-dashboard/
│
├── .github/
│   └── workflows/
│       └── weather_update.yml      # GitHub Actions workflow
├── weather_data/                   # Automated data storage
│   ├── bengaluru.json             # City weather data (auto-updated)
│   ├── mumbai.json
│   └── ... (all 9 cities)
├── weather_fetcher.py              # Python automation script
├── requirements.txt                # Python dependencies
├── Weather_Dashboard.pbix          # Main Power BI file
├── docs/
│   ├── setup_guide.md             # Detailed setup instructions
│   ├── automation_guide.md        # GitHub Actions configuration
│   └── powerbi_setup.md           # Power BI configuration guide
└── README.md                       # This file
```

## ⚙️ Automation Components

### GitHub Actions Workflow
```yaml
name: Update Weather Data
on:
  schedule:
    - cron: '0 */3 * * *'  # Every 3 hours
  workflow_dispatch:       # Manual trigger option

jobs:
  update-weather:
    runs-on: ubuntu-latest
    steps:
      - name: Fetch and update weather data
      - name: Commit changes to repository
      - name: Notify on failures
```

### Python Weather Fetcher
- **API Integration**: Fetches weather data from WeatherAPI.com
- **Data Processing**: JSON formatting for Power BI consumption
- **Multi-city Support**: Processes all 9 cities in one run
- **Automated Updates**: Runs via GitHub Actions schedule

### Power BI Integration
- **GitHub Data Source**: Direct connection to repository JSON files
- **Automatic Refresh**: Scheduled refresh synchronized with data updates
- **Data Transformation**: Power Query processing for optimal performance

## 📊 Dashboard Metrics

### Weather Data Points
- **Temperature**: Current, daily high/low, 7-day forecast
- **Humidity**: Relative humidity percentage
- **Wind**: Speed (km/h) and direction
- **Visibility**: Atmospheric visibility in kilometers
- **Pressure**: Atmospheric pressure in inHg
- **UV Index**: Solar radiation levels (0-11+ scale)

### Air Quality Parameters
- **PM10**: Particulate matter ≤10 micrometers
- **PM2.5**: Fine particulate matter ≤2.5 micrometers
- **O3**: Ground-level ozone concentration
- **SO2**: Sulfur dioxide levels
- **CO**: Carbon monoxide concentration
- **NO2**: Nitrogen dioxide levels

## 🎯 Use Cases

### Personal Use
- **Daily Planning**: Weather-based activity planning with always-current data
- **Travel Decisions**: Multi-city weather comparison with 14-day outlook
- **Health Monitoring**: Real-time air quality awareness

### Business Applications
- **Event Planning**: Weather-dependent scheduling with 14-day advance planning
- **Supply Chain**: Weather impact analysis with automated monitoring
- **Agriculture**: Continuous weather monitoring for farming decisions
- **Tourism**: Real-time weather information for travel recommendations

## 🔄 Data Refresh & Monitoring

### Automated Refresh Schedule
- **GitHub Actions**: Every 3 hours (24/7 automation)
- **Power BI**: 8 refreshes daily (synchronized with data updates)
- **Monitoring**: Email notifications for any failures
- **Backup**: Manual trigger option available

### Data Freshness
- **Update Frequency**: Every 3 hours via GitHub Actions
- **Dashboard Refresh**: 8 times daily in Power BI Pro
- **Manual Override**: Can refresh manually when needed

## 🌟 Key Features
- **Automated Updates**: GitHub Actions fetches fresh data every 3 hours
- **Multi-city Coverage**: Weather monitoring for 9 Indian cities
- **Air Quality Tracking**: Real-time AQI monitoring with health indicators
- **Interactive Visualization**: Power BI dashboard with trend analysis

## 🚀 Advanced Features
- **Error Handling**: Robust retry mechanisms and fallback options
- **Performance Optimization**: Efficient API usage and data processing
- **Scalability**: Easy addition of new cities to monitoring
- **Monitoring**: GitHub Actions logs and Power BI refresh notifications

## 🤝 Contributing
This is a personal weather dashboard project. If you'd like to create your own version:
1. Fork the repository for your own use
2. Modify the cities list in `weather_fetcher.py` to your preferred locations
3. Update your WeatherAPI key in GitHub Secrets
4. Customize the Power BI dashboard for your needs

## 📝 License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments
- **WeatherAPI.com** for comprehensive weather data
- **GitHub Actions** for reliable automation platform
- **Power BI Community** for visualization inspiration
- **Open Source Community** for automation best practices

## 📞 Contact
- **GitHub**: [Gagan BP](https://github.com/GaganBP)
- **LinkedIn**: [Gagan BP](https://www.linkedin.com/in/gagan-b-p-0a9635243/)
- **Portfolio**: [gaganbp.github.io](https://gaganbp.github.io/)
- **Email**: databygagan@gmail.com

---

## 🎉 **Current Status**
🟢 **System Active**: Weather data updates every 3 hours automatically  
📊 **Dashboard Live**: Real-time weather monitoring for all 9 Indian cities  
⚡ **Automated Pipeline**: GitHub Actions + Power BI integration running smoothly

⭐ **Star this repository if you found this automated weather dashboard helpful!**
