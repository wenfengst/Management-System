var tDict={};

var app=new Vue({
		  el: '#v-for-tlist',
		  data: {
		    object:{}
		  }
		})
jQuery(document).ready(function() {
	jQuery("#alertmsg").hide();
	jQuery("#alertmsg_t").hide();

  	jQuery("#tbtn").click(function(){ 
  		jQuery("#alertmsg_t").hide();
  		
    	jQuery.ajax({  
	        type: "GET",  
	        url:"/json_get_tlist/"+jQuery("#tname").val(),  
	        async:true,
	        cache:false,                    
	        dataType:"json",            
	        success:function(msg){  

				if(msg.length>0)	
				{
		        	app.object=msg;
		        	for (i=0;i< app.object.length;i++)
		        	{	   
		        		tDict[app.object[i].tid]=app.object[i];
		        	}
		        		jQuery("#tlist_choose").attr("style","display: inline");
                jQuery("#teacherid").val(app.object[0].tid);
                jQuery("#tname_confirm").val(tDict[app.object[0].tid].tname);
                jQuery("#tcompany").val(tDict[app.object[0].tid].company);
                if(tDict[app.object[0].tid].bank_name.length>0)
                  jQuery("#tbank_name").val(tDict[app.object[0].tid].bank_name);
                jQuery("#tbank_num").val(tDict[app.object[0].tid].bank_number);
                jQuery("#ttitle").val(tDict[app.object[0].tid].title);
                jQuery("#tsalary").val(tDict[app.object[0].tid].salary);
       	        jQuery("#v-for-tlist").focus();	              
	        	}
	        	else
	        		jQuery("#alertmsg_t").show();
	        }  
      	});  
  	});   
});  