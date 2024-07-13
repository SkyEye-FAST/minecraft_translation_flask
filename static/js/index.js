$(document).ready(function () {
    // 折叠 fieldset
    $(".collapsible").each(function () {
        const $fieldset = $(this);
        $fieldset.find(".toggle-button").on("click", function () {
            $fieldset.toggleClass("collapsed");
        });
    });

    // 判断是否需要显示查询语言
    $("#query-mode").change(function () {
        const queryLangLabel = $('label[for="query-lang"]');
        const queryLangSelect = $('select[name="query-lang"]');

        if ($(this).val() === "transl") {
            queryLangLabel.removeClass("hidden");
            queryLangSelect.removeClass("hidden");
        } else {
            queryLangLabel.addClass("hidden");
            queryLangSelect.addClass("hidden");
        }
    });
});
