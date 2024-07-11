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

    function createBoxes(length) {
        const boxesDiv = $("#boxes").empty();
        for (let i = 0; i < length; i++) {
            $("<div>", {
                class: "box",
                id: "box" + (i + 1),
            }).appendTo(boxesDiv);
        }
    }

    function loadQuestion() {
        $("#inputBox").val("");

        const currentKey = questionKeys[currentQuestionIndex];
        const question = questions[currentKey];
        const sourceText = question.source;
        const translationText = question.translation;

        console.log("当前题目索引：", currentQuestionIndex);
        console.log("当前键名：", currentKey);
        Sentry.captureMessage(`Quiz, ${currentQuestionIndex}`);

        $("#info").fadeOut(fadeDuration, function () {
            $("#sourceText").text(sourceText);
            $("#keyText").text(currentKey);

            const questionLength = translationText.length;
            $("#inputBox").attr("maxlength", questionLength);
            createBoxes(questionLength);
            updateBoxes();

            $(this).fadeIn(fadeDuration);
        });
    }

    function updateBoxes() {
        const input = $("#inputBox").val();
        const currentKey = questionKeys[currentQuestionIndex];
        const correctAnswer = questions[currentKey].translation;

        for (let i = 0; i < correctAnswer.length; i++) {
            const box = $("#box" + (i + 1));
            box.text(input[i] || "");
            if (input[i] === undefined) {
                box.css("background-color", "#9ca3af25");
            } else if (input[i] === correctAnswer[i]) {
                box.css("background-color", "#79b851");
            } else if (correctAnswer.includes(input[i])) {
                box.css("background-color", "#f3c237");
            } else {
                box.css("background-color", "#9ca3af25");
            }
        }
    }

    function showSummary() {
        $("#info, #inputBox").fadeOut(fadeDuration, function () {
            const summaryTableBody = $("#summaryBody").empty();

            questionKeys.forEach((key) => {
                const question = questions[key];
                const sourceText = question.source;
                const translationText = question.translation;

                const row = $("<tr>").appendTo(summaryTableBody);
                $("<td>").text(sourceText).appendTo(row);
                $("<td>").text(translationText).appendTo(row);
            });

            $("#summary").fadeIn(fadeDuration);
        });
    }

    $("#restartButton").click(function () {
        window.location.href = `../quiz/${randomCode}`;
    });

    $("#inputBox").on("input", updateBoxes);

    $("#inputBox").on("input", function () {
        const input = $(this).val();
        const currentKey = questionKeys[currentQuestionIndex];
        const correctAnswer = questions[currentKey].translation;

        if (input === correctAnswer) {
            for (let i = 0; i < correctAnswer.length; i++) {
                const box = $("#box" + (i + 1));
                box.css("background-color", "#79b851");
            }
            if ((currentQuestionIndex + 1) === questionKeys.length) {
                setTimeout(() => {
                    showSummary();
                }, delayBetweenQuestions);
            } else {
                currentQuestionIndex++;
                setTimeout(() => {
                    loadQuestion();
                }, delayBetweenQuestions);
            }
        }
    });

    // 加载首个题目
    loadQuestion();
});

$(document).ready(function () {
    var currentUrl = window.location.href;
    var match = currentUrl.match(/\/([^\/?#]+)[\/?#]?$/);
    var lastSegment = match ? match[1] : "";
    document.getElementById("last-segment").textContent = lastSegment;

    $("#copy-button").click(function () {
        var $copyButton = $(this);
        var $lastSegment = $("#last-segment");
        var lastSegmentContent = $lastSegment.text();

        navigator.clipboard
            .writeText(lastSegmentContent)
            .then(function () {
                $copyButton.text("check");
                setTimeout(function () {
                    $copyButton.text("content_copy");
                }, 1500);
            })
            .catch(function (err) {
                console.error("Failed to copy: ", err);
            });
    });
});
