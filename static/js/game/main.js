var windowWidth = $(window).width();
var windowSm = 600;
if (windowWidth <= windowSm) {
    //横幅768px以下（スマホ）に適用させるJavaScriptを記述
    document.getElementById('score').remove()
    var tap = new Tap(words);
    tap.startGame();
    document.getElementById('typing').addEventListener('touchstart', function(e){
        if (!tap.gameOver) {
            tap.tapCard();
            if (tap.gameOver) {
                // 最後の文字を表示させてから
                tap.endGame();
            }
        } else {
            window.history.back(-1);
        }
    });

} else {
    //横幅768px以上（PC、タブレット）に適用させるJavaScriptを記述
    var typing = new Typing(words, wordbook);
    typing.startGame();
    
    document.addEventListener('keydown', function(e){
        if (!typing.gameOver) {
            typing.checkTypedKey(e);
            if (typing.gameOver) {
                document.removeEventListener('keydown', function(e){});
                // 最後の文字を表示させてから
                setTimeout(() => {
                    typing.endGame();
                }, 300);
            }
        }
    });
}
