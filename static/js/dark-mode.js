$(document).ready(() => {
    const elements = {
        body: $("body"),
        icon: $("#mode-icon"),
        toggleButton: $("#toggle-button"),
        switchButton: $("#mode-switch"),
        inputBox: $("#inputBox"),
        boxes: $(
            "button:not(#toggle-button, #mode-switch), select, input:not(#submit, #inputBox)"
        ),
        links: $("a, #query-link, #quiz-link, #table-link"),
        container: $(".container-1, .summary"),
        svg: $("#svg"),
    };

    const darkStyles = {
        color: "#e0e0e0",
        backgroundColor: "#616161",
    };
    const darkContainerStyles = {
        color: "#e0e0e0",
        backgroundColor: "#333",
    };
    const lightStyles = {
        color: "#000",
        backgroundColor: "#f0f0f0",
    };
    const lightContainerStyles = {
        color: "#000",
        backgroundColor: "#fff",
    };

    function toggleMode() {
        elements.body.toggleClass("dark-mode");
        const isDarkMode = elements.body.hasClass("dark-mode");
        localStorage.setItem("mode", isDarkMode ? "dark" : "light");
        updateModeElements(isDarkMode);
        elements.body.trigger("toggle-dark-mode");
    }

    function updateModeElements(isDarkMode) {
        const displayStyle = window.location.pathname.startsWith("/quiz/")
            ? "block"
            : "flex";
        elements.body.css("display", displayStyle);
        elements.icon.text(isDarkMode ? "light_mode" : "dark_mode");

        applyStyles(isDarkMode);
    }

    function applyStyles(isDarkMode) {
        if (isDarkMode) {
            applyDarkModeStyles();
        } else {
            applyLightModeStyles();
        }
    }

    function applyDarkModeStyles() {
        elements.boxes.css(darkStyles);
        elements.toggleButton.css({ color: darkStyles.color });
        elements.switchButton.css({ color: darkStyles.color });
        elements.inputBox.css({
            "border-color": "#e0e0e01a",
            color: darkStyles.color,
        });
        elements.links.css({ color: darkStyles.color });
        elements.container.css(darkContainerStyles);
        elements.svg.addClass("invert");
    }

    function applyLightModeStyles() {
        elements.boxes.css(lightStyles);
        elements.toggleButton.css({ color: lightStyles.color });
        elements.switchButton.css({ color: lightStyles.color });
        elements.inputBox.css({
            "border-color": "#50535a1a",
            color: lightStyles.color,
        });
        elements.links.css({ color: lightStyles.color });
        elements.container.css(lightContainerStyles);
        elements.svg.removeClass("invert");
    }

    const savedMode = localStorage.getItem("mode");
    const prefersDarkScheme = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;
    const isDarkMode = savedMode ? savedMode === "dark" : prefersDarkScheme;

    elements.body.toggleClass("dark-mode", isDarkMode);
    updateModeElements(isDarkMode);

    elements.switchButton.click(toggleMode);
});
