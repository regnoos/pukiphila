(function ($, Backbone, _, app) {
    var TemplateView = Backbone.View.extend({
        templateName: '',
        initialize: function () {
            this.template = _.template($(this.templateName).html());
        },
        render: function () {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function () {
            return {};
        }
    });

    var FormView = TemplateView.extend({
        events: {
            'submit form': 'submit'
        },
        errorTemplate: _.template('<span class="error"><%- msg %></span>'),
        clearErrors: function () {
            $('.error', this.form).remove();
        },
        showErrors: function (errors) {
            _.map(errors, function (fieldErrors, name) {
                var field = $(':input[name=' + name + ']', this.form),
                    label = $('label[for=' + field.attr('id') + ']', this.form);
                if (label.length === 0) {
                    label = $('label', this.form).first();
                }
                function appendError(msg) {
                    label.before(this.errorTemplate({msg: msg}));
                }

                _.map(fieldErrors, appendError, this);
            }, this);
        },
        serializeForm: function (form) {
            return _.object(_.map(form.serializeArray(), function (item) {
        // Convert object to tuple of (name, value)
                return [item.name, item.value];
            }));
        },
        submit: function (event) {
            event.preventDefault();
            this.form = $(event.currentTarget);
            this.clearErrors();
        },
        failure: function (xhr, status, error) {
            var errors = xhr.responseJSON;
            this.showErrors(errors);
        },
        done: function (event) {
            if (event) {
                event.preventDefault();
            }
            this.trigger('done');
            this.remove();
        },
        modelFailure: function (model, xhr, options) {
            var errors = xhr.responseJSON;
            this.showErrors(errors)
        }
    });

    var NewAlbumView = FormView.extend({
        templateName: '#new_album_template',
        className: 'new-album',
        events: _.extend({'click button.cancel': 'done'}, FormView.prototype.events),
        submit: function (event) {
            var self = this,
                attributes = {};
            FormView.prototype.submit.apply(this, arguments);
            attributes = this.serializeForm(this.form);
            app.collections.ready.done(function () {
                app.albums.create(attributes, {
                    wait: true,
                    success: $.proxy(self.success, self),
                    error: $.proxy(self.modelFailure, self)
                });
            });
        },
        success: function (model) {
            this.done();
            window.location.hash = '#album/' + model.get('id');
        }
    });

    var AlbumView = TemplateView.extend({
        templateName: '#album_template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            this.albumId = options.albumId;
            this.album = null;
            app.collections.ready.done(function () {
                app.albums.getOrFetch(self.albumId).done(function (album) {
                    self.album = album;
                    self.render();
                }).fail(function (album) {
                    self.album = album;
                    self.album.invalid = true;
                    self.render();
                });
            });
        },
        getContext: function () {
            return {album: this.album};
        }
    });

    var HomepageView = TemplateView.extend({
        templateName: '#home_template',
        events: {
            'click button.add': 'renderAddForm'
        },
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            app.collections.ready.done(function () {
                var end = new Date();
                end.setDate(end.getDate() - 7);
                end = end.toISOString().replace(/T.*/g, '');
                app.albums.fetch({
                    data: {end_min: end},
                    success: $.proxy(self.render, self)
                });
            });
        },
        getContext: function () {
            return {albums: app.albums || null};
        },
        renderAddForm: function (event) {
            var view = new NewAlbumView(), link = $(event.currentTarget);
            event.preventDefault();
            link.before(view.el);
            link.hide();
            view.render();
            view.on('done', function () {
                link.show();
            });
        }

    });


    var LoginView = FormView.extend({
        id: 'login',
        templateName: '#login_template',
        submit: function (event) {
            var data = {};
            FormView.prototype.submit.apply(this, arguments);
            data = this.serializeForm(this.form);
            $.post(app.apiLogin, data)
                .success($.proxy(this.loginSuccess, this))
                .fail($.proxy(this.failure, this));
        },
        loginSuccess: function (data) {
            app.session.save(data.token);
            this.done();
        }
    });

    var HeaderView = TemplateView.extend({
        tagName: 'header',
        templateName: '#header-template',
        events: {
            'click a#logout': 'logout'
        },
        getContext: function () {
            return {authenticated: app.session.authenticated()};
        },
        logout: function (event) {
            event.preventDefault();
            app.session.delete();
            window.location = '/';
        }
    });
    app.views.HomepageView = HomepageView;
    app.views.LoginView = LoginView;
    app.views.HeaderView = HeaderView;
    app.views.AlbumView = AlbumView;

})(jQuery, Backbone, _, app);
