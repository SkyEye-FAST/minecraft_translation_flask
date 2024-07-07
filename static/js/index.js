$(document).ready(function () {
    // 判断是否需要显示查询语言
    $('#query-mode').change(function () {
        var queryLangLabel = $('label[for="query-lang"]');
        var queryLangSelect = $('select[name="query-lang"]');

        if ($(this).val() === 'transl') {
            queryLangLabel.removeClass('hidden');
            queryLangSelect.removeClass('hidden');
        } else {
            queryLangLabel.addClass('hidden');
            queryLangSelect.addClass('hidden');
        }
    });

    // 折叠 fieldset
    $('.collapsible').each(function () {
        var $fieldset = $(this);
        var fieldsetId = $fieldset.attr('id');
        var isCollapsed = localStorage.getItem(fieldsetId) === 'true';

        if (isCollapsed) {
            $fieldset.addClass('collapsed');
        }

        $fieldset.find('.toggle-button').on('click', function () {
            $fieldset.toggleClass('collapsed');
            var state = $fieldset.hasClass('collapsed');
            localStorage.setItem(fieldsetId, state.toString());
        });
    });

    // 应用亮暗模式
    function applyMode(mode) {
        $('body').css('display', 'flex');  // 显示页面
        var icon = $('#mode-icon');
        var button = $('#mode-switch');
        var links = $('.table-link, .toggle-button');
        var svgContainer = $('#svg-container');

        if (mode === 'dark') {
            $('body').addClass('dark-mode');
            icon.text('light_mode');
            button.css('color', '#f9f2e0');
            links.css('color', '#f9f2e0');
            svgContainer.addClass('invert');
        } else {
            $('body').removeClass('dark-mode');
            icon.text('dark_mode');
            button.css('color', '#000');
            links.css('color', '#000');
            svgContainer.removeClass('invert');
        }
    }

    // 切换亮暗模式
    function toggleMode() {
        var icon = $('#mode-icon');
        var button = $('#mode-switch');
        var links = $('.table-link, .toggle-button');
        var svgContainer = $('#svg-container');
        $('body').toggleClass('dark-mode');
        svgContainer.toggleClass('invert');

        if ($('body').hasClass('dark-mode')) {
            icon.text('light_mode');
            button.css('color', '#f9f2e0');
            links.css('color', '#f9f2e0');
            localStorage.setItem('mode', 'dark');
        } else {
            icon.text('dark_mode');
            button.css('color', '#000');
            links.css('color', '#000');
            localStorage.setItem('mode', 'light');
        }
    }

    // 页面加载完成时应用保存的模式
    var savedMode = localStorage.getItem('mode') || 'light';
    applyMode(savedMode);

    // 为切换按钮绑定点击事件
    $('#mode-switch').click(function () {
        toggleMode();
    });
});
