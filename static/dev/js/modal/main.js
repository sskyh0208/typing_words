/******************** ログインモーダル ********************/
const openLogin = document.getElementById('open-login');
const modalLogin = document.getElementById('modal-login');
const maskLogin = document.getElementById('mask-login');

openLogin.addEventListener('click', function () {
    modalLogin.classList.remove('hidden');
    maskLogin.classList.remove('hidden');
});
maskLogin.addEventListener('click', function () {
    modalLogin.classList.add('hidden');
    maskLogin.classList.add('hidden');
});

/******************** 新規登録モーダル ********************/
const openRegist = document.getElementById('open-regist');
const modalRegist = document.getElementById('modal-regist');
const maskRegist = document.getElementById('mask-regist');

openRegist.addEventListener('click', function () {
    modalRegist.classList.remove('hidden');
    maskRegist.classList.remove('hidden');
});
maskRegist.addEventListener('click', function () {
    modalRegist.classList.add('hidden');
    maskRegist.classList.add('hidden');
});

/******************** メッセージモーダル ********************/
const modalMessage = document.getElementById('modal-message');
const maskMessage = document.getElementById('mask-message');

maskMessage.addEventListener('click', function () {
    modalMessage.classList.add('hidden');
    maskMessage.classList.add('hidden');
    cleanShowMessage();
});

/******************** メッセージモーダル関連 ********************/
function generateShowMessage(message) {
    var messageBody = document.getElementById('message-body');
    var p = document.createElement('p');
    p.textContent = message;
    messageBody.appendChild(p);
};

function cleanShowMessage() {
    var messageBody = document.getElementById('message-body');
    while(messageBody.firstChild) {
        messageBody.removeChild(messageBody.firstChild);
    }
}

/******************** ログイン処理 ********************/
$('#form-login').submit(function(e) {
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        type: 'POST',
        url: loginUrl,
        data: $('#form-login').serialize(),
        success: function(data, status, xhr) {
            if (data.success == false) {
                // ログイン失敗
                cleanShowMessage();
                generateShowMessage(data.message);
                // ログインモーダルを非表示
                modalLogin.classList.add('hidden');
                maskLogin.classList.add('hidden');
                setTimeout(() => {
                    // メッセージモーダルを表示
                    modalMessage.classList.remove('hidden');
                    maskMessage.classList.remove('hidden');
                }, 200)
            } else if (data.success) {
                // ログイン成功
                modalLogin.classList.add('hidden');
                maskLogin.classList.add('hidden');
                setTimeout(() => {
                    window.location.reload();
                }, 200)
            }
        }
    });
    e.preventDefault();
});

/********************  新規登録処理 ********************/
$('#form-regist').submit(function(e) {
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        type: 'POST',
        url: registUrl,
        data: $('#form-regist').serialize(),
        success: function(data, status, xhr) {
            if (data.success == false) {
                // 新規登録失敗
                cleanShowMessage();
                // ValidationErrorをすべて表示
                for (const msg of data.message) {
                    generateShowMessage(msg);
                }
                // 新規登録モーダルを非表示
                modalRegist.classList.add('hidden');
                maskRegist.classList.add('hidden');
                setTimeout(() => {
                    // メッセージモーダルを表示
                    modalMessage.classList.remove('hidden');
                    maskMessage.classList.remove('hidden');
                }, 200)
            } else if (data.success) {
                // 新規登録成功
                cleanShowMessage();
                for (const msg of data.message) {
                    generateShowMessage(msg);
                }
                modalRegist.classList.add('hidden');
                maskRegist.classList.add('hidden');
                setTimeout(() => {
                    // メッセージモーダルを表示
                    modalMessage.classList.remove('hidden');
                    maskMessage.classList.remove('hidden');
                }, 200)
            }
        }
    });
    e.preventDefault();
});