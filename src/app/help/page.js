'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, HelpCircle } from 'lucide-react';

export default function HelpPage() {
    const [messages, setMessages] = useState([
        { id: 1, sender: 'bot', text: 'Hello! I am Veritas Assistant. How can I help you with your compliance analysis today?' }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { id: Date.now(), sender: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Mock response logic
        setTimeout(() => {
            let botResponse = "I process data related to mis-selling detection.";
            if (input.toLowerCase().includes('risk')) {
                botResponse = "Risk assessment is calculated by comparing 'Promised Features' from product documents against 'Actual Experiences' from customer reviews. A high mismatch count increases the Risk Score.";
            } else if (input.toLowerCase().includes('report') || input.toLowerCase().includes('export')) {
                botResponse = "You can generate and export detailed reports from the 'Reports' section in the sidebar. We support PDF, CSV, and HTML formats.";
            } else if (input.toLowerCase().includes('hello') || input.toLowerCase().includes('hi')) {
                botResponse = "Hi there! Ask me anything about the Veritas Finance platform.";
            }

            setMessages(prev => [...prev, { id: Date.now() + 1, sender: 'bot', text: botResponse }]);
            setIsTyping(false);
        }, 1500);
    };

    return (
        <div className="container mx-auto p-6 h-[calc(100vh-2rem)] flex flex-col">
            <div className="page-header mb-4 flex-none">
                <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                    AI Assistant
                </h1>
                <p className="text-slate-400 text-sm flex items-center gap-2">
                    <HelpCircle size={14} />
                    Ask questions about compliance, risk scores, or platform navigation.
                </p>
            </div>

            <div className="card glass flex-1 flex flex-col p-0 overflow-hidden">
                {/* Chat Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-black/20">
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`flex gap-4 ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
                        >
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-none ${msg.sender === 'user' ? 'bg-blue-600' : 'bg-purple-600'
                                }`}>
                                {msg.sender === 'user' ? <User size={20} className="text-white" /> : <Bot size={20} className="text-white" />}
                            </div>

                            <div className={`p-4 rounded-2xl max-w-[80%] text-sm leading-relaxed shadow-lg ${msg.sender === 'user'
                                    ? 'bg-blue-600/20 border border-blue-500/30 text-white rounded-tr-sm'
                                    : 'bg-slate-800/80 border border-slate-700 text-slate-200 rounded-tl-sm'
                                }`}>
                                {msg.text}
                            </div>
                        </div>
                    ))}

                    {isTyping && (
                        <div className="flex gap-4 flex-row">
                            <div className="w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center flex-none">
                                <Bot size={20} className="text-white" />
                            </div>
                            <div className="p-4 rounded-2xl bg-slate-800/80 border border-slate-700 text-slate-400 rounded-tl-sm flex items-center gap-2">
                                <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                                <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                                <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-slate-900/50 border-t border-white/5">
                    <form onSubmit={handleSendMessage} className="flex gap-4">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your question here..."
                            className="flex-1 bg-black/30 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
                        />
                        <button
                            type="submit"
                            disabled={!input.trim() || isTyping}
                            className="btn btn-primary rounded-xl px-6"
                        >
                            <Send size={20} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
