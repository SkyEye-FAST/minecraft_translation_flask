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

    // 初始化题目
    function initializeQuestion() {
        const currentKey = questionKeys[currentQuestionIndex];
        const question = questions[currentKey];
        const translationLength = question.translation.length;

        $("#info").fadeOut(fadeDuration, function () {
            $("#sourceText").text(question.source);
            $("#keyText").text(currentKey);

            $("#info").fadeIn(fadeDuration);
        });

        $("#inputBox").val("").attr("maxlength", translationLength);
        createBoxes(translationLength);
    }

    // 创建相应长度的 box
    function createBoxes(length) {
        const boxesDiv = $("#boxes").empty();
        for (let i = 0; i < length; i++) {
            $("<div>", {
                class: "box",
                id: "box" + (i + 1),
            }).appendTo(boxesDiv);
        }
    }

    // 更新 box 显示状态
    function updateBoxes() {
        const input = $("#inputBox").val();
        const currentKey = questionKeys[currentQuestionIndex];
        const correctAnswer = questions[currentKey].translation;

        $(".box").each(function (index) {
            const box = $(this);
            const userInput = input[index];
            const correctChar = correctAnswer[index];

            box.text(userInput || "");

            if (!userInput) {
                box.css("background-color", "#9ca3af25");
            } else if (userInput === correctChar) {
                box.css("background-color", "#79b851");
            } else if (correctAnswer.includes(userInput)) {
                box.css("background-color", "#f3c237");
            } else {
                box.css("background-color", "#9ca3af25");
            }
        });
    }

    // 显示总结信息
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

    // 处理输入框内容变化事件
    $("#inputBox").on("input", function () {
        updateBoxes();

        const input = $(this).val();
        const currentKey = questionKeys[currentQuestionIndex];
        const correctAnswer = questions[currentKey].translation;

        if (input === correctAnswer) {
            $(".box").css("background-color", "#79b851");

            if (currentQuestionIndex === questionKeys.length - 1) {
                setTimeout(showSummary, delayBetweenQuestions);
            } else {
                currentQuestionIndex++;
                setTimeout(initializeQuestion, delayBetweenQuestions);
            }
        }
    });

    // 初始化第一个题目
    initializeQuestion();
});
