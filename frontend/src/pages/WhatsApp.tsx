import { useState } from 'react';

export default function WhatsApp() {
  const [phone, setPhone] = useState('9800000001');
  const [text, setText] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!phone || !text) return;
    setLoading(true);
    try {
      const res = await fetch('/api/whatsapp/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, text }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: (err as Error).message });
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">WhatsApp Integration</h1>
        <p className="text-gray-500 mt-1">Simulate tenant messages via WhatsApp</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Input */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl flex items-center justify-center text-2xl text-white">
              📱
            </div>
            <div>
              <h3 className="font-bold text-gray-900">Simulate WhatsApp Message</h3>
              <p className="text-xs text-gray-500">Send a message as a tenant</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-xs text-gray-500 font-medium">Tenant Phone</label>
              <input
                type="text"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="9800000001"
                className="w-full mt-1 px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium">Message</label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Bathroom ka tap leak ho raha hai..."
                rows={4}
                className="w-full mt-1 px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
              />
            </div>
            <button
              onClick={handleSend}
              disabled={loading || !text.trim()}
              className="w-full px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-medium hover:from-green-600 hover:to-emerald-700 transition-all shadow-lg shadow-green-500/25 disabled:opacity-50"
            >
              {loading ? 'Sending...' : '📱 Send WhatsApp Message'}
            </button>
          </div>
        </div>

        {/* Response */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 className="font-bold text-gray-900 mb-4">Agent Response</h3>
          {response ? (
            <div className="space-y-4">
              <div className={`p-4 rounded-xl ${
                response.status === 'processed' ? 'bg-green-50 border border-green-100' : 'bg-gray-50 border border-gray-100'
              }`}>
                <div className="text-xs font-semibold text-gray-500 mb-1">Status</div>
                <div className="text-sm font-bold">{response.status}</div>
              </div>
              {response.agent_response && (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-100">
                  <div className="text-xs font-semibold text-blue-700 mb-2">🤖 AI Agent Response</div>
                  <div className="text-sm text-blue-800 whitespace-pre-wrap leading-relaxed">
                    {response.agent_response}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <div className="text-4xl mb-2">💬</div>
              <p>Send a message to see the response</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
