import React from "react";

const Button = ({ children, onClick, type = "button", variant = "primary", disabled = false }) => {
    const colors = {
        primary: "#3498db",
        secondary: "#95a5a6",
        danger: "#e74c3c",
    };

    return (
        <button
            style={{
                ...styles.button,
                backgroundColor: colors[variant] || colors.primary,
                cursor: disabled ? "not-allowed" : "pointer",
            }}
            onCLick={onClick}
            type={type}
            disabled={disabled}
        >
            {children}
        </button>
    );
};

const styles = {
    button: {
        padding: "10px 20px",
        color: "#fff",
        border: "none",
        borderRadius: "5px",
        fontSize: "14px",
        fontWeight: "bold",
    },
};

export default Button;