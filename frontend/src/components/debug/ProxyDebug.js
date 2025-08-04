import React, { useState } from 'react';
import axios from 'axios';

const ProxyDebug = () => {
  const [results, setResults] = useState([]);

  const testEndpoints = [
    { name: 'Direct Backend', url: 'http://localhost:8000/auth/me' },
    { name: 'Proxy Auth', url: '/auth/me' },
    { name: 'Proxy API', url: '/api/auth/me' },
    { name: 'Backend Health', url: '/auth/health' },
    { name: 'Health Check', url: '/health' }
  ];

  const testRequest = async (endpoint) => {
    const startTime = Date.now();
    try {
      console.log(`🚀 Testing: ${endpoint.name} - ${endpoint.url}`);
      
      const response = await axios.get(endpoint.url);
      const duration = Date.now() - startTime;
      
      const result = {
        name: endpoint.name,
        url: endpoint.url,
        status: 'success',
        statusCode: response.status,
        duration,
        data: response.data,
        timestamp: new Date().toLocaleTimeString()
      };
      
      console.log('✅ Success:', result);
      setResults(prev => [result, ...prev]);
      
    } catch (error) {
      const duration = Date.now() - startTime;
      
      const result = {
        name: endpoint.name,
        url: endpoint.url,
        status: 'error',
        statusCode: error.response?.status || 'Network Error',
        duration,
        error: error.response?.data || error.message,
        timestamp: new Date().toLocaleTimeString()
      };
      
      console.log('❌ Error:', result);
      setResults(prev => [result, ...prev]);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h2>🔍 Vite Proxy Debugger</h2>
      
      <div style={{ marginBottom: '20px' }}>
        {testEndpoints.map((endpoint, index) => (
          <button
            key={index}
            onClick={() => testRequest(endpoint)}
            style={{
              margin: '5px',
              padding: '10px',
              backgroundColor: '#007acc',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Test {endpoint.name}
          </button>
        ))}
        
        <button
          onClick={() => setResults([])}
          style={{
            margin: '5px',
            padding: '10px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Clear Results
        </button>
      </div>

      <div>
        <h3>Results:</h3>
        {results.map((result, index) => (
          <div
            key={index}
            style={{
              margin: '10px 0',
              padding: '10px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              backgroundColor: result.status === 'success' ? '#d4edda' : '#f8d7da'
            }}
          >
            <div><strong>{result.name}</strong> - {result.timestamp}</div>
            <div>URL: {result.url}</div>
            <div>Status: {result.statusCode} ({result.duration}ms)</div>
            {result.status === 'success' ? (
              <pre style={{ fontSize: '12px', maxHeight: '100px', overflow: 'auto' }}>
                {JSON.stringify(result.data, null, 2)}
              </pre>
            ) : (
              <div style={{ color: 'red' }}>
                Error: {JSON.stringify(result.error)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProxyDebug;
