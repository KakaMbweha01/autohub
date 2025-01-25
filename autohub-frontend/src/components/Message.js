import React from "react";

const Message = ({ children, variant = "info" }) => {
    const colors = {
        info: "3498db",
        success: "2ecc71",
        danger: "#e74c3c",
        warning: "#f1c40f",
    };

    return (
        <div style={{ ...styles.message, backgroundColor: colors[variant] || colors.info}}>
            {children}
        </div>
    );
};

const styles = {
    message: {
        padding: "10px 15px",
        color: "#fff",
        borderRadius: "5px",
        margin: "10px 0",
        textAlign: "center",
        fontSize: "14px",
    },
};

export default Message;