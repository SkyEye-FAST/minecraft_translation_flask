// 判断是否需要显示查询语言
document.getElementById('query-mode').addEventListener('change', function () {
    var queryLangLabel = document.querySelector('label[for="query-lang"]');
    var queryLangSelect = document.querySelector('select[name="query-lang"]');

    if (this.value === 'transl') {
        queryLangLabel.style.display = 'inherit';
        queryLangSelect.style.display = 'inherit';
    } else {
        queryLangLabel.style.display = 'none';
        queryLangSelect.style.display = 'none';
    }
});

// 折叠 fieldset
document.addEventListener("DOMContentLoaded", function () {
    const fieldsets = document.querySelectorAll(".collapsible");

    fieldsets.forEach(fieldset => {
        const button = fieldset.querySelector(".toggle-button");
        const fieldsetId = fieldset.id;
        const isCollapsed = localStorage.getItem(fieldsetId) === "false";

        if (isCollapsed) {
            fieldset.classList.add("collapsed");
        } else {
            fieldset.classList.remove("collapsed");
        }

        button.addEventListener("click", () => {
            fieldset.classList.toggle("collapsed");
            const state = fieldset.classList.contains("collapsed");
            localStorage.setItem(fieldsetId, state);
        });
    });
});

// 应用亮暗模式
function applyMode(mode) {
    document.body.style.display = 'flex';  // 显示页面
    const icon = document.getElementById('mode-icon');
    const button = document.getElementById('mode-switch');
    const links = document.querySelectorAll('.table-link, .toggle-button');
    const svgContainer = document.getElementById('svg-container');

    if (mode === 'dark') {
        document.body.classList.add('dark-mode');
        icon.textContent = 'light_mode';
        button.style.color = '#f9f2e0';
        links.forEach(link => link.style.color = '#f9f2e0');
        svgContainer.classList.add('invert');
    } else {
        document.body.classList.remove('dark-mode');
        icon.textContent = 'dark_mode';
        button.style.color = '#000';
        links.forEach(link => link.style.color = '#000');
        svgContainer.classList.remove('invert');
    }
}

// 切换亮暗模式
function toggleMode() {
    const icon = document.getElementById('mode-icon');
    const button = document.getElementById('mode-switch');
    const links = document.querySelectorAll('.table-link, .toggle-button');
    const svgContainer = document.getElementById('svg-container');
    document.body.classList.toggle('dark-mode');
    svgContainer.classList.toggle('invert');

    if (document.body.classList.contains('dark-mode')) {
        icon.textContent = 'light_mode';
        button.style.color = '#f9f2e0';
        links.forEach(link => link.style.color = '#f9f2e0');
        localStorage.setItem('mode', 'dark');
    } else {
        icon.textContent = 'dark_mode';
        button.style.color = '#000';
        links.forEach(link => link.style.color = '#000');
        localStorage.setItem('mode', 'light');
    }
}

window.onload = function () {
    const savedMode = localStorage.getItem('mode') || 'light';
    applyMode(savedMode);
}