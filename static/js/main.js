$( document ).ready(function() {

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
    var host = document.location.host;
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
      (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      !(/^(\/\/|http:|https:).*/.test(url));
  }

  var inlineEdit = function(selector, changeType) {
    $("body").on("click", selector, function(e) {
      var replaceWith = $('<input name="temp" type="text" />')
      var elem = $(this);
      elem.hide();
      var url;
      if (changeType == "item") {
        var parent = elem.parent(".bucketlists-item");
        var bucketlistUrl = parent.parent("div").siblings("form").attr("action");
        var itemId = parent.attr("data-id");
        url = bucketlistUrl+itemId+"/";
      } else if (changeType == "bucketlist") {
        var bucketlistId = elem.parents(".bucketlist").attr("data-id");
        url = "/api/v1/bucketlists/"+bucketlistId+"/";
      }
      elem.after(replaceWith);
      replaceWith.val(elem.text())
      replaceWith.focus();
      replaceWith.blur(function() {
      var name = $(this).val();
        if (name != "") {
          elem.text(name);
        }
        $(this).remove();
        elem.show();
        $.ajax({
          method: "PUT",
          url: url,
          dataType: "json",
          data: {"name": name},
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
        })
    });
  });
};


inlineEdit('.bucketlist-name', "bucketlist");
inlineEdit('.item-not-done p, item-done p', "item");


  $( "body" ).on("click", ".item-add", function() {
    $(this).parents('.col-md-4').toggleClass("add-magin");
    bucketlistGrid.packery("shiftLayout");
    $(this).siblings("form").slideToggle(200);
  });

  $("body").on("change", ".done", function(e){
    var itemContainer = $(this).parents(".bucketlists-item");
    var itemId = itemContainer.attr("data-id");
    var bucketlistUrl = itemContainer.parent("div").siblings("form").attr("action");
    var itemUrl = bucketlistUrl+itemId+"/"
    var done = $(this).is(":checked") ? true : false;
    var csrf = $('input[name=csrfmiddlewaretoken]').val();
    var data = {
      'done': done
    }
    $.ajax({
      method: "PUT",
      url: itemUrl,
      dataType: "json",
      data: data,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
  });

  var bucketlistGrid = $('.bucketlists-row').packery({
    // options
    itemSelector: '.col-md-4',
    percentPosition: true
  });


  $("body").on('click', '.create', function(e){
    var nameField = $(".modal-body form textarea");
    var bucketlistName = nameField.val();
    nameField.val('');
    var csrf = $('input[name=csrfmiddlewaretoken]').val()
    var data = {
     'name': bucketlistName
    }
    $.ajax({
      method: "POST",
      url: "/api/v1/bucketlists/",
      dataType: "json",
      data: data,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    }).done(function(e){
      id = e.id;
      var bucketlist = $('<div class="col-md-4" ><div class="bucketlist" data-id="'+id+'"><h4 class="bucketlist-head">'+
                         '<span class="bucketlist-name">'+bucketlistName+'</span><span class="pull-right">'+
                         '<i class="fa fa-lock bucketlist-public" data-public="false" aria-hidden="true" title="make public"></i>'+
                         '<span class="glyphicon glyphicon-remove bucketlist-delete" aria-hidden="true"></span>'+
                         '</span></h4><div class="item-not-done"></div><div class="item-done"></div><form method="POST" action='+
                         '"/api/v1/bucketlists/'+id+'/items/"><textarea class="form-control" rows="2"></textarea>'+
                         '<button type="submit" class="btn btn-primary btn-xs pull-right">save</button></form><div class="item-add">'+
                         '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span></div></div></div>');
        bucketlistGrid.prepend(bucketlist).packery('prepended', bucketlist);
    });
  });

  $("body").on("submit", ".bucketlist form", function(e){
      e.preventDefault();
      var _this = $(this)
      var itemTextarea = _this.children("textarea");
      var itemUrl = _this.attr('action')
      var itemName = itemTextarea.val()
      itemTextarea.val('')
      var csrf = $('input[name=csrfmiddlewaretoken]').val()
      var data = {
          'name': itemName,
          'csrfmiddlewaretoken': csrf
      }
      $.ajax({
            method: "POST",
            url: itemUrl,
            dataType: "json",
            data: data
        }).done(function(e){
            id = e.id;
            var item = '<div class="bucketlists-item" data-id='+id+'><input type="checkbox" '+
                       'class="done"><a href="#" style="display: none;"><span class="glyphicon '+
                       'glyphicon-remove item-delete pull-right" aria-hidden="true"></span></a><p>'+
                       itemName+'</p></div>';
            _this.siblings(".item-not-done").append(item);
            _this.slideToggle(200);
      });
  });

  $("body").on("click", ".bucketlist-delete", function(e){
      var bucketlist = $(this).parents(".bucketlist");
      var bucketlistId = bucketlist.attr("data-id");
      var url = "/api/v1/bucketlists/"+bucketlistId+"/";
      $.ajax({
          method: "DELETE",
          url: url,
          dataType: "json",
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
      });
      bucketlist.remove();
  });

  $("body").on("mouseenter mouseleave", ".bucketlists-item", function(e){
      $(this).children("a").toggle();
  });

  $("body").on("click", ".item-delete", function(e){
      e.preventDefault()
      var parent = $(this).parents(".bucketlists-item");
      var bucketlistUrl = parent.parent("div").siblings("form").attr("action");
      var itemId = parent.attr("data-id");
      url = bucketlistUrl+itemId+"/";
      $.ajax({
          method: "DELETE",
          url: url,
          dataType: "json",
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
      });
      parent.remove()
  });

  $("body").on("mouseenter mouseleave", ".bucketlist-public", function(e){
      $(this).toggleClass("fa-lock fa-unlock");
  });
  $("body").on("click", ".bucketlist-public", function(e){
      var _this = $(this)
      var makePublic = _this.attr("data-public") == "true" ? false : true;
      var bucketlist = _this.parents(".bucketlist");
      var bucketlistId = bucketlist.attr("data-id");
      var url = "/api/v1/bucketlists/"+bucketlistId+"/";
      $.ajax({
          method: "PUT",
          url: url,
          dataType: "json",
          data: {
              "is_public": makePublic
          },
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
      }).done(function(e){
          _this.removeClass("fa-unlock fa-lock");
          if(makePublic == true){
              _this.addClass("fa-lock");
          } else {
              _this.addClass("fa-unlock");
          }
      });
  });

  $(document).ajaxComplete(function(){
      bucketlistGrid.packery();
  })

  $('#myTabs a').click(function (e) {
      e.preventDefault()
      $(this).tab('show')
      console.log($(this));
  })

});
