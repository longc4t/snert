var comlayedit;
layui.use(['element','layer','layedit','laypage'], function () {
        var laypage = layui.laypage;
        var layedit = layui.layedit;
        var element = layui.element;
        var layer = layui.layer;
        if (Cookies.get('token')){
            if(window.location.href.indexOf("login")==-1){
                $.post("/api/checklogin",JSON.stringify({"token":Cookies.get('token')}),function (results){
                    if(results.success){
                        $(".personal")[0].href="/user"
                    }else{
                        layer.alert(results.msg, {
                            icon: 2,
                            skin: 'layer-ext-moon'
                        },function(index){
                            window.location.href="/login"
                            layer.close(index);
                        })
                    }
                });
            }
            articleedit=layedit.build('demo',{tool: [
              'strong' //加粗
              ,'italic' //斜体
              ,'underline' //下划线
              ,'del' //删除线
              ,'|' //分割线
              ,'left' //左对齐
              ,'center' //居中对齐
              ,'right' //右对齐
              ,'link' //超链接
              ,'unlink' //清除链接
              ,'face' //表情
            ]});
            getuserdata();
            comlayedit=layedit;

            if($(".item-title > p:nth-child(1) > span:nth-child(2)").text()=="欢迎来到我的轻博客"){
                laypage.render({
                    elem: 'demo2'
                    ,count: 100
                    ,theme: '#1E9FFF'
                });

            }
        }else{
            window.location.href="/login"
        }
});


function check_login() {
	var name = $("#user_name").val();
	var pass = $("#password").val();
	if (name =="" || pass == "") {
        $("#login_form").removeClass('shake_effect');
	    setTimeout(function(){$("#login_form").addClass('shake_effect')},1);
	    layer.alert('请填写完整', {
			icon: 2,
			skin: 'layer-ext-moon'
		})
    }else{
        $.post("/api/login",JSON.stringify({"username":btoa(name),"password": btoa(pass)}),function (results){
            if(results.success){
                Cookies.set("token",results.token);
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        });
		        setTimeout(function(){window.location.href="/"},1000);
            }else{
                layer.alert(results.msg, {
                    icon: 2,
                    skin: 'layer-ext-moon'
                })
            }
        },"json");
    }
}

function check_register(){
	var name = $("#r_user_name").val();
	var pass = $("#r_password").val();
	if(name =="" || pass==""){
	    $("#login_form").removeClass('shake_effect');
	    setTimeout(function(){$("#login_form").addClass('shake_effect')},1);
	    layer.alert('请填写完整', {
			icon: 2,
			skin: 'layer-ext-moon'
		})
	}else{
	    $.post("/api/register",JSON.stringify({"username":btoa(name),"password": btoa(pass)}),function (results){
            if(results.success){
                Cookies.set("token",results.token);
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        });
		        setTimeout(function(){window.location.href="/"},1000);
            }else{
                layer.alert(results.msg, {
                    icon: 2,
                    skin: 'layer-ext-moon'
                })
            }
        },"json");
    }
}

function changeuserinformation(){
    var current_Password = $("#current_password").val();
    var newPassword = $("#new_password").val();
    var confirmation_password = $("#confirmation_password").val();
    var personalized_signature = $("#personalized_signature").val();

    if(current_Password=="" || newPassword==""){
        layer.alert("请输入"+ (current_Password==""?"当前":"新")+"密码", {
            icon: 2,
            skin: 'layer-ext-moon'
		});
		return 0
    }else{
        if(current_Password==newPassword){
            layer.alert("新密码不能当前密码相同", {
                icon: 2,
                skin: 'layer-ext-moon'
            });
            return 0
        }
        if(newPassword == confirmation_password){
            $.post("/api/user/change", JSON.stringify({
                                    "token": Cookies.get('token'),
                                    "oldpassword": btoa(current_Password),
                                    "newpassword": btoa(newPassword),
                                    "personsay": btoa(escape(personalized_signature))
                                }), function (data) {
                                    if (data.success) {
                                        layer.alert(data.msg, {
                                            icon: 1,
                                            skin: 'layer-ext-moon'
                                        },function(index){
                                            Cookies.set("token",data.token)
                                            window.location.href="/user"
                                            layer.close(index);
                                        });
                                    } else {
                                        layer.alert(data.msg, {
                                            icon: 2,
                                            skin: 'layer-ext-moon'
                                        });
                                    }
            });
        }else{
            layer.alert("两次输入的密码不一致", {
                icon: 2,
                skin: 'layer-ext-moon'
            });
        }
    }
}


function getuserdata(){
    if(window.location.href.indexOf("/user")){
        if(location.hash.replace("#","")){
            datas={"userid":location.hash.replace("#","")}
        }else{
            datas={"token":Cookies.get('token')}
        }
        $.post("/api/user/getinfo", JSON.stringify(datas), function (data) {
            if (data.success) {
                $("#personalized_signature").val(unescape(atob(data.personsay)));
            } else {
                layer.alert("网络错误", {
                    icon: 2,
                    skin: 'layer-ext-moon'
                });
            }
        });
    }
}


/*
function comment() {
    $.post("/api/comment/add",JSON.stringify({"commentauthor":btoa(author),"commentauthorid": commentid,"commentcontent":btoa(content),"commenttimestamp":timestamp,"token":Cookies.get('token')}),function (results){
            if(results.success){
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        })
		        //window.location.href="/"
            }else{
                layer.alert(results.msg, {
                    icon: 2,
                    skin: 'layer-ext-moon'
                })
            }
    },"json");
}

function getcomment() {
    $.post("/api/comment/search",JSON.stringify({"commentidarrary":idarrary,"token":Cookies.get('token')}),function (results){
            if(results.success){
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        })
		        //window.location.href="/"
            }else{
                layer.alert(results.msg, {
                    icon: 2,
                    skin: 'layer-ext-moon'
                })
            }
        },"json");
}

*/

function getarticle() {
    if($(".item-title > p:nth-child(1) > span:nth-child(2)").text()=="欢迎来到我的轻博客"){
        $.post("/api/article/index",JSON.stringify({"pagenum":num,"token":Cookies.get('token')}),function (results){
        laypage.render({
            elem: 'demo2'
            ,count: 100
            ,theme: '#1E9FFF'
        });


    }

    $.post("/api/article/index",JSON.stringify({"pagenum":num,"token":Cookies.get('token')}),function (results){
        if(results.success){
            html="";
            for (var i in results.data){
                html+="<div class=\"item\"><div class=\"item-box  layer-photos-demo1 layer-pho" +
                    "tos-demo\"><h3><a href=\"details.html?id="
                    +results.data[i]["articleid"]
                    +"\">"
                    +atob(results.data[i]["articletitle"]).replace("<","&lt;").replace(">","&gt;")
                    +"</a></h3>"+"<h5>发布于：<span>"
                    +new Date(results.data[i]["articletimestamp"]*1000).toLocaleString()
                    +"</span></h5><p>"
                    +atob(results.data[i]["articlecontent"]).replace("<","&lt;").replace(">","&gt;")
                    +"</p></div><div class=\"comment count\"><a href=\"details.html?id="
                    +results.data[i]["commentid"]
                    +"\">评论</a><a href=\"javascript:;\" class=\"like\">点赞</a></div></div>"
            }
            //window.location.href="/"
        }else{
            layer.alert(results.msg, {
                icon: 2,
                skin: 'layer-ext-moon'
            })
        }
    },"json");
}


function getHashParameter(key){
    var params = getHashParameters();
    return params[key];
}

function getHashParameters(){
    var arr = (location.hash || "").replace(/^\#/,'').split("&");
    var params = {};
    for(var i=0; i<arr.length; i++){
        var data = arr[i].split("=");
        if(data.length == 2){
             params[data[0]] = data[1];
        }
    }
    return params;
}

function uploadarticle() {
    title=escape($("#title").val())
    content=escape(comlayedit.getContent(articleedit))
    timestamp=""+new Date().getTime()
    username=""
    if (title=="" || content ==""){
        layer.alert("请填写完整", {
                    icon: 2,
                    skin: 'layer-ext-moon'
        });
        return 0;
    }
    $.post("/api/user/getinfo", JSON.stringify(datas), function (data) {
            if (data.success) {
                username=data.username
            } else {
                layer.alert("网络错误", {
                    icon: 2,
                    skin: 'layer-ext-moon'
                });
            }
    });
    $.post("/api/article/add",JSON.stringify({"articletitle":btoa(title),"articleauthor": username,"articlecontent":btoa(content),"articletimestamp":timestamp,"token":Cookies.get('token')}),function (results){
            if(results.success){
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        })
            }else{
                layer.alert(results.msg, {
                    icon: 2,
                    skin: 'layer-ext-moon'
                })
            }
        },"json");
}