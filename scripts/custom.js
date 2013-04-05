$(document).ready(function(){		
   $(".editBusiness").click(function(){
     $("#yellowpages_id").val($(this).data('id'));
	 $('#businessNameLabel').text($(this).data('name'));
     $('#updateBusiness').modal('show');
   });
});