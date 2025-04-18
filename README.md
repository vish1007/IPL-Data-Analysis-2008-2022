# 🏏 IPL Data Analysis Project

A complete data analysis and visualization pipeline built on IPL cricket data. The project includes data preprocessing, relational database design, and an interactive dashboard to explore insights from matches, players, and teams.

---

## 📌 Team Information

**Group 7 – DS5003 DE Project**  
**Instructor:** Dr. Mrinal Das  

**Team Members:**
- Ankita K (142302002)
- Vishal Singh (142302009)
- Abhishek S Mayya (142302014)

---

## ⚙️ Project Overview

![Overview](https://github.com/vish1007/IPL-Data-Analysis-2008-2022/raw/f10dc5f037dbbc54e3d8bf343f878a3f8c8226d5/img.png)


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

![Schema](./images/slide3_img3.png)

The PostgreSQL database schema organizes match, player, and performance information for structured querying and integration with visualization tools.

---

## 📊 Dashboard Overview

![Dashboard](./images/slide3_img4.png)

The interactive dashboard is built using **Streamlit**, enabling:
- Player-wise batting and bowling performance
- Team win/loss stats
- SQL-based custom queries with visualizations

---

## 🧰 Tools & Libraries Used

![Tools](./images/slide4_img5.png)

- **Data Preprocessing**: Pandas, NumPy (Google Colab)
- **Database Management**: PostgreSQL, VS Code, psycopg2
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit

---

## 👥 Individual Contributions

![Contributions](./images/slide5_img9.png)

| Team Member       | Responsibilities                                                                 |
|-------------------|----------------------------------------------------------------------------------|
| **Ankita K**       | Dashboard design, login/register pages, SQL queries, data visualization         |
| **Vishal Singh**   | Data preprocessing, SQL integration, dashboard plotting                         |
| **Abhishek S Mayya** | Database design, query formulation, Batting & Bowling stats in dashboard     |


