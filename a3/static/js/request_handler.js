$(document).ready(function(){
  $("#getWord").click(function(){
    //alert("here's a word");
    $.ajax({
      type: "GET",
      url: "/test",
      data: {msg: "howdy"},
      success: function(data)
        {
          alert("it says... " + data);
        }
      });
  });

  $("#sendWord").click(function(){
    var someWord = $("input[name=wordToSend]").val()
    if (someWord.length <= 0)
    {
      //alert
      alert("error: enter a value");
    }
    else {
      //alert("you want to send '"+ someWord + "'!")
      $.ajax({
        type: "POST",
        url: "/test",
        data: {wordToSend: someWord},
        success: function(data)
          {
            alert("it says... " + data);
          }
        });
    }
  });

});