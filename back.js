r=[1,2,3,1,2,1,2,3,1,3,1,2]
c = [1,1,1,2,2,4,4,4,5,5,6,6]
x = [1,1,1,2,2,1,2,1,1,1,1,1]
y=[1,1,1,1,2,1,1,1,1,1,1,2]

$.ajax({

url:


}.done(function(data){

	len = data.length()
	for(i=0;i<len;i++)
	{	
		html += '<li data-row=' + r[i]+' data-col='+c[i]+' data-sizex='+x[i]+' data-sizey='+y[i]+'><div class="box"><img src="c.png" alt="img12" /><div class="content"><h2>'+data.header+'</h2><p>'+data.data+'</p></div></div></li>'
		$(.gridster>ul).append(html);
	}
	
	


})

var height = $(".content").height()
var width = $(".content").width()
var width_p =  $("p").width()

$("h2").css("top",0.5*height)