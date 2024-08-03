document.addEventListener('DOMContentLoaded', function () {
    var verifyBtn = document.getElementById('verifyBtn');
    var seedBtn = document.getElementById('seedBtn');
    var registerBtn = document.getElementById('registerBtn');
    var loginBtn = document.getElementById('loginBtn');
    var forgetBtn = document.getElementById('forgetBtn');
    var postBtn = document.getElementById('postBtn');



    if (postBtn) {
        postBtn.addEventListener('click', function (e) {
            e.preventDefault();
            console.log('Before grecaptcha.execute');
            console.log('siteKey ',siteKey);
            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'submit'}).then(function (token) {
                    var form = document.getElementById('recaptchaForm');

                    var recaptchaInput = document.createElement('input');
                    recaptchaInput.type = 'hidden';
                    recaptchaInput.name = 'g-recaptcha-response';
                    recaptchaInput.value = token;
                    form.appendChild(recaptchaInput);

                    var contentInput = document.createElement('input');
                    contentInput.type = 'hidden';
                    contentInput.name = 'postContent';
                    contentInput.value = editor.getMarkdown();
                    form.appendChild(contentInput);

                    form.submit();
                });
            });
        });
    }


    if (verifyBtn) {
        verifyBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var actionValue = e.currentTarget.value;
            console.log('Before grecaptcha.execute');
            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'submit'}).then(function (token) {
                    var form = document.getElementById('recaptchaForm');
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'g-recaptcha-response';
                    input.value = token;
                    form.appendChild(input);

                    var actionInput = document.createElement('input');
                    actionInput.type = 'hidden';
                    actionInput.name = 'action';
                    actionInput.value = actionValue;
                    form.appendChild(actionInput);

                    form.submit();
                });
            });
        });
    }

    if (seedBtn) {
        seedBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var actionValue = e.currentTarget.value;
            console.log('Before grecaptcha.execute');
            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'submit'}).then(function (token) {
                    var form = document.getElementById('recaptchaForm');
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'g-recaptcha-response';
                    input.value = token;
                    form.appendChild(input);

                    var actionInput = document.createElement('input');
                    actionInput.type = 'hidden';
                    actionInput.name = 'action';
                    actionInput.value = actionValue;
                    form.appendChild(actionInput);

                    form.submit();
                });
            });
        });
    }

    if (registerBtn) {
        registerBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var actionValue = e.currentTarget.value;
            console.log('Before grecaptcha.execute');
            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'submit'}).then(function (token) {
                    var form = document.getElementById('recaptchaForm');
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'g-recaptcha-response';
                    input.value = token;
                    form.appendChild(input);

                    var actionInput = document.createElement('input');
                    actionInput.type = 'hidden';
                    actionInput.name = 'action';
                    actionInput.value = actionValue;
                    form.appendChild(actionInput);

                    form.submit();
                });
            });
        });
    }

    if (loginBtn) {
        loginBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var actionValue = e.currentTarget.value;
            console.log('Before grecaptcha.execute');
            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'submit'}).then(function (token) {
                    var form = document.getElementById('recaptchaForm');
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'g-recaptcha-response';
                    input.value = token;
                    form.appendChild(input);

                    var actionInput = document.createElement('input');
                    actionInput.type = 'hidden';
                    actionInput.name = 'action';
                    actionInput.value = actionValue;
                    form.appendChild(actionInput);

                    form.submit();
                });
            });
        });
    }

    if (forgetBtn) {
        forgetBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var actionValue = e.currentTarget.value;
            console.log('Before grecaptcha.execute');
            grecaptcha.ready(function () {
                grecaptcha.execute(siteKey, {action: 'submit'}).then(function (token) {
                    var form = document.getElementById('recaptchaForm');
                    var input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'g-recaptcha-response';
                    input.value = token;
                    form.appendChild(input);

                    var actionInput = document.createElement('input');
                    actionInput.type = 'hidden';
                    actionInput.name = 'action';
                    actionInput.value = actionValue;
                    form.appendChild(actionInput);

                    form.submit();
                });
            });
        });
    }
});
