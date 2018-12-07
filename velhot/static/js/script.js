$('#chat-form').on('submit', function(event) {
  event.preventDefault();

  var urlParts = window.location.href.split('/');
  var id = urlParts[urlParts.length - 2];
  var isPrivate = id !== 'chat';
  var url = '/chatpost/';
  if (isPrivate) {
    url += id + '/';
  }
  
  $.ajax({

    url: url,
    type: 'POST',
    data: { msgbox: $('#chat-msg').val() },
    
    success: function(json) {
      $('#chat-msg').val('');
      $('#msg-list').append(
        '<li class="text-right list-group-item">' + json.msg + '</li>'
      );
      // ylläolevaa riviä pitää muokata niin että viestin lähettäjä saadaan näkyviin ensimmäisen get kutsun jälkeenkin
      var chatlist = document.getElementById('msg-list-div');
      chatlist.scrollTop = chatlist.scrollHeight;
    }
  });
});

function getChatMessages() {
  var urlParts = window.location.href.split('/');
  var id = urlParts[urlParts.length - 2];
  var isPrivate = id !== 'chat';
  var url = '/chatmessages/';
  if (isPrivate) {
    url += id + '/';
  }

  if (!scrolling) {
    $.get(url, function(chatmessages) {
      $('#msg-list').html(chatmessages);
    });
  }
  scrolling = false;
}

var scrolling = false;
$(function() {
  $('#msg-list-div').on('scroll', function() {
    scrolling = true;
  });
  refreshTimer = setInterval(getChatMessages, 5000);
});

// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  }
});

$(document).ready(function() {
  $('#send').attr('disabled', 'disabled');
  $('#chat-msg').keyup(function() {
    if ($(this).val() != '') {
      $('#send').removeAttr('disabled');
    } else {
      $('#send').attr('disabled', 'disabled');
    }
  });
});

function remove_post(id) {
    $.ajax({

        url: '/message/'+(id)+'/',
        type: 'DELETE',
        data: { msgbox: $('#chat-msg').val() },
        
        success: function(json) {
          $('#chat-msg').val('');
          $('#message-'+id).remove();
        }
})
}
