$(function () {
  // add to cart buttons
  $('.m_cart_button a').on('click', function (e) {
    var self = this;
    e.preventDefault();

    if ($(self).hasClass('disabled')) {
      return;
    }

    productId = $(this).attr('rel');
    $.post('/add-to-cart', { product_id: productId }, function (data) {
      if (data.success) {
        window.ShoppingCart.addItem(data.order);
        $(self).addClass('disabled').text('SEPETE EKLENDI');
      }
    }, 'json');
  });

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
