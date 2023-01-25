const Message = ({ text, color, alignment, thick }) => {
    return (
        <div className={(thick) ? "thick-container" : "basic-container"}>
            <p>{text}</p>
        </div>
    )
}

Message.defaultProps = {
    thick: false
}

export default Message