JS_MOUSEEVENT_CLICK = """
const path = arguments[0];
if (path) {
    const clickEvent = new MouseEvent('click', {
        bubbles: true,         // Allow the event to bubble up the DOM tree
        cancelable: true,      // Allow the event to be canceled
        view: window           // The window object
    });
    path.dispatchEvent(clickEvent);  // Manually dispatch the event
}
"""
