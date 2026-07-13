class WebSocketService {
constructor() {
this.channels = new Map();
this.maxReconnectAttempts = 5;
this.reconnectDelay = 3000;
}

_initChannelState(url) {
    return {
        socket: null,
        listeners: new Map(),
        connected: false,
        reconnectAttempts: 0,
        url: url,
        reconnectTimer: null
    };
}

connect(channel, url) {
    if (!this.channels.has(channel)) {
        this.channels.set(channel, this._initChannelState(url));
    }

    const state = this.channels.get(channel);
    
    if (state.socket) return;
    if (url) state.url = url;

    state.socket = new WebSocket(state.url);

    state.socket.onopen = () => {
        console.log("✅ WebSocket Connected: " + channel);
        state.connected = true;
        state.reconnectAttempts = 0;
        this.emit(channel, "connected");
    };

    state.socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            this.emit(channel, "message", data);
            if (data.type) {
                this.emit(channel, data.type, data);
            }
        } catch (error) {
            console.error("WebSocket Parse Error on channel " + channel, error);
        }
    };

    state.socket.onclose = () => {
        console.log("❌ WebSocket Closed: " + channel);
        state.connected = false;
        this.emit(channel, "disconnected");
        state.socket = null;
        this._reconnect(channel);
    };

    state.socket.onerror = (error) => {
        console.error("WebSocket Error on channel " + channel, error);
    };
}

_reconnect(channel) {
    const state = this.channels.get(channel);
    if (!state) return;
    
    if (state.reconnectAttempts >= this.maxReconnectAttempts) return;

    state.reconnectAttempts++;

    if (state.reconnectTimer) {
        clearTimeout(state.reconnectTimer);
    }

    state.reconnectTimer = setTimeout(() => {
        this.connect(channel, state.url);
    }, this.reconnectDelay);
}

disconnect(channel) {
    const state = this.channels.get(channel);
    if (!state) return;

    if (state.reconnectTimer) {
        clearTimeout(state.reconnectTimer);
        state.reconnectTimer = null;
    }

    if (state.socket) {
        state.socket.onclose = null;
        state.socket.close();
        state.socket = null;
    }

    state.connected = false;
}

disconnectAll() {
    for (const channel of this.channels.keys()) {
        this.disconnect(channel);
    }
}

send(channel, data) {
    const state = this.channels.get(channel);
    if (!state || !state.socket) return;

    if (state.socket.readyState !== WebSocket.OPEN) return;

    state.socket.send(JSON.stringify(data));
}

on(channel, event, callback) {
    if (!this.channels.has(channel)) {
        this.channels.set(channel, this._initChannelState(null));
    }
    
    const state = this.channels.get(channel);
    
    if (!state.listeners.has(event)) {
        state.listeners.set(event, []);
    }

    state.listeners.get(event).push(callback);
}

off(channel, event, callback) {
    const state = this.channels.get(channel);
    if (!state || !state.listeners.has(event)) return;

    state.listeners.set(
        event,
        state.listeners.get(event).filter(cb => cb !== callback)
    );
}

emit(channel, event, payload) {
    const state = this.channels.get(channel);
    if (!state || !state.listeners.has(event)) return;

    state.listeners.get(event).forEach(cb => cb(payload));
}

isConnected(channel) {
    const state = this.channels.get(channel);
    return state ? state.connected : false;
}

getConnection(channel) {
    const state = this.channels.get(channel);
    return state ? state.socket : null;
}
}

export default new WebSocketService();