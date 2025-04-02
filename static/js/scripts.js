document.addEventListener("DOMContentLoaded", function () {
    const darkModeToggle = document.getElementById("dark-mode-toggle");
    const html = document.documentElement; // Select <html> instead of <body>

    // Check user preference in local storage
    if (localStorage.getItem("darkMode") === "enabled") {
        html.classList.add("dark");
    }

    // Toggle dark mode
    darkModeToggle.addEventListener("click", function () {
        html.classList.toggle("dark");
        if (html.classList.contains("dark")) {
            localStorage.setItem("darkMode", "enabled");
        } else {
            localStorage.setItem("darkMode", "disabled");
        }
    });

    // Autocomplete feature
    function setupAutocomplete(inputField, type) {
        inputField.addEventListener("input", function () {
            let query = inputField.value.trim();

            if (query.length < 2) {
                document.getElementById(type + "-suggestions").innerHTML = "";
                return;
            }

            fetch(`/autocomplete?query=${query}&type=${type}`)
                .then(response => response.json())
                .then(data => {
                    let suggestionsBox = document.getElementById(type + "-suggestions");
                    suggestionsBox.innerHTML = "";

                    data.forEach(item => {
                        let suggestionItem = document.createElement("li");
                        suggestionItem.textContent = item;
                        suggestionItem.classList.add("suggestion-item");

                        suggestionItem.addEventListener("click", function () {
                            inputField.value = item;
                            suggestionsBox.innerHTML = "";
                        });

                        suggestionsBox.appendChild(suggestionItem);
                    });
                });
        });
    }

    setupAutocomplete(document.getElementById("medicine_name"), "medicine");
    setupAutocomplete(document.getElementById("disease_name"), "disease");
});
