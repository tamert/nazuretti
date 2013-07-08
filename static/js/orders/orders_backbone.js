$(function () {
  var OrderModel   = Backbone.Model.extend({});
  var ShoppingCart = Backbone.Model.extend({});

  var OrderCollection = Backbone.Collection.extend({
    model: OrderModel
  });

  var OrderItemView = Backbone.View.extend({
    itemTemplate: _.template($('#order-item-template').html()),
    tagName: 'div',
    className: 'cart-row',

    events: {
      'click .product-remove a': 'removeOrder',
      'click .buttons .up':      'incQuantity',
      'click .buttons .down':    'decQuantity'
    },

    initialize: function () {
      var self = this;
      self.listenTo(self.model, 'change', self.render);
    },
    
    render: function () {
      this.$el.html(this.itemTemplate(this.model.toJSON()));
      return this;
    },

    incQuantity: function (e) {
      var self     = this,
          quantity = parseInt(self.model.get('quantity')),
          product  = self.model.get('product'),
          price    = parseFloat(product.price);

      e.preventDefault();

      self.model.set('quantity', quantity + 1, { silent: true });
      self.model.set('total', (quantity + 1) * price);

      self.model.collection.trigger('change-total');

      $.post('/add-to-cart', { product_id: product.id, inc: true });
    },

    decQuantity: function (e) {
      var self     = this,
          quantity = parseInt(self.model.get('quantity')),
          product  = self.model.get('product'),
          price    = parseFloat(product.price);

      e.preventDefault();

      if (quantity > 1) {
        self.model.set('quantity', quantity - 1, { silent: true });
        self.model.set('total', (quantity - 1) * price);

        self.model.collection.trigger('change-total');
        $.post('/add-to-cart', { product_id: product.id, dec: true });
      }
    },

    removeOrder: function (e) {
      var self = this,
          product = self.model.get('product');
       
      e.preventDefault();

      $.post('/remove-from-cart', { product_id: product.id }, function (data) {
        if (data.success) {
          $('a[rel=' + product.id + ']').removeClass('disabled').html('SEPETE AT <span class="plus">+</span>');
          self.$el.fadeOut('fast', function () {
            self.model.collection.remove(self.model);
            self.remove();
          });
        }
      }, 'json');
    }
  });

  var OrderListView = Backbone.View.extend({
    el: $('#order-list-view'),

    initialize: function (options) {
      this.orders = options.orders;
      this.listenTo(this.orders, 'add', this.addItem);
      this.listenTo(this.orders, 'remove', this.removedItem);
    },

    addItem: function (item) {
      var self = this;
      var itemView = new OrderItemView({ model: item });

      self.$el.append(itemView.render().$el);
    },

    render: function () {
      var self = this;

      self.$el.html('');
      self.orders.each(self.addItem, self);

      return this;
    }
  });

  var OrderTotalView   = Backbone.View.extend({
    el: $('#order-total-view'),

    initialize: function (options) {
      var self = this;

      self.orders = options.orders;

      self.listenTo(self.orders, 'add', self.calculateTotal);
      self.listenTo(self.orders, 'remove', self.calculateTotal);
      self.listenTo(self.orders, 'change-total', self.calculateTotal);
    },

    calculateTotal: function () {
      var self = this,
          total = 0;
  
      self.orders.each(function (order) {
        total += parseFloat(order.get('total'));
      });

      self.model.set('total', total);
      self.render();
    },

    render: function () {
      var self = this;
      self.$('.model-value').html(self.model.get('total'));
    }
  });

  var ShoppingCartView = Backbone.View.extend({
    el: $('#shopping-cart'),

    initialize: function () {
      var self = this;

      self.orders = new Backbone.Collection();
      self.orders.comparator = function (order) {
        return order.get('product').id;
      };

      self.orderListView = new OrderListView({orders: self.orders});
      self.orderTotalView = new OrderTotalView({orders: self.orders, model: self.model});

      self.listenTo(self.orders, 'add', self.updateUi);
      self.listenTo(self.orders, 'remove', self.updateUi);
      self.listenTo(self.orders, 'remove', self.removeOrder);
    },

    addItem: function (order) {
      var self = this;
      self.orders.add(new Backbone.Model(order));
    },

    initItems: function (items) {
      var self = this;
      _(items).each(function (item) {
        self.addItem(item);
      });

      self.updateUi();
    },

    updateUi: function () {
      if (this.orders.length == 1) {
        this.orderListView.$el.show();
        this.orderTotalView.$el.show();
        this.$('.empty-text').hide();
        this.$('.full-text').show();
        this.$('.order-submit').show();
      } else if (this.orders.length == 0) {
        this.orderListView.$el.hide();
        this.orderTotalView.$el.hide();
        this.$('.empty-text').show();
        this.$('.full-text').hide();
        this.$('.order-submit').hide();
      } else if (this.orders.length > 1) {
        this.$('.empty-text').hide();
        this.$('.order-submit').show();
      }
    }
  });

  window.ShoppingCart = new ShoppingCartView({ model: new Backbone.Model({
    total: 0
  }) });

});
