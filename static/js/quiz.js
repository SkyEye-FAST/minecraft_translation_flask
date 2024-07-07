$(document).ready(function () {
    let currentQuestionIndex = 0;
    const questions = questionsData;
    const questionKeys = Object.keys(questions);
    const delayBetweenQuestions = 800;

    function createBoxes(length) {
        const boxesDiv = $('#boxes').empty();
        for (let i = 0; i < length; i++) {
            $('<div>', {
                class: 'box',
                id: 'box' + (i + 1)
            }).appendTo(boxesDiv);
        }
    }

    function loadQuestion() {
        const inputBox = $('#inputBox').val('');
        const currentKey = questionKeys[currentQuestionIndex];
        const question = questions[currentKey];
        const sourceText = question.source;
        const translationText = question.translation;

        $('#info').fadeOut(300, function () {
            $('#sourceText').text(sourceText);
            $('#keyText').text(currentKey);

            const questionLength = translationText.length;
            inputBox.attr('maxlength', questionLength);
            createBoxes(questionLength);
            updateBoxes();

            $(this).fadeIn(300);
        });
    }

    function updateBoxes() {
        const input = $('#inputBox').val();
        const currentKey = questionKeys[currentQuestionIndex];
        const correctAnswer = questions[currentKey].translation;

        for (let i = 0; i < correctAnswer.length; i++) {
            const box = $('#box' + (i + 1));
            box.text(input[i] || '');
            if (input[i] === undefined) {
                box.css('background-color', '#9ca3af25');
            } else if (input[i] === correctAnswer[i]) {
                box.css('background-color', '#79b851');
            } else if (correctAnswer.includes(input[i])) {
                box.css('background-color', '#f3c237');
            } else {
                box.css('background-color', '#9ca3af25');
            }
        }

        if (input === correctAnswer) {
            setTimeout(() => {
                currentQuestionIndex++;
                if (currentQuestionIndex < questionKeys.length) {
                    loadQuestion();
                } else {
                    showSummary();
                }
            }, delayBetweenQuestions);
        }
    }

    function showSummary() {
        $('#info, #inputBox').fadeOut(300, function () {
            $(this).hide();
            const summaryTableBody = $('#summaryBody').empty();

            questionKeys.forEach((key) => {
                const question = questions[key];
                const sourceText = question.source;
                const translationText = question.translation;

                const row = $('<tr>').appendTo(summaryTableBody);
                $('<td>').text(sourceText).appendTo(row);
                $('<td>').text(translationText).appendTo(row);
            });

            $('#summary').fadeIn(300);
        });
    }

    $('#restartButton').click(function () {
        window.location.href = `../quiz/${randomCode}`;
    });

    $('#inputBox').on('input', updateBoxes);

    loadQuestion();
});
