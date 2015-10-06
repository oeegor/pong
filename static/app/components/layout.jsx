var React = require('react');
var Router = require('react-router');
var RouteHandler = Router.RouteHandler;
var LoginView = require('./login.jsx');


var LayoutView = React.createClass({
    render: function () {
        // var login = this.state.userStatus.is_anonymous ? <Link to="login">Login</Link> : this.props.userStatus.email;
        var routeHandler = this.props.userStatus.is_anonymous
            ? <LoginView/>
            : (
                <div>
                    <header className='layout-header'>
                        <div className='user font-m'>
                            <span>{this.props.userStatus.email}</span>
                            <a
                                href={window.config.urls.logout}
                                className="logout icon-button glyphicons glyphicons-exit"
                            >
                            </a>
                        </div>
                    </header>
                    <RouteHandler/>
                </div>
            );

        return (
            <div className='layout'>
                {routeHandler}
            </div>
        );
    }
});
module.exports = LayoutView;
