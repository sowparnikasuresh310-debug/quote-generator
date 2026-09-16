from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import requests
import time
from datetime import datetime
import random

app = Flask(__name__)

DATABASE = "database.db"


# =========================================================
# API CONFIGURATION
# =========================================================

# Primary API
ZENQUOTES_API = "https://zenquotes.io/api/random"

# Secondary API
QUOTABLE_API = "https://api.quotable.io/random"


# =========================================================
# LOCAL BACKUP QUOTES
# =========================================================

BACKUP_QUOTES = [
    {
        "quote": "The future depends on what you do today.",
        "author": "Mahatma Gandhi"
    },
    {
        "quote": "Success is not final, failure is not fatal.",
        "author": "Winston Churchill"
    },
    {
        "quote": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs"
    },
    {
        "quote": "It always seems impossible until it's done.",
        "author": "Nelson Mandela"
    },
    {
        "quote": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt"
    },
    {
        "quote": "The secret of getting ahead is getting started.",
        "author": "Mark Twain"
    },
    {
        "quote": "Do what you can, with what you have, where you are.",
        "author": "Theodore Roosevelt"
    },
    {
        "quote": "Everything you've ever wanted is on the other side of fear.",
        "author": "George Addair"
    },
    {
        "quote": "Dream big and dare to fail.",
        "author": "Norman Vincent Peale"
    },
    {
        "quote": "Don't watch the clock; do what it does. Keep going.",
        "author": "Sam Levenson"
    },
    {
        "quote": "The harder I work, the luckier I get.",
        "author": "Samuel Goldwyn"
    },
    {
        "quote": "Great things are done by a series of small things brought together.",
        "author": "Vincent van Gogh"
    },
    {
        "quote": "Start where you are. Use what you have. Do what you can.",
        "author": "Arthur Ashe"
    },
    {
        "quote": "You miss 100% of the shots you don't take.",
        "author": "Wayne Gretzky"
    },
    {
        "quote": "The best way out is always through.",
        "author": "Robert Frost"
    }
]


# =========================================================
# DATABASE
# =========================================================

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL,
            is_favorite INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()


# =========================================================
# PRIMARY API - ZENQUOTES
# =========================================================

def fetch_from_zenquotes():

    try:

        print("Trying ZenQuotes API...")

        response = requests.get(
            ZENQUOTES_API,
            timeout=(3, 5),
            headers={
                "User-Agent": "QuoteHub/1.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list) and len(data) > 0:

            quote_data = data[0]

            quote = quote_data.get("q")
            author = quote_data.get("a")

            if quote:

                print("✓ Quote received from ZenQuotes")

                return {
                    "quote": quote,
                    "author": author or "Unknown",
                    "source": "ZenQuotes API"
                }

    except requests.exceptions.Timeout:

        print("✗ ZenQuotes timed out.")

    except requests.exceptions.ConnectionError:

        print("✗ Could not connect to ZenQuotes.")

    except requests.exceptions.RequestException as error:

        print("✗ ZenQuotes request failed:", error)

    except (ValueError, KeyError, TypeError) as error:

        print("✗ Invalid ZenQuotes response:", error)

    return None


# =========================================================
# SECONDARY API - QUOTABLE
# =========================================================

def fetch_from_quotable():

    try:

        print("Trying Quotable API...")

        response = requests.get(
            QUOTABLE_API,
            timeout=(3, 5),
            headers={
                "User-Agent": "QuoteHub/1.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):

            quote = data.get("content")
            author = data.get("author")

            if quote:

                print("✓ Quote received from Quotable")

                return {
                    "quote": quote,
                    "author": author or "Unknown",
                    "source": "Quotable API"
                }

    except requests.exceptions.Timeout:

        print("✗ Quotable timed out.")

    except requests.exceptions.ConnectionError:

        print("✗ Could not connect to Quotable.")

    except requests.exceptions.RequestException as error:

        print("✗ Quotable request failed:", error)

    except (ValueError, KeyError, TypeError) as error:

        print("✗ Invalid Quotable response:", error)

    return None


# =========================================================
# LOCAL BACKUP
# =========================================================

def get_local_backup_quote():

    quote = random.choice(BACKUP_QUOTES)

    print("✓ Using local backup quote.")

    return {
        "quote": quote["quote"],
        "author": quote["author"],
        "source": "Local Backup"
    }


# =========================================================
# FETCH QUOTE WITH RETRY + FALLBACK
# =========================================================

def fetch_quote():

    # -----------------------------------------------------
    # FIRST ATTEMPT - ZENQUOTES
    # -----------------------------------------------------

    quote = fetch_from_zenquotes()

    if quote:

        return quote


    # -----------------------------------------------------
    # RETRY ZENQUOTES
    # -----------------------------------------------------

    print("Retrying ZenQuotes in 1 second...")

    time.sleep(1)

    quote = fetch_from_zenquotes()

    if quote:

        return quote


    # -----------------------------------------------------
    # SECOND API - QUOTABLE
    # -----------------------------------------------------

    quote = fetch_from_quotable()

    if quote:

        return quote


    # -----------------------------------------------------
    # RETRY QUOTABLE
    # -----------------------------------------------------

    print("Retrying Quotable in 1 second...")

    time.sleep(1)

    quote = fetch_from_quotable()

    if quote:

        return quote


    # -----------------------------------------------------
    # FINAL FALLBACK
    # -----------------------------------------------------

    print("Both APIs failed.")

    return get_local_backup_quote()


# =========================================================
# SAVE QUOTE
# =========================================================

def save_quote(quote):

    if not quote:
        return

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO quotes
        (quote, author, is_favorite, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            quote["quote"],
            quote["author"],
            0,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()

    conn.close()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    quote = fetch_quote()

    save_quote(quote)

    return render_template(
        "index.html",
        quote=quote
    )


# =========================================================
# NEW QUOTE
# =========================================================

@app.route("/new-quote")
def new_quote():

    quote = fetch_quote()

    save_quote(quote)

    return redirect(
        url_for("index")
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    search = request.args.get(
        "search",
        ""
    ).strip()

    conn = get_db_connection()

    if search:

        quotes = conn.execute(
            """
            SELECT *
            FROM quotes
            WHERE quote LIKE ?
               OR author LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    else:

        quotes = conn.execute(
            """
            SELECT *
            FROM quotes
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        quotes=quotes,
        search=search
    )


# =========================================================
# FAVORITE
# =========================================================

@app.route(
    "/favorite/<int:quote_id>",
    methods=["POST"]
)
def favorite(quote_id):

    conn = get_db_connection()

    quote = conn.execute(
        """
        SELECT is_favorite
        FROM quotes
        WHERE id = ?
        """,
        (quote_id,)
    ).fetchone()

    if quote:

        new_status = (
            0
            if quote["is_favorite"]
            else 1
        )

        conn.execute(
            """
            UPDATE quotes
            SET is_favorite = ?
            WHERE id = ?
            """,
            (
                new_status,
                quote_id
            )
        )

        conn.commit()

    conn.close()

    return redirect(
        url_for("history")
    )


# =========================================================
# DELETE QUOTE
# =========================================================

@app.route(
    "/delete/<int:quote_id>",
    methods=["POST"]
)
def delete_quote(quote_id):

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM quotes
        WHERE id = ?
        """,
        (quote_id,)
    )

    conn.commit()

    conn.close()

    return redirect(
        url_for("history")
    )


# =========================================================
# JSON API ENDPOINT
# =========================================================

@app.route("/api/quote")
def api_quote():

    quote = fetch_quote()

    if not quote:

        return jsonify({
            "error": "Unable to fetch quote"
        }), 500

    save_quote(quote)

    return jsonify({
        "quote": quote["quote"],
        "author": quote["author"],
        "source": quote["source"]
    })


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)