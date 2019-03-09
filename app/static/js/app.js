/*global $*/
/*global countries*/
/*global $last_edited_poem_id*/

$( document ).ready(function() {
  $('#menu-homepage').on('click', HomePage);
  $('#menu-poets').on('click', Poets);
  $('#menu-societies').on('click', NotImplemented);
  $('#menu-publishPoem').on('click', PublishPoem);
  $('#menu-publishBio').on('click', PublishBio);
  $('#menu-news').on('click', NotImplemented);
  $('#menu-events').on('click', NotImplemented);
  $('#menu-shop').on('click', NotImplemented);
  $('#menu-donate').on('click', NotImplemented);
  $('#menu-mission').on('click', NotImplemented);
  $('#menu-people').on('click', NotImplemented);
  $('#menu-contact').on('click', NotImplemented);
  $('#menu-signin').on('click', Signin);
  $('#menu-login').on('click', Login);
  $('.navbar-nav a' ).on( 'click', function () {
  	$('.navbar-nav' ).find( 'li.active' ).removeClass( 'active' );
  	$( this ).parent( 'li' ).addClass( 'active' );
  });
  if (sessionStorage.getItem('id') != null){
    $("#menu-login").html('<span><i class="fas fa-sign-in-alt"></i></span> Logout');
    $("#logged-in").html("Welcome "+sessionStorage.getItem('name'));
    $("#menu-publish").addClass('d-block');
  } 
  $(document).on("submit", "form", function(e){
    e.preventDefault();
    return  false;
  });
  populateCountrySelection("signin_country")
  Poets();
});

function myAlert(alertType,alertMessage){
  var alertDiv = '<div class="alert '+alertType+' alert-dismissible " role="alert">';
  alertDiv += alertMessage;
  alertDiv += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
  alertDiv += '<span aria-hidden="true">&times;</span></button></div>';
  $("#alertMessage").html(alertDiv);
}

/* Load Homepage */
function HomePage(){
  $.post( "homepage", function( response ) {
    $( "#page-content" ).html( response );
    $(".navbar-toggler").click();
  });
}

/* Show Login Modal Form */
function Login(){
  if($("#menu-login").html() =='<span><i class="fas fa-sign-in-alt"></i></span> Login'){
     $("#formLogin").trigger('reset');
     $("#loginModal").modal('show');
  }
  else{
    $("#menu-login").html('<span><i class="fas fa-sign-in-alt"></i></span> Login');
    sessionStorage.clear();
    $("#logged-in").html("");
    $("#menu-publish").removeClass("d-block");
    $("#menu-publish").addClass("d-none");
  }
  Poets();
}

/* Show Signin ModalForm */
function Signin(){
  $("#signupModal").trigger('reset');
  $("#signupModal").modal('show');
  $(".navbar-toggler").click();
}

/* User Registration */
function RegisterNewUser(){
  var error = false;
  var error_message = ''
  var password = $('#password').val();
  var confirm_password = $('#confirm-password').val();
  var username = $('#username').val();
  var email = $('#email').val();
  var country_code = $('#signin_country').val();
  if (username.length < 5) {
    error_message ='<p>Incorrect full name: too short</p>';
    error = true;
  }
  var pattern = "^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$";
  if (!email.match(pattern)){
    error_message +='<p>Incorrect mail address</p>';
    error = true;
  }
  pattern = "^(?=.*?[a-z])(?=.*?[0-9]).{5,}$";
  if(!password.match(pattern)){
    error_message +='<p>Password: minimum five characters, at least one letter and one number.</p>';
    error = true;
  }
  if (password !== confirm_password){
    error_message +='Passwords dont match.';
    error = true;
  }
  if (!error){
    $.post( "register", { name: username, email: email,country: country_code, password: password })
    .done(function( response ) {
      myAlert("alert-success", response );
      $("#signupModal").modal('hide');
    });
  }
  else{
    myAlert("alert-danger", error_message );
  }
}

/* User authentication - login*/
function Authenticate(){
  var email = $('#inputEmail').val();
  var password = $('#inputPassword').val();
  $.post( "auth", { email: email, password: password })
    .done(function( response ) {
      if (response != ''){
          $("#loginModal").modal('hide');
          var cred = JSON.parse(response);
          sessionStorage.setItem('email', cred.email);
          sessionStorage.setItem('id', cred.id);
          sessionStorage.setItem('name', cred.name);
          sessionStorage.setItem('is_admin', cred.is_admin);
          $("#menu-login").html('<span><i class="fas fa-sign-in-alt"></i></span> Logout');
          $("#logged-in").html("Welcome "+cred.name);
          $("#menu-publish").removeClass("d-none")
          $("#menu-publish").addClass("d-block")
      }
      else {
        sessionStorage.clear();
        myAlert("alert-danger","Wrong username or password, try again.");
        return;
      }
    });
    $(".navbar-toggler").click();
}

/* Show new poem modal form */
function PublishPoem(){
  $(".navbar-toggler").click();
  $("#poemModal").modal('show');
}

/* Save poem from modal form */
function SavePoem(){
  var id = sessionStorage.getItem('id');
  var type = $('#inputPoemType').val();
  var title = $('#inputPoemTitle').val();
  var poem = $('#inputPoemText').val();
  $.post( "save-poem", { userid: id, poem_type: type, title: title, content: poem })
    .done(function( response ) {
        myAlert("alert-success", response );
        if(response == "Poem saved."){
            $("#poemModal").modal('hide');
        }
    });
}

/*Show modal bio form */
function PublishBio(){
  var id = sessionStorage.getItem('id');
  $(".navbar-toggler").click();
  $.post( "get-bio", { userid: id})
    .done(function( response ) {
      var data = JSON.parse(response);
      $("#inputBioText").val(data.content);
  });
  $("#bioModal").modal('show')
}

/* Save bio from modal form*/
function SaveBio(){
  var id = sessionStorage.getItem('id');
  var bio = $('#inputBioText').val();
  $.post( "save-bio", { userid: id, content: bio })
    .done(function( response ) {
      myAlert("alert-success", response );
      if (response == "Bio saved."){
        ShowPoems(id)
        $("#bioModal").modal('hide');
      }
  });
}

/*Show all poets*/
function Poets(){
   spinner('on')
   $.post( "poets", function( response ) {
     $( "#page-content" ).html( response );
     $('#navbarSupportedContent').collapse('hide')
     $('.navbar-nav' ).find( 'li.active' ).removeClass('active');
     $('#menu-poets').parent('li').addClass('active');
     populateCountrySelection('search_country');$('#poets-nav').parent('li').addClass('active');
     spinner('off')
  });
  
}

/* Show poems and bio of a poet*/
function ShowPoems(id){
  var logged_user_id = sessionStorage.getItem('id');
  if(logged_user_id == null) logged_user_id = 0;
  spinner('on')
  $.post( "user-poems", { user_id: id, logged_id: logged_user_id })
    .done(function( response ) {
      $("#poems").html( response );
  });
  $.post( "user-bio", { user_id: id, logged_id: logged_user_id })
    .done(function( response ) {
      $("#bio").html( response );
      spinner('off')
  });
  var targetOffset = $('#poems').parent().offset().top;
  $('html, body').animate({scrollTop: targetOffset}, 1000);
}

/* Show Edit modal form with a poem data*/
function EditPoem(id){
  $(".navbar-toggler").click();
  $.post( "get-poem", { poem_id: id})
    .done(function( response ) {
      var poem = JSON.parse(response);
      $("#updatePoemTitle").val(poem.title)
      $("#updatePoemType").val(poem.poem_type)
      $("#updatePoemText").val(poem.text)
      $last_edited_poem_id = poem.poem_id
  });
  $("#poemUpdateModal").modal('show')
}

/* Update poem from edit poem modal form*/
function UpdatePoem(){
  var user_id = sessionStorage.getItem('id');
  var type = $('#updatePoemType').val();
  var poem_title = $('#updatePoemTitle').val();
  var poem = $('#updatePoemText').val();
  var data =  { poem_id: $last_edited_poem_id, poem_type: type, title: poem_title, content: poem }
  $.post( "update-poem", data)
    .done(function( response ) {
        myAlert("alert-success", response );
        if(response == "Poem updated"){
            ShowPoems(user_id)
            $("#poemUpdateModal").modal('hide');
        }
    });
}
/* Delete poem */
function DeletePoem(id){
  $(".navbar-toggler").click();
  $.post( "delete-poem", { poem_id: id})
    .done(function( response ) {
      var user_id = sessionStorage.getItem('id');
      ShowPoems(user_id)
  });
}

/* Show/hide poem*/
function TogglePoem(x){
  if($("#"+x).attr('class') == 'd-none'){
    $("#"+x).removeClass('d-none');
    $("#"+x).addClass('d-block')
  }
  else{
    $("#"+x).removeClass('d-block');
    $("#"+x).addClass('d-none')
  }
}

/* Search poets*/
function SearchPoets(){
  var poet_name = $("#search_poet").val()
  var country = $("#search_country").val()
  var poem_type = $("#search_type option:selected").text()
  alert(poet_name+"\n"+country+"\n"+poem_type)
}

/* Not implemented alert*/
function NotImplemented(){
  myAlert("alert-warning","Not yet implemented.");
  $(".navbar-toggler").click();
  //$(window).scrollTop(0);
}

/* Populate select with countries data */
function populateCountrySelection(sel){
  for (var i in countries){
    $('#'+sel).append($('<option>', { 
        value: countries[i].code,
        text : countries[i].name 
    }));
  }
}

function spinner(to){
  if(to == 'on'){
    $("#spinner").removeClass("d-none");
    $("#spinner").addClass("d-block");
  }
  else{
    $("#spinner").removeClass("d-block");
    $("#spinner").addClass("d-none");
  }
}