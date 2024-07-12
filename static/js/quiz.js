$(document).ready(function () {
    let currentQuestionIndex = 0;
    const questionsData = questions || {};
    const questionKeys = Object.keys(questionsData);
    const delayBetweenQuestions = 800;
    const fadeDuration = 300;

    if (questionKeys.length === 0) {
        console.error("No questions available.");
        return;
    }

    const $info = $("#info");
    const $sourceText = $("#sourceText");
    const $keyText = $("#keyText");
    const $inputBox = $("#inputBox");
    const $boxes = $("#boxes");

    function initializeQuestion() {
        const currentKey = questionKeys[currentQuestionIndex];
        const { source, translation } = questionsData[currentKey];

        console.log("当前题目索引：", currentQuestionIndex);
        console.log("当前键名：", currentKey);
        Sentry.captureMessage(`Quiz, ${currentQuestionIndex}`);

        const translationSegments = [...new Intl.Segmenter().segment(translation)].map(segment => segment.segment);
        const translationLength = translationSegments.length;

        $info.fadeOut(fadeDuration, function () {
            $sourceText.text(source);
            $keyText.text(currentKey);

            $inputBox.val("");
            createBoxes(translationLength);

            $info.fadeIn(fadeDuration);
        });
    }

    function getSegmentedText(text) {
        return [...new Intl.Segmenter().segment(text)].map(segment => segment.segment);
    }

    function truncateInput(input, maxLength) {
        const segmentedInput = getSegmentedText(input);
        return segmentedInput.slice(0, maxLength).join('');
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
        const input = $inputBox.val();
        let currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];

        const translationSegments = getSegmentedText(translation);
        const translationLength = translationSegments.length;

        let inputSegments = getSegmentedText(input);

        if (inputSegments.length > translationLength) {
            inputSegments = inputSegments.slice(0, translationLength);
            $inputBox.val(inputSegments.join(''));
        }

        $(".box").each(function (index) {
            const $box = $(this);
            const userInputChar = inputSegments[index] || '';
            const correctChar = translationSegments[index] || '';

            $box.text(userInputChar);

            if (!userInputChar) {
                $box.css("background-color", "#9ca3af25");
            } else if (userInputChar === correctChar) {
                $box.css("background-color", "#79b851");
            } else if (translationSegments.includes(userInputChar)) {
                $box.css("background-color", "#f3c237");
            } else {
                $box.css("background-color", "#9ca3af25");
            }
        });
    }

    function showSummary() {
        $info.add($inputBox).fadeOut(fadeDuration, function () {
            const $summaryBody = $("#summaryBody").empty();

            questionKeys.forEach((key) => {
                const { source, translation } = questionsData[key];
                $("<tr>").append(
                    $("<td>").text(source),
                    $("<td>").text(translation)
                ).appendTo($summaryBody);
            });

            $("#summary").fadeIn(fadeDuration);
        });
    }

    let isComposing = false;

    $inputBox.on('compositionstart', function () {
        isComposing = true;
    });

    $inputBox.on('compositionend', function () {
        isComposing = false;
        updateBoxes();
    });

    function handleInput(input) {
        let currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questionsData[currentKey];

        if (!isComposing) {
            const translationLength = getSegmentedText(translation).length;
            const truncatedValue = truncateInput(input, translationLength);
            $inputBox.val(truncatedValue);
            updateBoxes();
        }

        if (input === translation) {
            $(".box").css("background-color", "#79b851");

            if (currentQuestionIndex === questionKeys.length - 1) {
                setTimeout(showSummary, delayBetweenQuestions);
            } else {
                setTimeout(() => {
                    currentQuestionIndex++;
                    initializeQuestion();
                }, delayBetweenQuestions);
            }
        }
    }

    $inputBox.on('input', function () {
        const input = $(this).val();
        handleInput(input);
    });


    // Initialize first question
    initializeQuestion();
});