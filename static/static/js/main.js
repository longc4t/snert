layer = layui.layer;
if (Cookies.get('token')){
    $(".personal")[0].href="/user"
}else {
    $(".personal")[0].href="login.html"
}
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
		        window.location.href="/"
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
		        window.location.href="/"
            }else{
                layer.alert(results.msg, {
                    icon: 2,
                    skin: 'layer-ext-moon'
                })
            }
        },"json");
    }
}

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

function article() {
    $.post("/api/article/add",JSON.stringify({"articletitle":btoa(title),"articleauthor":btoa(author),"articleauthorid": authorid,"articlecontent":btoa(content),"articletimestamp":timestamp,"token":Cookies.get('token')}),function (results){
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

function getarticle() {
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


