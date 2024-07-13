$(document).ready(function () {
    const body = $("body");
    const icon = $("#mode-icon");
    const toggleButton = $("#toggle-button");
    const switchButton = $("#mode-switch");
    const inputBox = $("#inputBox");
    const boxes = $(
        "button:not(#toggle-button, #mode-switch), select, input:not(#submit, #inputBox)"
    );
    const links = $("a, #query-link, #quiz-link, #table-link");
    const container = $(".container-1, .summary");
    const svg = $("#svg");

    // 切换亮暗模式
    function toggleMode() {
        body.toggleClass("dark-mode");
        const isDarkMode = body.hasClass("dark-mode");
        localStorage.setItem("mode", isDarkMode ? "dark" : "light");
        updateModeElements(isDarkMode);
        body.trigger("toggle-dark-mode");
    }

    // 更新亮暗模式相关的元素
    function updateModeElements(isDarkMode) {
        const displayStyle = window.location.pathname.startsWith("/quiz/")
            ? "block"
            : "flex";
        body.css("display", displayStyle);

        if (isDarkMode) {
            icon.text("light_mode");
            applyDarkModeStyles();
        } else {
            icon.text("dark_mode");
            applyLightModeStyles();
        }
    }

    // 应用暗模式样式
    function applyDarkModeStyles() {
        const darkStyles = {
            color: "#e0e0e0",
            backgroundColor: "#616161",
        };
        const darkContainerStyles = {
            color: "#e0e0e0",
            backgroundColor: "#333",
        };

        boxes.css(darkStyles);
        toggleButton.css({ color: "#e0e0e0" });
        switchButton.css({ color: "#e0e0e0" });
        inputBox.css({ "border-color": "#e0e0e01a", color: "#e0e0e0" });
        links.css({ color: "#e0e0e0" });
        container.css(darkContainerStyles);
        svg.addClass("invert");
    }

    // 应用亮模式样式
    function applyLightModeStyles() {
        const lightStyles = {
            color: "#000",
            backgroundColor: "#f0f0f0",
        };
        const lightContainerStyles = {
            color: "#000",
            backgroundColor: "#fff",
        };

        boxes.css(lightStyles);
        toggleButton.css({ color: "#000" });
        switchButton.css({ color: "#000" });
        inputBox.css({ "border-color": "#50535a1a", color: "#000" });
        links.css({ color: "#000" });
        container.css(lightContainerStyles);
        svg.removeClass("invert");
    }

    // 页面加载完成时应用保存的模式或系统偏好模式
    const savedMode = localStorage.getItem("mode");
    const prefersDarkScheme = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;
    const isDarkMode = savedMode ? savedMode === "dark" : prefersDarkScheme;

    body.toggleClass("dark-mode", isDarkMode);
    updateModeElements(isDarkMode);

    // 为切换按钮绑定点击事件
    switchButton.click(toggleMode);
});
