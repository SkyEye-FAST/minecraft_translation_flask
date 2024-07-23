$(document).ready(() => {
    // 折叠 fieldset
    $(".collapsible").on("click", ".toggle-button", function () {
        $(this).closest(".collapsible").toggleClass("collapsed");
    });

    // 判断是否需要显示查询语言
    const queryLangLabel = $('label[for="query-lang"]');
    const queryLangSelect = $('select[name="query-lang"]');
    const toggleQueryLangVisibility = (isVisible) => {
        queryLangLabel.toggleClass("hidden", !isVisible);
        queryLangSelect.toggleClass("hidden", !isVisible);
    };

    $("#query-mode").change(function () {
        toggleQueryLangVisibility($(this).val() === "transl");
    });
});
