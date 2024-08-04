$(document).ready(() => {
    const body = $("body");
    const $info = $("#info");
    const $sourceText = $("#sourceText");
    const $keyText = $("#keyText");
    const $questionRatingNum = $("#questionRatingNum");
    const $questionRating = $("#questionRating");
    const $inputBox = $("#inputBox");
    const $boxes = $("#boxes");
    const $buttons = $("#buttons");
    const $hintButton = $("#hintButton");
    const $skipButton = $("#skipButton");
    const $summary = $("#summary");

    let currentQuestionIndex = 0;
    let score = 0;
    let questionScore = 10;
    const questionsData = questions || {};
    const questionKeys = Object.keys(questionsData);

    if (!questionKeys.length) {
        console.error("No questions available.");
        return;
    }

    const currentUrl = new URL(window.location.href);
    const lang = currentUrl.searchParams.get("l");
    const fadeDuration = 300;
    const delayBetweenQuestions = 800;
    let isLocked = false;
    let isComposing = false;

    const charStates = {};

    const toggleDarkMode = () => {
        body.toggleClass("dark-mode");
        $("#summaryBody span").toggleClass("dark", body.hasClass("dark-mode"));

        if ($summary.is(":hidden")) {
            updateBoxes();
        }
    };

    body.on("toggle-dark-mode", toggleDarkMode);
    $("#mode-switch").click(() => body.trigger("toggle-dark-mode"));

    const getSegmentedText = (text) =>
        [...new Intl.Segmenter().segment(text)].map((seg) => seg.segment);
    const truncateInput = (input, maxLength) =>
        getSegmentedText(input).slice(0, maxLength).join("");

    const createBoxes = (length) => {
        $boxes.empty();
        for (let i = 0; i < length; i++) {
            $("<div>", { class: "box", id: `box${i + 1}` }).appendTo($boxes);
        }
    };

    const fadeElement = ($element, type) =>
        new Promise((resolve) => $element[type](fadeDuration, resolve));
    const delay = (duration) =>
        new Promise((resolve) => setTimeout(resolve, duration));

    const updateBoxes = () => {
        const isDarkMode = body.hasClass("dark-mode");
        const input = $inputBox.val();
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];
        const translationSegments = getSegmentedText(translation);
        let inputSegments = getSegmentedText(input).slice(
            0,
            translationSegments.length
        );

        $inputBox.val(inputSegments.join(""));
        $(".box").each((index, box) => {
            const $box = $(box);
            const userInputChar = inputSegments[index] || "";
            const correctChar = translationSegments[index] || "";
            const hintChar = $box.data("hint");

            const boxClass = hintChar
                ? `box hinted${
                      userInputChar === correctChar ? " correct" : ""
                  }${isDarkMode ? " dark" : ""}`
                : `box${
                      !userInputChar
                          ? ""
                          : userInputChar === correctChar
                          ? " correct"
                          : translationSegments.includes(userInputChar)
                          ? " exist"
                          : ""
                  }${isDarkMode ? " dark" : ""}`;

            $box.text(hintChar || userInputChar).attr("class", boxClass);

            if (!charStates[currentKey]) charStates[currentKey] = [];
            charStates[currentKey][index] = $box.attr("class");
        });
    };

    const updateRatingStars = (rating) => {
        $questionRating.empty();
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 > 0;

        for (let i = 0; i < fullStars; i++) {
            $questionRating.append(
                $('<span class="material-symbols-outlined b">').text("star")
            );
        }

        if (hasHalfStar) {
            $questionRating.append(
                $('<span class="material-symbols-outlined b">').text(
                    "star_half"
                )
            );
        }

        $("#questionRatingNum").text(rating.toFixed(2));
    };

    const initializeQuestion = async () => {
        const currentKey = questionKeys[currentQuestionIndex];
        questionScore = 10;
        const { source, translation, rating } =
            lang === "zh_cn"
                ? questionsData[currentKey]
                : { ...questionsData[currentKey], rating: undefined };

        const translationSegments = getSegmentedText(translation);
        await fadeElement($info, "fadeOut");
        $skipButton.hide();
        $hintButton.show();

        $sourceText.text(source);
        $keyText.text(currentKey);
        if (rating !== undefined) {
            $questionRatingNum.text(rating);
            updateRatingStars(rating);
        }
        $inputBox.val("");
        createBoxes(translationSegments.length);

        await fadeElement($info, "fadeIn");
    };

    const showSummary = async () => {
        await fadeElement($info.add($inputBox).add($buttons), "fadeOut");
        const isDarkMode = body.hasClass("dark-mode");
        const $summaryBody = $("#summaryBody").empty();
        let level = 0;

        questionKeys.forEach((key) => {
            const { source, translation, rating } =
                lang === "zh_cn"
                    ? questionsData[key]
                    : { ...questionsData[key], rating: undefined };
            if (lang === "zh_cn") level += rating;

            const translationSegments = getSegmentedText(translation);
            const $translationTd = $("<td>");

            translationSegments.forEach((char, index) => {
                const span = $("<span>").text(char);
                if (charStates[key] && charStates[key][index]) {
                    span.addClass(
                        charStates[key][index].replace(
                            "box",
                            `transl${isDarkMode ? " dark" : ""}`
                        )
                    );
                }
                $translationTd.append(span);
            });

            $("<tr>")
                .append($("<td>").text(source), $translationTd)
                .appendTo($summaryBody);
        });

        if (lang === "zh_cn") {
            $("#levelNum").text(level.toFixed(2));
            $("#score").text(`${score.toFixed(2)} pts`);
        } else {
            $("#level").hide();
        }

        await fadeElement($summary, "fadeIn");
    };

    const check = async () => {
        if (isComposing || isLocked) return;

        let input = $inputBox.val();
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];
        const translationLength = getSegmentedText(translation).length;

        input = truncateInput(input, translationLength);

        $inputBox.val(input);
        updateBoxes();

        const remainingHintableCount =
            $(".box").not(".correct, .hinted").length;
        $hintButton.toggle(remainingHintableCount > 1);
        $skipButton.toggle(remainingHintableCount <= 1);

        if (input === translation && !isLocked) {
            isLocked = true;
            $skipButton.attr("disabled", true);
            score += questionScore;
            await delay(delayBetweenQuestions);

            if (currentQuestionIndex === questionKeys.length - 1) {
                await showSummary();
            } else {
                await fadeElement($info, "fadeOut");
                currentQuestionIndex++;
                $skipButton.removeAttr("disabled");
                await initializeQuestion();
            }
            isLocked = false;
        }
    };

    $inputBox.on({
        compositionstart: () => {
            isComposing = true;
        },
        compositionend: () => {
            isComposing = false;
            check();
        },
        input: check,
    });

    $hintButton.click(() => {
        if (isLocked) return;

        isLocked = true;
        const isDarkMode = body.hasClass("dark-mode");
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];
        const translationSegments = getSegmentedText(translation);

        const hintedIndex = $(".box").not(".correct, .hinted").first().index();

        if (hintedIndex !== -1) {
            const correctChar = translationSegments[hintedIndex];
            const $hintedBox = $(".box").eq(hintedIndex);

            if ($hintedBox.hasClass("exist")) {
                $hintedBox.removeClass("exist");
            }

            $hintedBox
                .text(correctChar)
                .data("hint", correctChar)
                .addClass(`hinted${isDarkMode ? " dark" : ""}`);

            questionScore =
                10 * (1 - $(".box.hinted").length / $(".box").length);

            $(".box").each(function (index) {
                const $box = $(this);
                if (!charStates[currentKey]) charStates[currentKey] = [];
                charStates[currentKey][index] = $box.attr("class");
            });

            const remainingHintableCount =
                $(".box").not(".correct, .hinted").length;
            $hintButton.toggle(remainingHintableCount > 1);
            $skipButton.toggle(remainingHintableCount <= 1);
        }

        isLocked = false;
    });

    $skipButton.click(async () => {
        if (isLocked) return;
        isLocked = true;

        const currentKey = questionKeys[currentQuestionIndex];
        $(".box").each(function (index) {
            const $box = $(this);
            if (!charStates[currentKey]) charStates[currentKey] = [];
            charStates[currentKey][index] = $box.attr("class");
        });

        currentQuestionIndex++;
        if (currentQuestionIndex < questionKeys.length) {
            await initializeQuestion();
        } else {
            await showSummary();
        }
        isLocked = false;
    });

    // Initialize first question
    initializeQuestion();
});

$(document).ready(() => {
    const titleToShare = title || "Minecraft Standard Translation Quiz";
    const textToShare = text || "Test your mastery of standard translations...";
    const currentUrl = new URL(window.location.href);
    const lastSegment = currentUrl.pathname
        .split("/")
        .filter((seg) => seg.trim())
        .pop();
    $("#last-segment").text(lastSegment);

    $("#restartButton").click(() => {
        const lValue = currentUrl.searchParams.get("l");
        window.location.href = `../quiz/${randomCode}${
            lValue ? `?l=${lValue}` : ""
        }`;
    });

    const $copyButton = $("#copy-button");
    $copyButton.click(() => {
        const lastSegmentContent = $("#last-segment").text();
        navigator.clipboard
            .writeText(lastSegmentContent)
            .then(() => {
                $copyButton.text("check");
                setTimeout(() => $copyButton.text("content_copy"), 1500);
            })
            .catch((err) => console.error("Failed to copy: ", err));
    });

    $("#share-button").click(() => {
        if (navigator.share) {
            navigator
                .share({
                    title: titleToShare,
                    text: textToShare,
                    url: window.location.href,
                })
                .then(() => console.log("Shared successfully!"))
                .catch((error) => console.log("Failed to share:", error));
        }
    });
});
