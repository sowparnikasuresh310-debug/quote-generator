# ✨ QuoteHub – Quote Generator with History

A modern and interactive **Quote Generator web application** built using **Python Flask**.

The application fetches random quotes from external APIs, automatically saves them to a **SQLite database**, and provides a complete quote history with search, favorites, deletion, and other useful features.

The application also includes **automatic API retry and fallback mechanisms**, ensuring that users can still receive quotes even when external APIs are temporarily unavailable.

---

## 📌 Project Overview

**QuoteHub** is a beginner-friendly full-stack web application developed to understand and implement:

- REST API integration
- External data handling
- JSON response processing
- Flask routing
- SQLite database operations
- CRUD operations
- API error handling
- Retry mechanisms
- API fallback mechanisms
- Frontend and backend integration
- Responsive web design

---

## 🚀 Features

### 🎲 Random Quote Generator

- Fetches a random quote from an external API.
- Displays the quote and author dynamically.
- Allows users to generate a new quote.

### 🌐 External API Integration

The application communicates with external quote APIs to retrieve quote data.

Primary API:

- ZenQuotes API

Secondary API:

- Quotable API

---

### 🔄 Automatic Retry

If the primary API fails or times out:

1. The application retries the primary API.
2. If it fails again, it tries the secondary API.
3. If both APIs fail, it uses a local backup quote.

This improves application reliability.

---

### 📦 Local Backup Quotes

The application contains a collection of backup quotes.

If both external APIs are unavailable, a quote is selected from the local collection.

Therefore, the application can continue working even without a successful API response.

---

### 💾 Quote History

Every generated quote is automatically stored in an SQLite database.

The history includes:

- Quote
- Author
- Favorite status
- Date and time

---

### ❤️ Favorite Quotes

Users can mark quotes as favorites.

Favorite status is stored in the database and can be changed at any time.

---

### 🔍 Search History

Users can search their saved quotes by:

- Quote text
- Author name

---

### 🗑️ Delete Quotes

Users can remove individual quotes from their history.

A confirmation message is displayed before deletion.

---

### 📋 Copy Quote

Users can copy the displayed quote and author directly to their clipboard.

---

### 🌙 Dark Mode

The application includes a dark mode option.

The selected theme is stored in the browser's `localStorage`, so the preference remains after refreshing the page.

---

### 📱 Responsive Design

The interface is designed to work on:

- 💻 Desktop
- 💻 Laptop
- 📱 Mobile
- 📱 Tablet

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Interactive features |
| Requests | API communication |
| REST API | External quote retrieval |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📂 Project Structure

```text
quote-generator/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── history.html
│
└── static/
    ├── style.css
    └── script.js
