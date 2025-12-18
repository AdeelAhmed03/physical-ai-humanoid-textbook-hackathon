import React, { useState, useRef, useEffect } from 'react';
import config from '@site/src/config';
import { useTheme } from '../contexts/ThemeContext';
import styles from './ChatInterface.module.css';

const ChatInterface = ({ chapterId = null, currentChapter = null }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const { isDark } = useTheme();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call backend API
      const response = await fetch(`${config.API_BASE_URL}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          chapter_id: chapterId, // If we're in a specific chapter, limit search to it
          conversation_history: messages.map(m => ({
            sender: m.type,
            text: m.content
          }))
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.response,
        sources: data.sources || [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatSources = (sources) => {
    if (!sources || sources.length === 0) return null;

    return (
      <div className={styles.sources}>
        <strong>Sources:</strong> {sources.join(', ')}
      </div>
    );
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className={`${styles.chatContainer} ${isDark ? styles.darkTheme : styles.lightTheme}`}>
      <div className={styles.chatHeader}>
        <h3>AI Assistant</h3>
        {messages.length > 0 && (
          <button
            onClick={clearChat}
            className={styles.clearChatButton}
            title="Clear chat history"
            aria-label="Clear chat history"
          >
            Clear Chat
          </button>
        )}
      </div>

      <div className={styles.chatMessages} aria-live="polite">
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <p>Hello! I'm your AI assistant for the textbook. Ask me anything about the content.</p>
            <p>Try asking: "Explain the basics of physical AI" or "What are the key concepts in this chapter?"</p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`${styles.message} ${styles[msg.type]}`}
              role="log"
              aria-label={`Message from ${msg.type}`}
            >
              <div className={styles.messageHeader}>
                <span className={styles.sender}>{msg.type === 'user' ? 'You' : 'AI'}</span>
                <span className={styles.timestamp}>
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <div className={styles.messageContent}>
                {msg.content}
                {msg.sources && formatSources(msg.sources)}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className={`${styles.message} ${styles.ai}`}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.chatInputForm}>
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook..."
          disabled={isLoading}
          className={styles.chatInput}
          aria-label="Type your message"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className={styles.chatButton}
          aria-label="Send message"
        >
          {isLoading ? (
            <span className={styles.loadingDots}>Sending...</span>
          ) : (
            'Send'
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;