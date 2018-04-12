/*
* @Author: xiaodong
* @Date:   2018-01-15 11:59:06
* @Last Modified by:   xiaodong
* @Last Modified time: 2018-01-16 09:57:30
*/
//导航栏添加active属性
$(document).ready(function(){
	//1.当前的url
	var c_url = window.location.href; 
	//2.判断当前的url
	var c_index = 0;
	if(c_url.indexOf('add_article') > 0){
		c_index = 1;
	}else if (c_url.indexOf('about') > 0) {
		c_index = 2;
	}else if (c_url.indexOf('contact') > 0) {
		c_index = 3;
	}else if (c_url.indexOf('front_settings') > 0) {
		c_index = -1;
	}else{
		c_index = 0;
	}
	var ulTag = $('#ul-tags');

	//判断处理
	if(c_index >= 0){
		ulTag.children().eq(c_index).addClass('active').siblings().removeClass('active');
	}else{
		ulTag.children().removeClass('active');
	}
});
