// ---------------- COPY QUOTE ----------------

function copyQuote() {

    const quote =
        document.querySelector(".quote-text");

    const author =
        document.querySelector(".author");

    if (!quote || !author) {
        return;
    }

    const text =
        quote.innerText + " " + author.innerText;

    navigator.clipboard.writeText(text)
        .then(() => {

            alert("Quote copied to clipboard! 📋");

        })
        .catch(() => {

            alert("Unable to copy quote.");

        });
}


// ---------------- DELETE CONFIRMATION ----------------

function confirmDelete() {

    return confirm(
        "Are you sure you want to delete this quote?"
    );
}


// ---------------- DARK MODE ----------------

function toggleDarkMode() {

    document.body.classList.toggle("dark");

    const isDark =
        document.body.classList.contains("dark");

    localStorage.setItem(
        "darkMode",
        isDark ? "enabled" : "disabled"
    );
}


// ---------------- LOAD DARK MODE ----------------

document.addEventListener("DOMContentLoaded", function () {

    const darkMode =
        localStorage.getItem("darkMode");

    if (darkMode === "enabled") {

        document.body.classList.add("dark");

    }

});