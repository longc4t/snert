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
	    setTimeout(function(){$("#login_form").addClass('shake_effect')},1)
	    layer.alert('请填写完整', {
			icon: 2,
			skin: 'layer-ext-moon'
		})
    }else{
        $.post("/api/login",JSON.stringify({"username":btoa(name),"password": btoa(pass)}),function (results){
            if(results.success){
                Cookies.set("token",results.token)
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        })
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
	    setTimeout(function(){$("#login_form").addClass('shake_effect')},1)
	    layer.alert('请填写完整', {
			icon: 2,
			skin: 'layer-ext-moon'
		})
	}else{
	    $.post("/api/register",JSON.stringify({"username":btoa(name),"password": btoa(pass)}),function (results){
            if(results.success){
                Cookies.set("token",results.token)
                layer.alert(results.msg, {
			        icon: 1,
			        skin: 'layer-ext-moon'
		        })
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
