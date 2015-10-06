var React = require('react');
var _ = require('underscore');


var LoginView = React.createClass({
    render: function () {
        var loginLinks = _.map(
            window.config.auth_backends,
            function(name) {
                var url = '/login/' + name + '/';
                return <li><a href={url}>Login via {name}</a></li>
            }
        );
        return (
            <div className='login-page'>
                <ul>
                    {loginLinks}
                </ul>
            </div>
        );
    }
});
module.exports = LoginView;
