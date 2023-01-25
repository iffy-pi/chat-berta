const Header = ({ message }) => {
    return (
        <div>
            <h1>{message}</h1>
        </div>
    )
}

Header.defaultProps = {
    message: "Hello World!"
}


export default Header