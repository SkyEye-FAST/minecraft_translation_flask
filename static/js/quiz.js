$(document).ready(function () {
    let currentQuestionIndex = 0;
    const questions = questionsData || {};
    const questionKeys = Object.keys(questions);
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

    // Initialize question
    function initializeQuestion() {
        const currentKey = questionKeys[currentQuestionIndex];
        const { source, translation } = questions[currentKey];

        console.log("当前题目索引：", currentQuestionIndex);
        console.log("当前键名：", currentKey);
        Sentry.captureMessage(`Quiz, ${currentQuestionIndex}`);

        $info.fadeOut(fadeDuration, function () {
            $sourceText.text(source);
            $keyText.text(currentKey);

            $inputBox.val("").attr("maxlength", translation.length);
            createBoxes(translation.length);

            $info.fadeIn(fadeDuration);
        });
    }

    // Create boxes based on length
    function createBoxes(length) {
        $boxes.empty();
        for (let i = 0; i < length; i++) {
            $("<div>", {
                class: "box",
                id: "box" + (i + 1),
            }).appendTo($boxes);
        }
    }

    // Update box display based on user input
    function updateBoxes() {
        const input = $inputBox.val();
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questions[currentKey];

        $(".box").each(function (index) {
            const $box = $(this);
            const userInput = input[index];
            const correctChar = translation[index];

            $box.text(userInput || "");

            if (!userInput) {
                $box.css("background-color", "#9ca3af25");
            } else if (userInput === correctChar) {
                $box.css("background-color", "#79b851");
            } else if (translation.includes(userInput)) {
                $box.css("background-color", "#f3c237");
            } else {
                $box.css("background-color", "#9ca3af25");
            }
        });
    }

    // Show summary after completing all questions
    function showSummary() {
        $info.add($inputBox).fadeOut(fadeDuration, function () {
            const $summaryBody = $("#summaryBody").empty();

            questionKeys.forEach((key) => {
                const { source, translation } = questions[key];
                $("<tr>").append(
                    $("<td>").text(source),
                    $("<td>").text(translation)
                ).appendTo($summaryBody);
            });

            $("#summary").fadeIn(fadeDuration);
        });
    }

    // Handle input change event
    $inputBox.on("input", function () {
        updateBoxes();

        const input = $(this).val();
        const currentKey = questionKeys[currentQuestionIndex];
        const { translation } = questions[currentKey];

        if (input === translation) {
            $(".box").css("background-color", "#79b851");

            if (currentQuestionIndex === questionKeys.length - 1) {
                setTimeout(showSummary, delayBetweenQuestions);
            } else {
                currentQuestionIndex++;
                setTimeout(initializeQuestion, delayBetweenQuestions);
            }
        }
    });

    // Initialize first question
    initializeQuestion();
});
