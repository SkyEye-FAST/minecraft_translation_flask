$(document).ready(function () {
    const body = $("body");

    function toggleDarkMode() {
        body.toggleClass("dark-mode");
        updateBoxes();
    }

    body.on("toggle-dark-mode", toggleDarkMode);
    $("#mode-switch").click(function () {
        body.trigger("toggle-dark-mode");
    });

    let currentQuestionIndex = 0;
    const questionsData = questions || {};
    const questionKeys = Object.keys(questionsData);

    if (questionKeys.length === 0) {
        console.error("No questions available.");
        return;
    }

    const $info = $("#info");
    const $sourceText = $("#sourceText");
    const $keyText = $("#keyText");
    const $inputBox = $("#inputBox");
    const $boxes = $("#boxes");
    const $buttons = $("#buttons")
    const $skipButton = $("#skipButton")
    const $hintButton = $("#hintButton")

    async function initializeQuestion() {
        const currentKey = questionKeys[currentQuestionIndex];
        const { source, translation } = questionsData[currentKey];

        const translationSegments = [
            ...new Intl.Segmenter().segment(translation),
        ].map((segment) => segment.segment);
        const translationLength = translationSegments.length;

        await fadeOutElement($info, fadeDuration);

        $sourceText.text(source);
        $keyText.text(currentKey);

        $inputBox.val("");
        createBoxes(translationLength);

        await fadeInElement($info, fadeDuration);
    }

    function getSegmentedText(text) {
        return [...new Intl.Segmenter().segment(text)].map(
            (segment) => segment.segment
        );
    }

    function truncateInput(input, maxLength) {
        const segmentedInput = getSegmentedText(input);
        return segmentedInput.slice(0, maxLength).join("");
    }

    function createBoxes(length) {
        $boxes.empty();
        for (let i = 0; i < length; i++) {
            $("<div>", {
                class: "box",
                id: "box" + (i + 1),
            }).appendTo($boxes);
        }
    }

    function updateBoxes() {
        const isDarkMode = localStorage.getItem("mode");

        const input = $inputBox.val();
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];

        const translationSegments = getSegmentedText(translation);
        const translationLength = translationSegments.length;

        let inputSegments = getSegmentedText(input);

        if (inputSegments.length > translationLength) {
            inputSegments = inputSegments.slice(0, translationLength);
            $inputBox.val(inputSegments.join(""));
        }

        $(".box").each(function (index) {
            const $box = $(this);
            const userInputChar = inputSegments[index] || "";
            const correctChar = translationSegments[index] || "";

            $box.text(userInputChar);

            $box.removeClass("correct exist dark");

            if (!userInputChar) {
                $box.addClass(isDarkMode === "dark" ? "box dark" : "box");
            } else if (userInputChar === correctChar) {
                $box.addClass(
                    isDarkMode === "dark" ? "box correct dark" : "box correct"
                );
            } else if (translationSegments.includes(userInputChar)) {
                $box.addClass(
                    isDarkMode === "dark" ? "box exist dark" : "box exist"
                );
            } else {
                $box.addClass(isDarkMode === "dark" ? "box dark" : "box");
            }
        });
    }

    function delay(duration) {
        return new Promise((resolve) => setTimeout(resolve, duration));
    }

    function fadeOutElement($element, fadeDuration) {
        return new Promise((resolve) => {
            $element.fadeOut(fadeDuration, function () {
                resolve();
            });
        });
    }

    function fadeInElement($element, fadeDuration) {
        return new Promise((resolve) => {
            $element.fadeIn(fadeDuration, function () {
                resolve();
            });
        });
    }

    const delayBetweenQuestions = 800;
    const fadeDuration = 300;

    async function showSummary() {
        await fadeOutElement($info.add($inputBox).add($skipButton), fadeDuration);

        const $summaryBody = $("#summaryBody").empty();

        questionKeys.forEach((key) => {
            const { source, translation } = questionsData[key];
            $("<tr>")
                .append($("<td>").text(source), $("<td>").text(translation))
                .appendTo($summaryBody);
        });

        await fadeInElement($("#summary"), fadeDuration);
    }

    let isLocked = false;

    async function check() {
        if (isComposing) return;

        const input = $inputBox.val();
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];

        const translationLength = getSegmentedText(translation).length;
        const truncatedValue = truncateInput(input, translationLength);
        $inputBox.val(truncatedValue);
        updateBoxes();

        if (input === translation && !isLocked) {
            isLocked = true;
            await delay(delayBetweenQuestions);
            if (currentQuestionIndex === questionKeys.length - 1) {
                await showSummary();
            } else {
                await fadeOutElement($info, fadeDuration);
                currentQuestionIndex++;
                await initializeQuestion();
            }
            isLocked = false;
        }
    }

    let isComposing = false;

    $inputBox.on("compositionstart", function () {
        isComposing = true;
    });

    $inputBox.on("compositionend", function () {
        isComposing = false;
        check();
    });

    $inputBox.on("input", function () {
        check();
    });

    $skipButton.click(async function () {
        if (!isLocked) {
            isLocked = true;

            currentQuestionIndex++;
            if (currentQuestionIndex < questionKeys.length) {
                await initializeQuestion();
            } else {
                await showSummary();
            }
            isLocked = false;
        }
    });

    // Initialize first question
    initializeQuestion();
});

$(document).ready(function () {
    const currentUrl = new URL(window.location.href);

    // Restart
    $("#restartButton").click(() => {
        const lValue = url.searchParams.get("l");
        const newUrl = `../quiz/${randomCode}${lValue ? `?l=${lValue}` : ""}`;
        window.location.href = newUrl;
    });

    // Copy question group code
    const pathSegments = currentUrl.pathname
        .split("/")
        .filter((segment) => segment.trim() !== "");
    const lastSegment = pathSegments[pathSegments.length - 1];
    document.getElementById("last-segment").textContent = lastSegment;

    const $copyButton = $("#copy-button");
    $copyButton.click(() => {
        const lastSegmentContent = $("#last-segment").text();

        navigator.clipboard
            .writeText(lastSegmentContent)
            .then(() => {
                $copyButton.text("check");
                setTimeout(() => {
                    $copyButton.text("content_copy");
                }, 1500);
            })
            .catch((err) => {
                console.error("Failed to copy: ", err);
            });
    });
});
