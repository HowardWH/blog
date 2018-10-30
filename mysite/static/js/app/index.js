

// 验证码
$(function () {
            $("#mycode").on("click",function () {
               loadImg
            });
        });
        function loadImg() {
            $("#mycode").attr("src", "/blog/code/?id="+ new Date().getTime())
        }

//ajax用户名判断
        $(function(){
           $("#username").blur(function(){
              username = $(this).val()
              parms = {"username":username}
              $.ajax({
                    url:"/blog/checkusername/",
                    type:"post",
                    data:parms,
                    success:function(data){
                        if (parms['username'] == ""){
                            $("#show1").html("用户名不能为空")
                            $("#show1").addClass("colred").removeClass("colgreen")
                        }
                        else if(data.success && parms['username'] != null){
                            $("#show1").html("恭喜您，该用户名可以注册！！")
                            $("#show1").addClass("colgreen").removeClass("colred")
                        }
                        else {
                            $("#show1").html("对不起，该用户名已存在")
                            $("#show1").addClass("colred").removeClass("colgreen")
                        }
                    }
              })
           })
         })


         //ajax用户昵称判断
         $(function(){
           $("#nickname").blur(function(){
              nickname = $(this).val()
              parms = {"nickname":nickname}
              $.ajax({
                    url:"/blog/checknickname/",
                    type:"post",
                    data:parms,
                    success:function(data){
                        if (parms['nickname'] == ""){
                            $("#show2").html("昵称不能为空")
                            $("#show2").addClass("colred").removeClass("colgreen")
                        }
                       else if(data.success && parms['nickname'] != null){
                            $("#show2").html("恭喜您，该昵称可以注册！！")
                            $("#show2").addClass("colgreen").removeClass("colred")
                        }
                        else {
                            $("#show2").html("对不起，该昵称已存在")
                            $("#show2").addClass("colred").removeClass("colgreen")
                        }
                    }
              })
           })
         })