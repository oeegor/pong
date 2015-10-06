var React = require('react');
var Router = require('react-router');

var DefaultRoute = Router.DefaultRoute;
var Route = Router.Route;
var Link = Router.Link;
var RouteHandler = Router.RouteHandler;

var jquery = require('jquery');

var Layout = require('./components/layout.jsx');
var DailyActions = require('./components/daily-actions.jsx');


var routes = (
  <Route name='app' path="/" handler={Layout}>
    <DefaultRoute handler={DailyActions}/>
  </Route>
);

Router.run(routes, function (Handler) {
    jquery.ajax({
        url: window.config.urls.user_status,
        dataType: 'json',
        cache: false,
        success: function(data) {
            console.log('userstatus', data);
            React.render(<Handler userStatus={data.result}/>, document.body);
        }.bind(this),
        error: function(xhr, status, err) {
            console.error(status, err.toString());
        }.bind(this)
    });
});
