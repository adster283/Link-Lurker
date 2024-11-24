from flask import Flask, render_template, request
import sqlite3
import os
from whois_check import *
from permutation_check import *
from dns_lookup import *

def search_database(search_url):
    try:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../domain.db"))

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.url, f.category, f.source
            FROM urls u
            JOIN url_flags f ON u.id = f.url_id
            WHERE u.url = ?
        ''', (search_url,))
        results = cursor.fetchall()

        return results

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  

@app.route("/search", methods=["POST"])
def search():

    domain = request.form.get("domain")
    search_result = search_database(domain)

    whois_result = check_dns_records(domain)

    fuzz_result = check_match(domain)

    char_result = check_chars(domain)

    dns_result = get_dns_records(domain)

    print(char_result)

    return render_template(
        "results.html", 
        domain=domain,
        search_result=search_result,
        whois_result=whois_result,
        fuzz_result=fuzz_result,
        char_result=char_result,
        dns_result=dns_result
    )

if __name__ == "__main__":
    app.run(debug=True)