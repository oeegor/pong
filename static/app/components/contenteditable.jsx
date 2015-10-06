
var React = require('react');


var ContentEditable = React.createClass({
    render: function(){
        return (
            <span
                onInput={this.handleInput}
                onKeyDown={this.handleKeyDown}
                onBlur={this.handleChange}
                contentEditable="true"
                dangerouslySetInnerHTML={{__html: this.props.html}}
            >
            </span>
        );
    },
    shouldComponentUpdate: function(nextProps){
        return nextProps.html !== this.getDOMNode().innerHTML;
    },
    handleKeyDown: function(event){
        if (this.props.onKeyDown) {
            this.props.onKeyDown(event);
        }
    },
    handleChange: function(){
        var html = this.getDOMNode().innerHTML;
        if (this.props.onChange && html !== this.lastHtml) {
            this.props.onChange({
                target: {
                    value: html
                }
            });
        }
        this.lastHtml = html;
    }
});

module.exports = ContentEditable;
