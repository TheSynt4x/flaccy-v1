class WebSocketManager {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.reconnectDelay = 1000; // Initial reconnect delay in milliseconds
        this.maxReconnectDelay = 60000; // Maximum reconnect delay in milliseconds
        this.isConnected = false;
        this.messageQueue = []; // To store messages when socket is not ready
        this.hasSubscribedToMessages = false; // New flag
    }

    connect() {
        this.socket = new WebSocket(this.url);

        this.socket.onopen = () => {
            console.log('WebSocket is connected');
            this.isConnected = true;
            this.reconnectDelay = 1000; // Reset reconnect delay
            this.processMessageQueue();
        };

        this.socket.onerror = (error) => {
            console.error(`WebSocket error: ${error}`);
        };

        this.socket.onclose = (event) => {
            console.log(`WebSocket is closed. Reason: ${event.reason}`);
            this.isConnected = false;
            setTimeout(() => this.reconnect(), this.reconnectDelay);
            this.reconnectDelay *= 2;
            if (this.reconnectDelay > this.maxReconnectDelay) {
                this.reconnectDelay = this.maxReconnectDelay;
            }
        };
    }

    reconnect() {
        console.log('Attempting to reconnect...');
        this.connect();
    }

    send(msg) {
        if (this.isConnected && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(msg);
        } else if (this.socket.readyState === WebSocket.CONNECTING) {
            this.messageQueue.push(msg);
        } else {
            console.error('Failed to send a message: WebSocket is closed.');
        }
    }

    processMessageQueue() {
        while (this.isConnected && this.messageQueue.length > 0) {
            this.send(this.messageQueue.shift());
        }
    }

    subscribe(event, cb) {
        // Only add 'onmessage' event listener once
        if (event === 'onmessage' && this.hasSubscribedToMessages) {
            return;
        }

        this.socket[event] = cb;

        if (event === 'onmessage') {
            this.hasSubscribedToMessages = true;
        }
    }
}

export const connection = new WebSocketManager('ws://localhost:8000/ws');

connection.connect();
