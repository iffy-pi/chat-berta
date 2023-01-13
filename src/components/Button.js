const Button = ({buttonText, onClick}) => {
    return (
        <button
        onClick={onClick}>
            {buttonText}
        </button>
    )
}

Button.defaultProps = {
    buttonText: "Click Me!",
    onClick: () => alert("I've been clicked!")
}

export default Button