function bindEmailCaptchaClick() {
  $("#captcha-btn").click(function (event) {
    // $this：代表的是当前按钮的jquery对象
    var $this = $(this);
    // 阻止默认的事件
    event.preventDefault();

    var email = $("input[name='email']").val();
    var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // 验证邮箱格式
    if (!emailPattern.test(email)) {
      $("#emailError").text("邮箱格式错误,请输入正确的邮箱").show();
      return;
    } else {
      $("#emailError").hide();
    }

    $.ajax({
      url: "/auth/captcha/email?email=" + email,
      method: "GET",
      success: function (result) {
        var code = result['code'];
        if (code == 200) {
          var countdown = 60;
          // 开始倒计时之前，就取消按钮的点击事件
          $this.off("click");
          var timer = setInterval(function () {
            $this.text(countdown);
            countdown -= 1;
            // 倒计时结束的时候执行
            if (countdown <= 0) {
              // 清掉定时器
              clearInterval(timer);
              // 将按钮的文字重新修改回来
              $this.text("获取验证码");
              // 重新绑定点击事件
              bindEmailCaptchaClick();
            }
          }, 1000);
          alert("邮箱验证码发送成功！");
        } else {
          alert(result['message']);
        }
      },
      fail: function (error) {
        console.log(error);
      }
    });
  });
}

// 整个网页都加载完毕后再执行的
$(function () {
  bindEmailCaptchaClick();
});