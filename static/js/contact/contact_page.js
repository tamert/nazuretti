$(function () {
  var requiredMessage = 'Bu alan gereklidir!';
  var emailMessage    = 'Yanlış e-posta!';

  $('#order-submit').validate({
    messages: {
      name:    requiredMessage,
      phone:   requiredMessage,
      city:    requiredMessage,
      address: requiredMessage,
      email: {
        required: requiredMessage,
        email:    emailMessage
      }
    }
  });
});
