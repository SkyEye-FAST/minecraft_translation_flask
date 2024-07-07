$(document).ready(function () {
    // 切换亮暗模式
    function toggleMode() {
        $('body').toggleClass('dark-mode');
        const isDarkMode = $('body').hasClass('dark-mode');
        localStorage.setItem('mode', isDarkMode ? 'dark' : 'light');
        updateModeElements(isDarkMode);
    }

    // 更新亮暗模式相关的元素
    function updateModeElements(isDarkMode) {
        const icon = $('#mode-icon');
        const button = $('#mode-switch');
        const links = $('.table-link, .toggle-button');
        const svgContainer = $('#svg-container');

        if (isDarkMode) {
            icon.text('light_mode');
            button.css('color', '#f9f2e0');
            links.css('color', '#f9f2e0');
            svgContainer.addClass('invert');
        } else {
            icon.text('dark_mode');
            button.css('color', '#000');
            links.css('color', '#000');
            svgContainer.removeClass('invert');
        }
    }

    // 页面加载完成时应用保存的模式
    const savedMode = localStorage.getItem('mode') || 'light';
    const isDarkMode = savedMode === 'dark';
    $('body').toggleClass('dark-mode', isDarkMode);
    updateModeElements(isDarkMode);

    // 为切换按钮绑定点击事件
    $('#mode-switch').click(toggleMode);

    // 折叠 fieldset
    $('.collapsible').each(function () {
        const $fieldset = $(this);
        $fieldset.find('.toggle-button').on('click', function () {
            $fieldset.toggleClass('collapsed');
        });
    });

    // 判断是否需要显示查询语言
    $('#query-mode').change(function () {
        const queryLangLabel = $('label[for="query-lang"]');
        const queryLangSelect = $('select[name="query-lang"]');

        if ($(this).val() === 'transl') {
            queryLangLabel.removeClass('hidden');
            queryLangSelect.removeClass('hidden');
        } else {
            queryLangLabel.addClass('hidden');
            queryLangSelect.addClass('hidden');
        }
    });
});
