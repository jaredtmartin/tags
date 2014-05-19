function saveDataInCache(data){
  $('#ajax-data').replaceWith('<div id="ajax-data" style="display: none;"></div>'); // Clear temp data cache
  return $('#ajax-data').append(data); // Add new data to cache
}
function updateMessages(data){
  $('.message:visible').remove();
  $('.event:visible').remove();
  $('.message', d).appendTo($('#messages'));
  $('.event', d).appendTo($('#events'));
}
function hideEvent(data, result){
  d=saveDataInCache(data);
  updateMessages(d);
}
function dismissEvent(url, pk){
	var csrf = $("#dismiss-"+pk+"-form input[name='csrfmiddlewaretoken']").val()
  $.ajax({
  	url: url,
  	type:'POST',
  	data:{pk:pk, csrfmiddlewaretoken:csrf},
  	success:hideEvent,
  });
}