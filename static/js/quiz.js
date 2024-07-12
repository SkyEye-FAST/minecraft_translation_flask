$(document).ready(function () {
    let currentQuestionIndex = 0;
    const questionsData = questions || {}; // Assuming questions is defined elsewhere
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

    // Initialize question
    function initializeQuestion() {
        const currentKey = questionKeys[currentQuestionIndex];
        const { source, translation } = questionsData[currentKey];

        const translationChars = Array.from(translation);
        const translationLength = translationChars.length;

        $info.fadeOut(fadeDuration, function () {
            $sourceText.text(source);
            $keyText.text(currentKey);

            $inputBox.val("").attr("maxlength", translationLength * 2);
            createBoxes(translationLength);

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
        const { translation } = questionsData[currentKey];

        const inputChars = Array.from(input);
        const translationChars = Array.from(translation);

        if (inputChars.length > translationChars.length) {
            inputChars.length = translationChars.length;
            $inputBox.val(inputChars.join(''));
        }

        $(".box").each(function (index) {
            const $box = $(this);
            const userInputChar = inputChars[index] || '';
            const correctChar = translationChars[index] || '';

            $box.text(userInputChar);

            if (!userInputChar) {
                $box.css("background-color", "#9ca3af25");
            } else if (userInputChar === correctChar) {
                $box.css("background-color", "#79b851");
            } else if (translationChars.includes(userInputChar)) {
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
                const { source, translation } = questionsData[key];
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
        const { translation } = questionsData[currentKey];

        if (input === translation) {
            $(".box").css("background-color", "#79b851");

            if (currentQuestionIndex === questionKeys.length - 1) {
                setTimeout(showSummary, delayBetweenQuestions);
            } else {
                currentQuestionIndex++;
                setTimeout(() => {
                    initializeQuestion();
                }, delayBetweenQuestions);
            }
        }
    });

    // Initialize first question
    initializeQuestion();
});
