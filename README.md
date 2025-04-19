# 🏏 IPL Data Analysis Project

A complete data analysis and visualization pipeline built on IPL cricket data. The project includes data preprocessing, relational database design, and an interactive dashboard to explore insights from matches, players, and teams.

---
![Overview](folder/img.png)
## 📌 Team Information

**Group 7 – DS5003 DE Project**  
**Instructor:** Dr. Mrinal Das  

**Team Members:**
- Ankita K (142302002)
- Vishal Singh (142302009)
- Abhishek S Mayya (142302014)

---

## ⚙️ Project Overview

![Overview](folder/img1.png)


This project involves:
- Cleaning and preprocessing IPL match data
- Creating a PostgreSQL database schema
- Feature engineering for player/match stats
- Building a Streamlit dashboard
- Visualizing insights using Python libraries

---

## 🧹 Data Preprocessing

![Preprocessing](./images/slide3_img2.png)

Key steps:
- **Handled Missing Values**: City, Venue, Season, Team Names
- **Corrected Formats**: Fixed season format (2007/08 → 2008), name inconsistencies
- **Feature Engineering**:
  - Merged columns like `Kind + Fielders involved`
  - Computed winning margins (`wonby + margin`)
  - Aggregated data at match and player level

---

## 🧮 Database Schema

![Schema](folder/schema.png)

The PostgreSQL database schema organizes match, player, and performance information for structured querying and integration with visualization tools.

---

## 📊 Dashboard Overview

![Dashboard](folder/img2.png)

The interactive dashboard is built using **Streamlit**, enabling:
- Player-wise batting and bowling performance
- Team win/loss stats
- SQL-based custom queries with visualizations

---

## 🧰 Tools & Libraries Used


- **Data Preprocessing**: Pandas, NumPy (Google Colab)
- **Database Management**: PostgreSQL, VS Code, psycopg2
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit

---

## 👥 Individual Contributions

| Team Member       | Responsibilities                                                                 |
|-------------------|----------------------------------------------------------------------------------|
| **Ankita K**       | Dashboard design, login/register pages, SQL queries, data visualization         |
| **Vishal Singh**   | Data preprocessing, SQL integration, dashboard plotting                         |
| **Abhishek S Mayya** | Database design, query formulation, Batting & Bowling stats in dashboard     |


