import React from "react";

const Loader = () => {
    return (
        <div style={styles.loaderContainer}>
            <div style={styles.spinner}></div>
            <p>Loading...</p>
        </div>
    );
};

const styles = {
    loaderContainer: {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
    },
    spinner: {
        width: "50px",
        height: "50px",
        border: "5px solid #f3f3f3",
        borderTop: "5px solid #3498db",
        borderRadius: "50%",
        animation: "spin 1s linear infinite",
    },
};

// keyframes for spinner animation
const styleSheet = document.styleSheets[0];
const keyframes =
    `@keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }`;
styleSheet.insertRule(keyframes, styleSheet.cssRules.length);

export default Loader